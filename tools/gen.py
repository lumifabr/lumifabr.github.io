"""Gera fotos extras para o Mercado Livre a partir da foto do site.
Saída: /home/claude/work/out/PROD-xxxx-<n>.jpg
  -1 capa 1200x1200 (fundo branco, produto centralizado) | kit: grade com N unidades
  -2 detalhe (zoom) se a resolução permitir
  -3 ficha técnica
  -4 temperaturas de cor (só produtos com 3 temperaturas / CCT)
"""
import json, re, sys, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

SRC = '/home/claude/lumifabr.github.io/imagens/'
OUT = '/home/claude/work/out/'
os.makedirs(OUT, exist_ok=True)
S = 1200
GOLD = (150, 112, 26); DARK = (34, 30, 26); GREY = (110, 104, 98); LINE = (226, 220, 210)
F = '/usr/share/fonts/opentype/inter/Inter-'
def font(w, s): return ImageFont.truetype(F + w + '.otf', s)

def is_white_bg(im):
    a = np.asarray(im.convert('L'))
    b = np.concatenate([a[:6].ravel(), a[-6:].ravel(), a[:, :6].ravel(), a[:, -6:].ravel()])
    return (b > 232).mean() > 0.85

def bbox(im):
    a = np.asarray(im.convert('L'))
    ys, xs = np.where(a < 236)
    if len(xs) < 50: return (0, 0, im.width, im.height)
    # ignora pixels isolados nas bordas (ruído de compressão)
    x0, x1 = np.percentile(xs, [0.2, 99.8]); y0, y1 = np.percentile(ys, [0.2, 99.8])
    return int(x0), int(y0), int(x1) + 1, int(y1) + 1

def clean_white(im):
    a = np.asarray(im).astype(np.int16)
    m = (a.min(axis=2) > 244)
    a[m] = 255
    return Image.fromarray(a.astype(np.uint8))

def fit(im, box_w, box_h):
    r = min(box_w / im.width, box_h / im.height)
    return im.resize((max(1, round(im.width * r)), max(1, round(im.height * r))), Image.LANCZOS)

