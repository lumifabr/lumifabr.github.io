"""Baixa fotos extras dos produtos Embuled direto do site da fábrica (embuled.com).

Uso:  python baixar.py produtos.csv <pasta_saida> [pasta_imagens_atuais]

- produtos.csv: codigo, codigo_embuled, pagina_pdf, foto_errada
  (pagina_pdf = link "PHOTO" do PDF; vazio = procura pelo código no site)
- Para cada produto: abre a página, confere o SKU, pega as fotos em tamanho original.
- Descarta fotos que mostram o nome EMBULED (leitura de texto/OCR), fotos pequenas,
  e fotos iguais à que o site já tem.
- Remove metadados (EXIF) e salva com no máximo 1600 px, JPEG 85.
- Saída: <saida>/fotos/PROD-xxx-e<n>.jpg, <saida>/rejeitadas/..., <saida>/relatorio.csv
"""
import csv, io, json, os, re, sys, time, hashlib
from urllib.parse import urljoin, quote

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps
import pytesseract
import imagehash

BASE = "https://embuled.com"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124 Safari/537.36"}
MAX_LADO = 1600
MIN_LADO = 500
PAUSA = 0.6

s = requests.Session()
s.headers.update(UA)


def norm(t):
    return re.sub(r"[^0-9A-Z]", "", (t or "").upper())


def get(url, **kw):
    for tentativa in range(3):
        try:
            r = s.get(url, timeout=40, **kw)
            time.sleep(PAUSA)
            if r.status_code == 200:
                return r
            if r.status_code == 404:
                return None
        except requests.RequestException:
            pass
        time.sleep(3 * (tentativa + 1))
    return None


# ---------- leitura da página ----------
TAM = re.compile(r"-\d{2,4}x\d{2,4}(?=\.(?:jpe?g|png|webp|gif)$)", re.I)


def original(u):
    u = u.split("?")[0]
    u = TAM.sub("", u)
    u = re.sub(r"-scaled(?=\.(?:jpe?g|png|webp|gif)$)", "", u, flags=re.I)
    return u


def ler_pagina(url):
    r = get(url)
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    sku = " ".join(x.get_text(" ", strip=True) for x in soup.select(".sku, .sku_wrapper"))
    titulo = (soup.select_one("h1.product_title, h1") or soup.new_tag("x")).get_text(" ", strip=True)
    imgs = []

    def add(u):
        if not u or "/wp-content/uploads/" not in u:
            return
        if not re.search(r"\.(jpe?g|png|webp|gif)(\?|$)", u, re.I):
            return
        u = original(urljoin(url, u))
        if u not in imgs:
            imgs.append(u)

    gal = soup.select(".woocommerce-product-gallery__image, .woocommerce-product-gallery figure, .product-gallery, .woocommerce-product-gallery")
    for g in gal:
        for el in g.select("[data-large_image]"):
            add(el.get("data-large_image"))
        for el in g.select("[data-thumb_org]"):
            add(el.get("data-thumb_org"))
        for a in g.select("a[href]"):
            add(a["href"])
        for im in g.select("img"):
            add(im.get("data-large_image") or im.get("data-src") or im.get("src"))
    # fotos de variações (cores) do WooCommerce
    for f in soup.select("form.variations_form[data-product_variations]"):
        try:
            for v in json.loads(f["data-product_variations"]):
                im = v.get("image") or {}
                add(im.get("full_src") or im.get("url"))
        except Exception:
            pass
    if not imgs:  # último recurso
        og = soup.select_one('meta[property="og:image"]')
        if og:
            add(og.get("content"))
    return {"url": r.url, "sku": sku, "titulo": titulo, "imagens": imgs, "html": r.text}


def procurar(codigo):
    """Procura o produto pelo código no site. Só aceita se o SKU da página bater."""
    for q in (codigo, re.sub(r"^[A-Z]+", "", codigo)):
        if not q:
            continue
        r = get(f"{BASE}/?s={quote(q)}&post_type=product")
        if not r:
            continue
        candidatos = []
        if "/produto/" in r.url:
            candidatos.append(r.url)
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.select("a[href*='/produto/']"):
            h = a["href"].split("?")[0]
            if h not in candidatos:
                candidatos.append(h)
        for c in candidatos[:6]:
            p = ler_pagina(c)
            if p and sku_bate(codigo, p["sku"]):
                return p
    return None


