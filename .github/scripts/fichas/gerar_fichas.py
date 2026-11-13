# Gera a "ficha técnica" (2ª foto) para os produtos que ainda não têm.
# Lê o CSV publicado da planilha (aba Página1), usa a foto em imagens/ e as especificações.
# Saída: galeria/PROD-xxxx-3.webp (1000x1000) e galeria/mini/PROD-xxxx-3.webp (200x200).
# Não mexe em fichas que já existem. Uso: python gerar_fichas.py planilha.csv [raiz-do-site]
import csv, os, re, sys
from PIL import Image, ImageDraw, ImageFont
CSV = sys.argv[1]; ROOT = sys.argv[2] if len(sys.argv) > 2 else '.'
AQUI = os.path.dirname(os.path.abspath(__file__))
F = lambda w, s: ImageFont.truetype(os.path.join(AQUI, f'Inter_{w}.ttf'), s)
GOLD, INK, GREY, LINE = (150, 112, 26), (26, 22, 18), (110, 104, 96), (222, 218, 210)
W = 1000; M = 58

def wrap(d, txt, font, maxw):
    out, cur = [], ''
    for w in txt.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: out.append(cur)
            cur = w
    if cur: out.append(cur)
    return out

def specs_of(s):
    rows = []
    for part in (s or '').split('|'):
        if ':' not in part: continue
        k, v = part.split(':', 1); k, v = k.strip(), v.strip()
        if k and v and len(rows) < 8: rows.append((k.upper(), v))
    return rows

def ficha(code, name, specs, foto, out, mini):
    im = Image.new('RGB', (W, W), 'white'); d = ImageDraw.Draw(im)
    y = 52
    d.text((M, y), 'FICHA TÉCNICA', font=F('600SemiBold', 22), fill=GOLD); y += 40
    fs = 34
    while True:
        tf = F('700Bold', fs); lines = wrap(d, name, tf, W - 2 * M)
        if len(lines) <= 2 or fs <= 26: break
        fs -= 2
    for l in lines[:3]: d.text((M, y), l, font=tf, fill=INK); y += int(fs * 1.25)
    y += 14; d.line((M, y, W - M, y), fill=GOLD, width=3); y += 32
    top = y
    # foto à esquerda
    p = Image.open(foto).convert('RGB')
    # recorta bordas brancas
    bbox = Image.eval(p.convert('L'), lambda v: 255 if v < 240 else 0).getbbox()
    if bbox: p = p.crop(bbox)
    box = (int(W * 0.40) - M, W - top - 60)
    p.thumbnail(box, Image.LANCZOS)
    im.paste(p, (M + (box[0] - p.width) // 2, top + (box[1] - p.height) // 2))
    # especificações à direita
    x = int(W * 0.467); yy = top + 6
    for k, v in specs:
        d.text((x, yy), k, font=F('500Medium', 20), fill=GREY); yy += 29
        for l in wrap(d, v, F('600SemiBold', 25), W - M - x)[:2]:
            d.text((x, yy), l, font=F('600SemiBold', 25), fill=INK); yy += 33
        yy += 18; d.line((x, yy, W - M, yy), fill=LINE, width=2); yy += 22
        if yy > W - 80: break
    im.save(out, 'WEBP', quality=82)
    m = im.copy(); m.thumbnail((200, 200), Image.LANCZOS); m.save(mini, 'WEBP', quality=80)

gal = os.path.join(ROOT, 'galeria'); os.makedirs(os.path.join(gal, 'mini'), exist_ok=True)
# correções de português (correcoes.json do site): valem enquanto a planilha tem o valor antigo
try:
    import json
    CORR = json.load(open(os.path.join(ROOT, 'correcoes.json'), encoding='utf-8'))
except Exception:
    CORR = {}
# refazer.txt: códigos cuja ficha deve ser refeita (nome corrigido, foto trocada). Esvaziado depois.
REF_TXT = os.path.join(AQUI, 'refazer.txt')
REFAZER = set(open(REF_TXT).read().split()) if os.path.exists(REF_TXT) else set()
feitas = 0
with open(CSV, encoding='utf-8') as fh:
    for r in csv.DictReader(fh):
        code = (r.get('codigo') or '').strip().upper()
        if not re.match(r'^PROD-\d+$', code): continue
        for k, (antes, depois) in CORR.get(code, {}).items():
            if k in ('nome', 'especificacoes') and (r.get(k) or '').strip() == antes.strip(): r[k] = depois
        out = os.path.join(gal, f'{code}-3.webp')
        if os.path.exists(out) and code not in REFAZER: continue
        specs = specs_of(r.get('especificacoes'))
        foto = os.path.join(ROOT, 'imagens', f'{code}.jpg')
        if not specs or not os.path.exists(foto): continue
        try:
            ficha(code, re.sub(r'\(\s+', '(', re.sub(r'\s+\)', ')', (r.get('nome') or code).strip())), specs, foto, out, os.path.join(gal, 'mini', f'{code}-3.webp')); feitas += 1
        except Exception as e:
            print('erro', code, e)
print(feitas, 'fichas novas')
if REFAZER: open(REF_TXT, 'w').write('')