def capa(im, white):
    if white:
        p = clean_white(im.crop(bbox(im)))
        p = fit(p, int(S * 0.86), int(S * 0.86))
        c = Image.new('RGB', (S, S), 'white'); c.paste(p, ((S - p.width) // 2, (S - p.height) // 2)); return c
    # foto ambientada: recorte quadrado central quando quase quadrada, senão fundo com a própria foto desfocada
    ar = im.width / im.height
    if 0.8 <= ar <= 1.25:
        s = min(im.size); x = (im.width - s) // 2; y = (im.height - s) // 2
        return im.crop((x, y, x + s, y + s)).resize((S, S), Image.LANCZOS)
    bg = im.resize((S, S), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
    p = fit(im, S, S); bg.paste(p, ((S - p.width) // 2, (S - p.height) // 2)); return bg

def multi(im):
    import cv2
    a = np.asarray(im.convert('L').resize((300, 300)))
    m = (a < 236).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n_, lab, st, _ = cv2.connectedComponentsWithStats(m)
    areas = st[1:, cv2.CC_STAT_AREA]
    return len(areas) and (areas > 0.15 * areas.sum()).sum() > 1
def kit(im, white, n):
    if not white or multi(im): return capa(im, white)
    base = clean_white(im.crop(bbox(im))) if white else im
    cols = {2: 2, 3: 3, 4: 2, 5: 3, 6: 3, 10: 5, 25: 5}.get(n, math.ceil(math.sqrt(n)))
    rows = math.ceil(n / cols)
    if n == 25: cols, rows = 5, 5
    pad = 30; top = 150
    cw = (S - pad * (cols + 1)) // cols; ch = (S - top - pad * (rows + 1)) // rows
    c = Image.new('RGB', (S, S), 'white'); d = ImageDraw.Draw(c)
    t = fit(base, cw, ch)
    k = 0
    for r_ in range(rows):
        cnt = min(cols, n - k)
        off = (S - (cnt * cw + (cnt - 1) * pad)) // 2
        for j in range(cnt):
            x = off + j * (cw + pad) + (cw - t.width) // 2
            y = top + pad + r_ * (ch + pad) + (ch - t.height) // 2
            c.paste(t, (x, y)); k += 1
    txt = f'KIT COM {n} UNIDADES'
    f = font('Bold', 64); w = d.textlength(txt, font=f)
    d.text(((S - w) / 2, 50), txt, font=f, fill=DARK)
    return c

def detalhe(im, white):
    x0, y0, x1, y1 = bbox(im) if white else (0, 0, im.width, im.height)
    if white:
        import cv2
        a = np.asarray(im.convert('L').resize((300, 300)))
        m = (a < 236).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
        n_, lab, st, _ = cv2.connectedComponentsWithStats(m)
        areas = st[1:, cv2.CC_STAT_AREA]
        if len(areas) and (areas > 0.15 * areas.sum()).sum() > 1: return None   # mais de um objeto na foto
    w, h = x1 - x0, y1 - y0
    s = int(max(w, h) * 0.5)
    if s < 420: return None
    cx, cy = x0 + w // 2, y0 + h // 2
    # procura a região mais "rica" em detalhe dentro do produto (maior variância)
    g = np.asarray(im.convert('L')).astype(np.float32)
    best, bxy = -1, (cx, cy)
    for fx in (0.3, 0.5, 0.7):
        for fy in (0.3, 0.5, 0.7):
            px, py = int(x0 + w * fx), int(y0 + h * fy)
            a = max(0, px - s // 2); b = max(0, py - s // 2)
            reg = g[b:b + s, a:a + s]
            if reg.size == 0: continue
            v = reg.std() * (reg < 236).mean()
            if v > best: best, bxy = v, (px, py)
    px, py = bxy
    a = min(max(0, px - s // 2), max(0, im.width - s)); b = min(max(0, py - s // 2), max(0, im.height - s))
    cr = im.crop((a, b, a + s, b + s))
    if white: cr = clean_white(cr)
    if (np.asarray(cr.convert('L')) < 236).mean() < 0.12: return None   # quase vazio
    return cr.resize((S, S), Image.LANCZOS)

ROT = {'Potência': 'Potência', 'Temperatura de cor': 'Temperatura de cor', 'Tensão': 'Tensão', 'Fluxo': 'Fluxo luminoso',
       'Dimensões': 'Dimensões', 'Cabo': 'Cabo', 'Material': 'Material', 'Acabamento': 'Acabamento', 'Base': 'Base / soquete',
       'Proteção': 'Proteção', 'IRC': 'IRC', 'Ângulo': 'Ângulo de abertura', 'Cor': 'Cor'}
def specs(r):
    out = []
    for p in r['especificacoes'].split('|')[1:]:
        if ':' not in p: continue
        k, v = [x.strip() for x in p.split(':', 1)]
        if not v or k not in ROT: continue
        v = re.sub(r'\s+', ' ', v).strip(' |;,')
        if k == 'Material': v = v.strip(' +')
        if k == 'Fluxo': v = re.sub(r'(?i)lm', ' lm', v).replace('  ', ' ')
        out.append((ROT[k], v))
    return out

def wrap(d, text, f, maxw):
    ws = text.split(); lines = []; cur = ''
    for w in ws:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def ficha(im, white, r, nome, n):
    sp = specs(r)
    if n > 1: sp = [('Quantidade', f'{n} unidades')] + sp
    if len(sp) < 2: return None
    c = Image.new('RGB', (S, S), 'white'); d = ImageDraw.Draw(c)
    d.text((70, 60), 'FICHA TÉCNICA', font=font('SemiBold', 30), fill=GOLD)
    fy = 108
    for ln in wrap(d, nome, font('Bold', 46), S - 140)[:3]:
        d.text((70, fy), ln, font=font('Bold', 46), fill=DARK); fy += 58
    d.line([(70, fy + 20), (S - 70, fy + 20)], fill=GOLD, width=3)
    top = fy + 60
    # imagem à esquerda
    p = clean_white(im.crop(bbox(im))) if white else im
    p = fit(p, 430, S - top - 90)
    c.paste(p, (70 + (430 - p.width) // 2, top + (S - top - 90 - p.height) // 2))
    # tabela à direita
    x = 560; y = top; kf = font('Medium', 26); vf = font('SemiBold', 34)
    rowh = min(112, (S - top - 70) // max(1, len(sp)))
    for k, v in sp[:9]:
        d.text((x, y), k.upper(), font=kf, fill=GREY)
        vl = wrap(d, v, vf, S - x - 70)[:2]
        yy = y + 32
        for l in vl: d.text((x, yy), l, font=vf, fill=DARK); yy += 40
        y = max(y + rowh, yy + 18)
        d.line([(x, y - 12), (S - 70, y - 12)], fill=LINE, width=2)
        if y > S - 80: break
    return c

def temps(r):
    t = r['nome'] + ' ' + r['especificacoes']
    ks = sorted(set(int(x) for x in re.findall(r'(?<!\d)(\d{4})\s?K\b', t, re.I)))
    if len(ks) >= 3 or re.search(r'3 temperaturas|CCT', t, re.I):
        return ks if len(ks) >= 2 else [3000, 4000, 6000]
    m = re.search(r'(\d{4})K\s*[ÀA]\s*(\d{4})K', t, re.I)
    if m: return [int(m.group(1)), 4500, int(m.group(2))]
    return None
def kcolor(k):
    if k <= 2800: return (255, 196, 120)
    if k <= 3500: return (255, 214, 150)
    if k <= 4500: return (255, 241, 218)
    return (224, 236, 255)
def klabel(k):
    return 'Luz quente' if k <= 3500 else ('Luz neutra' if k < 5000 else 'Luz fria')
def temperaturas(im, white, ks):
    ks = ks[:3]
    c = Image.new('RGB', (S, S), 'white'); d = ImageDraw.Draw(c)
    t = f'{len(ks)} TEMPERATURAS DE COR'
    f = font('Bold', 56); d.text(((S - d.textlength(t, font=f)) / 2, 70), t, font=f, fill=DARK)
    sub = 'Escolha o tom de luz ideal para cada ambiente'
    f2 = font('Regular', 32); d.text(((S - d.textlength(sub, font=f2)) / 2, 150), sub, font=f2, fill=GREY)
    p = clean_white(im.crop(bbox(im))) if white else im
    w = (S - 140 - 40 * (len(ks) - 1)) // len(ks)
    for i, k in enumerate(ks):
        x = 70 + i * (w + 40); y = 260
        tile = Image.new('RGB', (w, 640), kcolor(k))
        # brilho radial suave
        g = Image.new('L', (w, 640), 0); gd = ImageDraw.Draw(g)
        gd.ellipse([w * 0.05, 40, w * 0.95, 600], fill=140); g = g.filter(ImageFilter.GaussianBlur(70))
        tile = Image.composite(Image.new('RGB', (w, 640), (255, 255, 255)), tile, g)
        q = fit(p, int(w * 0.8), 470)
        if white:
            mask = Image.fromarray((np.asarray(q.convert('L')) < 238).astype(np.uint8) * 255).filter(ImageFilter.GaussianBlur(1))
            tile.paste(q, ((w - q.width) // 2, 60 + (470 - q.height) // 2), mask)
        else:
            tile.paste(q, ((w - q.width) // 2, 60 + (470 - q.height) // 2))
        c.paste(tile, (x, y))
        d.rounded_rectangle([x, y, x + w, y + 640], radius=24, outline=LINE, width=3)
        l1 = f'{k}K'; f3 = font('Bold', 52); d.text((x + (w - d.textlength(l1, font=f3)) / 2, y + 680), l1, font=f3, fill=DARK)
        l2 = klabel(k); f4 = font('Medium', 32); d.text((x + (w - d.textlength(l2, font=f4)) / 2, y + 750), l2, font=f4, fill=GREY)
    return c

def gera(cod, nome, n, r, quais=('1', '2', '3', '4')):
    im = Image.open(SRC + cod + '.jpg').convert('RGB')
    white = is_white_bg(im)
    feitos = []
    suf = f'-K{n}' if n > 1 else ''
    if '1' in quais:
        (kit(im, white, n) if n > 1 else capa(im, white)).save(OUT + f'{cod}{suf}-1.jpg', quality=84, optimize=True); feitos.append('1')
    if '2' in quais:
        dt = detalhe(im, white)
        if dt is not None: dt.save(OUT + f'{cod}-2.jpg', quality=84, optimize=True); feitos.append('2')
    if '3' in quais:
        fi = ficha(im, white, r, nome, n)
        if fi is not None: fi.save(OUT + f'{cod}{suf}-3.jpg', quality=86, optimize=True); feitos.append('3')
    if '4' in quais:
        ks = temps(r)
        if ks: temperaturas(im, white, ks).save(OUT + f'{cod}-4.jpg', quality=86, optimize=True); feitos.append('4')
    if n > 1 and '1' in quais:
        capa(im, white).save(OUT + f'{cod}-1.jpg', quality=84, optimize=True); feitos.append('u')
    return feitos

if __name__ == '__main__':
    cat = {r['codigo']: r for r in json.load(open('/home/claude/ml/ok.json'))}
    for arg in sys.argv[1:]:
        cod, n = (arg.split(':') + ['1'])[:2]
        print(cod, gera(cod, cat[cod]['nome'], int(n), cat[cod]))