def sku_bate(codigo, sku_txt):
    c = norm(codigo)
    if not c:
        return False
    partes = [norm(x) for x in re.split(r"[\s,/;|]+|(?<=\d)-(?=[A-Z])", sku_txt or "")]
    partes = [p for p in partes if p]
    dig = re.sub(r"\D", "", c)
    for p in partes:
        if p == c or p.replace("SKU", "") == c:
            return True
        if dig and re.sub(r"\D", "", p) == dig and len(dig) >= 4:
            return True
    return c in norm(sku_txt)


# ---------- marca na imagem ----------
MARCA = re.compile(r"EMBU|MBULE|BULED|EMBLED|EMBULD|ENBULED|EMBUIED|EMBUL3D", re.I)


def tem_marca(img):
    """Lê o texto da imagem em várias versões (normal, cinza ampliado, invertido, cantos)."""
    textos = []
    g = ImageOps.grayscale(img)
    w, h = g.size
    escala = 2 if max(w, h) < 1400 else 1
    big = g.resize((w * escala, h * escala)) if escala > 1 else g
    versoes = [big, ImageOps.invert(big), ImageOps.autocontrast(big)]
    # recortes dos cantos e das faixas de cima/baixo, onde costuma ficar a logo
    W, H = big.size
    for box in [(0, 0, W, H // 4), (0, 3 * H // 4, W, H),
                (0, 0, W // 2, H // 2), (W // 2, 0, W, H // 2),
                (0, H // 2, W // 2, H), (W // 2, H // 2, W, H)]:
        c = big.crop(box)
        c = c.resize((c.width * 2, c.height * 2))
        versoes.append(c)
    for v in versoes:
        for psm in ("11",):
            try:
                t = pytesseract.image_to_string(v, config=f"--psm {psm}")
            except Exception:
                t = ""
            textos.append(t)
            if MARCA.search(norm(t)):
                return True, t.strip()[:80]
    return False, ""


CARIMBO = re.compile(r"EB[A-Z]{0,4}\d{3,}|[A-Z]{2,4}\d{4,}|\d{1,2}:\d{2}|JANEIRO|FEVEREIRO|MARCO|ABRIL|"
                     r"MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO|FEIRA|SIZE")


def limpar_carimbo(img):
    """Apaga (pinta de branco) o carimbo de desenho técnico com o código da fábrica e a data,
    ex.: "EBAR80329&EBAR80330 SIZE / terça-feira, 3 de junho de 2025". Só apaga sobre fundo branco."""
    g = ImageOps.grayscale(img)
    big = g.resize((g.width * 2, g.height * 2))
    try:
        d = pytesseract.image_to_data(big, config="--psm 11", output_type=pytesseract.Output.DICT)
    except Exception:
        return img, False
    caixas = []
    for i, t in enumerate(d["text"]):
        if t.strip():
            caixas.append((d["left"][i] // 2, d["top"][i] // 2, d["width"][i] // 2, d["height"][i] // 2,
                           norm(t.replace("Ç", "C"))))
    alvo = [c for c in caixas if CARIMBO.search(c[4]) and c[3] <= 30]
    if not alvo:
        return img, False
    apagar = set()
    for (x, y, w, h, _) in alvo:
        for c in caixas:  # palavras da mesma linha/bloco pequeno, logo abaixo ou ao lado
            cy = c[1] + c[3] / 2
            if c[3] <= 2 * h + 4 and y - 3 * h <= cy <= y + 4 * h:
                apagar.add(c[:4])
    from PIL import ImageDraw, ImageStat
    xs = [b[0] for b in apagar]; ys = [b[1] for b in apagar]
    xe = [b[0] + b[2] for b in apagar]; ye = [b[1] + b[3] for b in apagar]
    caixa = (max(0, min(xs) - 8), max(0, min(ys) - 8), min(img.width, max(xe) + 8), min(img.height, max(ye) + 8))
    # só apaga se em volta do carimbo for fundo claro (texto solto, não em cima do produto)
    x0, y0, x1, y1 = caixa
    m = 10
    moldura = [g.crop((max(0, x0 - m), max(0, y0 - m), min(g.width, x1 + m), y0)),
               g.crop((max(0, x0 - m), y1, min(g.width, x1 + m), min(g.height, y1 + m))),
               g.crop((max(0, x0 - m), y0, x0, y1)), g.crop((x1, y0, min(g.width, x1 + m), y1))]
    vals = [ImageStat.Stat(c).mean[0] for c in moldura if c.width > 0 and c.height > 0]
    feito = False
    out = img
    if vals and min(vals) > 225 and (x1 - x0) * (y1 - y0) < 0.15 * img.width * img.height:
        out = img.copy()
        ImageDraw.Draw(out).rectangle(caixa, fill=(255, 255, 255))
        feito = True
    return out, feito


ETIQ = re.compile(r"ODEL|NPUT|UTPUT|RIVER|ROHS|BIVOLT|SLIMFIT|\d{2,3}VAC|\d{2,3}V\d")


def etiqueta(img):
    """Fotos com etiqueta impressa no produto (driver, fonte, lâmpada): a logo pode estar
    pequena na etiqueta e escapar da leitura. Marca para conferência manual."""
    g = ImageOps.grayscale(img)
    g = g.resize((g.width * 2, g.height * 2))
    for ang in (0, 45, -45, 90):
        try:
            t = pytesseract.image_to_string(g.rotate(ang, expand=True, fillcolor=255), config="--psm 11")
        except Exception:
            continue
        if ETIQ.search(norm(t)):
            return True
    return False


def salvar_relatorio(saida, linhas):
    campos = ["codigo", "codigo_embuled", "nome", "foto_errada", "status", "arquivo", "tipo", "conferir",
              "carimbo_apagado", "origem",
              "sku_confere", "sku_pagina", "largura", "altura", "pagina", "url_foto", "texto_lido"]
    with open(f"{saida}/relatorio.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        w.writerows(linhas)


# ---------- principal ----------
def main():
    entrada, saida = sys.argv[1], sys.argv[2]
    atuais = sys.argv[3] if len(sys.argv) > 3 else None
    os.makedirs(f"{saida}/fotos", exist_ok=True)
    os.makedirs(f"{saida}/rejeitadas", exist_ok=True)
    os.makedirs(f"{saida}/debug", exist_ok=True)

    produtos = list(csv.DictReader(open(entrada, encoding="utf-8")))
    so = os.environ.get("SOMENTE", "").strip()  # ex.: "foto_errada" ou "PROD-123,PROD-124"
    if so == "foto_errada":
        produtos = [p for p in produtos if p["foto_errada"]]
    elif so:
        alvo = {x.strip() for x in so.split(",")}
        produtos = [p for p in produtos if p["codigo"] in alvo]
    # foto errada primeiro
    produtos.sort(key=lambda p: (not p["foto_errada"], p["codigo"]))
    codigos_todos = {norm(p["codigo_embuled"]) for p in csv.DictReader(open(entrada, encoding="utf-8"))}

    cache_pag, cache_img = {}, {}
    linhas = []
    debug_n = 0

    def hash_atual(cod):
        if not atuais:
            return None
        f = os.path.join(atuais, f"{cod}.jpg")
        if not os.path.exists(f):
            return None
        try:
            return imagehash.phash(Image.open(f).convert("RGB"))
        except Exception:
            return None

    for i, p in enumerate(produtos, 1):
        if i % 25 == 0:  # grava o relatório aos poucos (se a rodada for interrompida, não se perde)
            salvar_relatorio(saida, linhas)
        cod, ce = p["codigo"], p["codigo_embuled"]
        print(f"[{i}/{len(produtos)}] {cod} {ce}", flush=True)
        base = {"codigo": cod, "codigo_embuled": ce, "foto_errada": p["foto_errada"]}
        pag, origem = None, ""
        if p["pagina_pdf"] and "embuled.com/produto/" in p["pagina_pdf"]:
            u = p["pagina_pdf"]
            if u not in cache_pag:
                cache_pag[u] = ler_pagina(u)
            pag, origem = cache_pag[u], "pdf"
        if not pag:
            pag, origem = procurar(ce), "busca"
        if not pag:
            linhas.append({**base, "status": "sem_pagina"})
            continue
        if debug_n < 3:
            open(f"{saida}/debug/pagina{debug_n}.html", "w").write(pag["html"])
            debug_n += 1
        sku_ok = sku_bate(ce, pag["sku"])
        if origem == "busca" and not sku_ok:
            linhas.append({**base, "status": "sem_pagina"})
            continue

        # separa as fotos: as que têm o código deste produto no nome, as que têm
        # o código de OUTRO produto (outra cor) e as gerais da página
        minhas, gerais = [], []
        c = norm(ce)
        for u in pag["imagens"]:
            nome = norm(os.path.basename(u))
            if c and c in nome:
                minhas.append(u)
            elif any(o and o != c and len(o) >= 5 and o in nome for o in codigos_todos):
                continue
            else:
                gerais.append(u)
        # se a página tem fotos com o código deste produto, as gerais ficam de fora
        # (costumam mostrar outra cor ou outro modelo da mesma página)
        escolhidas = minhas if minhas else gerais
        h_atual = hash_atual(cod)
        n = 0
        for u in escolhidas:
            if u not in cache_img:
                r = get(u)
                if not r:
                    cache_img[u] = None
                else:
                    try:
                        im = Image.open(io.BytesIO(r.content))
                        if getattr(im, "is_animated", False):
                            im.seek(0)
                        im = ImageOps.exif_transpose(im)
                        if im.mode in ("RGBA", "LA", "P"):
                            im = im.convert("RGBA")
                            fundo = Image.new("RGB", im.size, (255, 255, 255))
                            fundo.paste(im, mask=im.split()[-1])
                            im = fundo
                        im = im.convert("RGB")
                        im, apagou = limpar_carimbo(im)
                        marca, txt = tem_marca(im)
                        cache_img[u] = (im, marca, txt, imagehash.phash(im), apagou, etiqueta(im))
                    except Exception as ex:
                        print("  erro imagem", u, ex)
                        cache_img[u] = None
            item = cache_img[u]
            reg = {**base, "origem": origem, "pagina": pag["url"], "sku_pagina": pag["sku"][:60],
                   "sku_confere": "sim" if sku_ok else "nao", "url_foto": u,
                   "tipo": "propria" if u in minhas else "geral"}
            if not item:
                linhas.append({**reg, "status": "erro_download"}); continue
            im, marca, txt, ph, apagou, etq = item
            motivo = []
            if p.get("conferir_tipo"):
                motivo.append("tipo_produto")
            if etq:
                motivo.append("etiqueta")
            if reg["tipo"] == "geral":
                motivo.append("foto_geral_da_pagina")
            reg.update(carimbo_apagado="sim" if apagou else "", conferir="+".join(motivo), nome=p.get("nome", ""))
            reg.update(largura=im.width, altura=im.height)
            if marca and os.environ.get("ACEITAR_MARCA", "") != "1":
                status = "marca_embuled"
            elif min(im.size) < MIN_LADO:
                status = "pequena"
            elif h_atual is not None and (ph - h_atual) <= 6:
                status = "igual_atual"
            else:
                status = "ok"
            out = im.copy()
            out.thumbnail((MAX_LADO, MAX_LADO))
            if status == "ok":
                n += 1
                nome = f"{cod}-e{n}.jpg"
                out.save(f"{saida}/fotos/{nome}", "JPEG", quality=85, optimize=True)
            else:
                nome = f"{cod}-{status}-{hashlib.md5(u.encode()).hexdigest()[:6]}.jpg"
                out.thumbnail((600, 600))
                out.save(f"{saida}/rejeitadas/{nome}", "JPEG", quality=75)
            linhas.append({**reg, "status": status, "arquivo": nome, "texto_lido": txt})
        if not escolhidas:
            linhas.append({**base, "origem": origem, "pagina": pag["url"], "status": "pagina_sem_fotos"})

    salvar_relatorio(saida, linhas)
    from collections import Counter
    print("RESUMO", Counter(l["status"] for l in linhas))


if __name__ == "__main__":
    main()
