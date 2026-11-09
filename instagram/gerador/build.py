import json, sys
from pathlib import Path
from PIL import Image
from layouts import *
import semana01

SEM = 'semana-01'
OUT = REPO / 'instagram' / 'posts' / SEM
BASEURL = 'https://www.lumifa.com.br/instagram/posts/' + SEM
INICIO = ['2026-11-11','2026-11-12','2026-11-13','2026-11-14','2026-11-15','2026-11-16','2026-11-17']

cal = []
with Renderer() as r:
    bpath = Path('/home/claude/work/banner.jpg'); r.render(banner(), bpath, 3240, 1350)
    B = Image.open(bpath)
    for i, p in enumerate(semana01.posts, 1):
        files = []
        for k, s in enumerate(p['slides'], 1):
            name = f"d{p['day']}-{p['time'].replace(':','h')}-{p['slug']}" + (f"-{k}" if len(p['slides']) > 1 else '') + '.jpg'
            out = OUT / name
            if s.startswith('BANNER:'):
                t = int(s.split(':')[1]); out.parent.mkdir(parents=True, exist_ok=True)
                B.crop((t*1080, 0, t*1080+1080, 1350)).save(out, 'JPEG', quality=90, optimize=True, progressive=True)
            else:
                r.render(s, out)
            files.append(f"{BASEURL}/{name}")
        cal.append(dict(id=f"{SEM}-{i:02d}", data=INICIO[p['day']-1], hora=p['time'], dia=p['day'], tipo=p['tipo'], titulo=p['titulo'],
                        formato='carrossel' if len(files) > 1 else 'imagem', imagens=files, legenda=p['caption'], status='aguardando aprovação'))
(REPO/'instagram'/'calendario-semana-01.json').write_text(json.dumps(cal, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(cal), sum(len(c['imagens']) for c in cal))
for c in cal: print(c['data'], c['hora'], c['tipo'], c['titulo'], len(c['imagens']), len(c['legenda']))
