import re, json
from pathlib import Path
from PIL import Image
from layouts import *
from reel import bg
import reels_semana01 as RS
R = REPO/'instagram'
OUT = R/'stories'/'banco'
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'https://www.lumifa.com.br/instagram/stories/banco'

frame = bg(f"""<img src='{LOGO_DARK}' style='position:absolute;top:250px;left:50%;transform:translateX(-50%);height:66px'>
<div style='position:absolute;top:360px;left:0;right:0;text-align:center'><div class='kick'>Dica LumiFa</div></div>
<div style='position:absolute;top:1530px;left:0;right:0;text-align:center'><p style='font-size:32px;color:#cbbf9f;letter-spacing:.04em'>Mais dicas no perfil · <b style='color:{GOLD}'>@lumifa.br</b></p></div>""")
cta1 = bg(f"""<div style='position:absolute;left:90px;right:90px;top:430px;text-align:center;display:flex;flex-direction:column;align-items:center'>
<img src='{ICONE}' style='width:180px'><h1 style='font-size:100px;margin-top:60px'>Como pedir seu<br><span class='gold'>orçamento</span></h1>
<p style='font-size:40px;color:#ddd2bb;margin-top:50px;line-height:1.6'>1 · Escolha em lumifa.com.br<br>2 · Monte o “Meu Orçamento”<br>3 · Envie pelo WhatsApp</p>
<div style='margin-top:60px;background:{GOLD};color:{INK};font-weight:700;font-size:34px;letter-spacing:.08em;padding:30px 56px;border-radius:999px'>LINK NA BIO</div></div>""")
cta2 = bg(f"""<div style='position:absolute;left:90px;right:90px;top:470px;text-align:center;display:flex;flex-direction:column;align-items:center'>
<div class='kick'>Para lojistas</div><h1 style='font-size:104px;margin-top:40px'>Condições<br><span class='gold'>especiais</span><br>para revenda</h1>
<p style='font-size:40px;color:#ddd2bb;margin-top:50px'>Fale com nossa especialista<br>WhatsApp (11) 95978-1849</p></div>""")
cta3 = bg(f"""<div style='position:absolute;left:90px;right:90px;top:470px;text-align:center;display:flex;flex-direction:column;align-items:center'>
<img src='{ICONE}' style='width:180px'><h1 style='font-size:100px;margin-top:60px'>Viu um produto<br>que <span class='gold'>amou?</span></h1>
<p style='font-size:40px;color:#ddd2bb;margin-top:50px'>Anote o código <b style='color:{GOLD}'>PROD-XXXX</b><br>e mande para nossa especialista</p>
<p style='font-size:34px;color:#cbbf9f;margin-top:50px'>lumifa.com.br · link na bio</p></div>""")

banco = {'dica': [], 'produto': [], 'cta': []}
with Renderer() as r:
    fr = r.render(frame, '/home/claude/work/_frame.jpg', 1080, 1920)
    F = Image.open(fr)
    # dicas: slides de carrosséis que não vão ao feed nas próximas 2 semanas
    slides = ['d5-09h00-watts-e-lumens-%d' % i for i in (2,3,4)] + ['d6-09h00-irc-%d' % i for i in (2,3,4)] + \
             ['d7-09h00-arandelas-onde-instalar-%d' % i for i in (2,3,4,5)] + ['d6-19h30-erros-de-iluminacao-%d' % i for i in (2,3,4,5)] + \
             ['d5-19h30-lojista-paineis-led-%d' % i for i in (2,3,4)] + ['d7-19h30-fachada-a-noite-%d' % i for i in (2,3)] + ['d4-19h30-quarto-aconchegante-2']
    for s in slides:
        im = Image.open(R/'posts'/'semana-01'/f'{s}.jpg').crop((0, 170, 1080, 1200))
        c = F.copy(); c.paste(im, (0, 450)); out = OUT/f'dica-{s[4:]}.jpg'
        c.save(out, 'JPEG', quality=90, optimize=True); banco['dica'].append(f'{BASE}/{out.name}')
    # dicas dos Reels de dica rápida que ainda não foram ao feed (cenas 1-3)
    for (data, hora, slug, scenes, cap) in RS.R:
        if slug in ('dica-cozinha','dica-home-office','dica-varanda','dica-vitrine'):
            for k in (1,2,3):
                out = r.render(scenes[k][0], OUT/f'dica-{slug}-{k}.jpg', 1080, 1920); banco['dica'].append(f'{BASE}/{out.name}')
    # produtos: cenas de produto dos Reels (sem o número do canto)
    order = ['plafons-arte','trilhos','pendentes-design','fitas-neon','luminarias-mesa','luz-caminho','lampadas-decorativas','spots']
    byslug = {x[2]: x for x in RS.R}
    for slug in order:
        scenes = byslug[slug][3]
        for k in (1,2,3):
            h = re.sub(r"(line-height:1'>)\d(</div>)", r"\1\2", scenes[k][0])
            out = r.render(h, OUT/f'produto-{slug}-{k}.jpg', 1080, 1920); banco['produto'].append(f'{BASE}/{out.name}')
    for i, h in enumerate((cta1, cta2, cta3), 1):
        out = r.render(h, OUT/f'cta-{i}.jpg', 1080, 1920); banco['cta'].append(f'{BASE}/{out.name}')
json.dump(banco, open('/home/claude/work/banco.json','w'), indent=1)
print({k: len(v) for k, v in banco.items()})
