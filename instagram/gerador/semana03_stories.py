"""Stories novos para 24–30/11/2026: 10 dicas inéditas, 14 produtos inéditos e teasers dos Reels do estoque."""
import json
from layouts import *
from reel import bg
R = REPO/'instagram'
OUT = R/'stories'/'banco'
SB = 'https://www.lumifa.com.br/instagram/stories/banco'

def dica_story(titulo, texto):
    return bg(f"""<img src='{LOGO_DARK}' style='position:absolute;top:250px;left:50%;transform:translateX(-50%);height:66px'>
<div style='position:absolute;top:400px;left:0;right:0;text-align:center'><div class='kick'>Dica LumiFa</div></div>
<div style='position:absolute;left:100px;right:100px;top:620px'>
<div class='rule' style='margin-bottom:56px'></div>
<h1 style='font-size:104px'>{titulo}</h1>
<p style='font-size:46px;color:#ddd2bb;line-height:1.45;margin-top:56px'>{texto}</p></div>
<div style='position:absolute;top:1560px;left:0;right:0;text-align:center'><p style='font-size:32px;color:#cbbf9f;letter-spacing:.04em'>Salve e compartilhe · <b style='color:{GOLD}'>@lumifa.br</b></p></div>""")

def prod_story(code, nome, info):
    return bg(f"""<img src='{LOGO_LIGHT}' style='position:absolute;top:240px;left:90px;height:60px'>
<div class='kick' style='position:absolute;top:262px;right:90px;color:{GOLD2};font-size:20px'>Destaque LumiFa</div>
<div style='position:absolute;left:70px;right:70px;top:380px'>{card(photo(code), 940, 860, pad=50, radius=34).replace('rgba(0,0,0,.35)','rgba(80,60,20,.18)')}</div>
<div style='position:absolute;left:90px;right:90px;top:1290px'><h1 style='font-size:76px;color:{INK}'>{nome}</h1>
<p style='font-size:34px;color:#5a4d38;margin-top:18px'>{info}</p><div style='margin-top:26px'><span class='code'>{code}</span></div></div>
<div style='position:absolute;left:0;right:0;bottom:250px;text-align:center'><span style='display:inline-block;background:{INK};color:{CREAM};font-size:28px;letter-spacing:.04em;padding:24px 44px;border-radius:999px'>Peça seu orçamento · <b style='color:{GOLD}'>fale com nossa especialista</b></span></div>""", cream=True)

DICAS = [
 ('dimmer', f"Dimmer pede LED <span class='gold'>dimerizável</span>", 'Lâmpada LED comum ligada em dimmer pode piscar, zumbir ou queimar antes do tempo. Confira na embalagem se ela é dimerizável.'),
 ('angulo-de-abertura', f"O <span class='gold'>ângulo</span> do spot muda tudo", 'Facho fechado (até cerca de 36°) destaca quadros e objetos. Facho aberto (60° ou mais) espalha a luz e ilumina o ambiente.'),
 ('grau-ip', f"O que é o <span class='gold'>IP</span> da luminária?", 'O 1º número indica a proteção contra poeira e o 2º contra água. Em área externa exposta à chuva, prefira IP65 ou mais.'),
 ('perfil-para-fita', f"Fita de LED pede <span class='gold'>perfil</span>", 'O perfil de alumínio ajuda a dissipar o calor e, com difusor, esconde os pontinhos de LED para uma linha de luz contínua.'),
 ('fita-24v', f"Trecho longo? Fita <span class='gold'>24V</span>", 'Em trechos longos, a fita de 24V sofre menos queda de tensão que a de 12V e mantém o brilho uniforme do início ao fim.'),
 ('luz-ambar', f"O charme da <span class='gold'>luz âmbar</span>", 'Lâmpadas de filamento entre 2200K e 2700K têm brilho dourado, perfeitas para pendentes de vidro e ambientes de convivência.'),
 ('luz-atras-da-tv', f"Uma luz <span class='gold'>atrás da TV</span>", 'Uma luz suave atrás da TV diminui o contraste entre a tela e a parede escura e deixa a visão mais confortável.'),
 ('lux-por-ambiente', f"Quanta luz cada <span class='gold'>ambiente</span> pede", 'A medida é o lux: salas ficam bem com 150 a 300 lux; bancadas de cozinha e mesas de trabalho pedem cerca de 500 lux.'),
 ('luminaria-fechada', f"Luminária fechada <span class='gold'>esquenta</span>", 'Nela o calor fica preso. Use lâmpadas LED indicadas para luminária fechada e garanta a vida útil prometida.'),
 ('sensor-de-presenca', f"<span class='gold'>Sensor</span> de presença", 'Em corredores, garagens e áreas de passagem, a luz acende só quando alguém passa: mais praticidade e economia.'),
]
PRODS = [
 ('PROD-3740', 'Pendente Albâtre ⌀100cm', 'Resina com efeito alabastro · LED 3 temperaturas'),
 ('PROD-3753', 'Arandela Cúpula de Tecido', 'Metal + tecido · dourada, preta ou branca'),
 ('PROD-3784', 'Plafon Cristal Dourado 30cm', 'LED 60W · troca de cor pelo interruptor'),
 ('PROD-3768', 'Pendente Sora', 'Vidro leitoso · LED 3 temperaturas'),
 ('PROD-3762', 'Pendente Éther 30', 'Disco de acrílico · LED 3 temperaturas'),
 ('PROD-3788', 'Pendente Éclat ⌀50cm', 'Cristal + metal dourado · 6 lâmpadas E14'),
 ('PROD-3765', 'Pendente Wabi ⌀40cm', 'Metal + resina branca · bocal E27'),
 ('PROD-3800', 'Pendente Vértica 6', 'Metal + silicone LED 3500K · dourado ou preto'),
 ('PROD-3772', 'Pendente Caju Solea ⌀30cm', 'Vidro âmbar · 3 lâmpadas E27'),
 ('PROD-3781', 'Pendente Fluir', 'Feito em impressão 3D · bocal E27'),
 ('PROD-3804', 'Luminária de Chão Escultura', '1,80 m · resina + vidro · 6 lâmpadas E27'),
 ('PROD-3793', 'Lustre Lumière ⌀80cm', 'Cristal + metal dourado · 15 lâmpadas E14'),
 ('PROD-3776', 'Pendente Alba', 'Metal dourado + cerâmica · bocal E27'),
 ('PROD-3791', 'Arandela Lumière', 'Cristal + metal dourado · 2 lâmpadas E14'),
]
TEASERS = ['dica-cozinha', 'plafons-arte', 'trilhos']

if __name__ == '__main__':
    reels = {c['titulo']: c for c in json.load(open(R/'calendario-reels-semana-01.json'))}
    res = {'dica': [], 'produto': [], 'teaser': {}}
    with Renderer() as r:
        for slug, t, x in DICAS:
            out = r.render(dica_story(t, x), OUT/f'dica-{slug}.jpg', 1080, 1920); res['dica'].append(f'{SB}/{out.name}')
        for code, n, info in PRODS:
            out = r.render(prod_story(code, n, info), OUT/f'produto-{code}.jpg', 1080, 1920); res['produto'].append(f'{SB}/{out.name}')
        for slug in TEASERS:
            capa = R/'reels'/'semana-01'/reels[slug]['capa'].split('/')[-1]
            out = r.render(story_post(img(capa), 'Reel novo no feed', 'Dá o play lá no perfil ▶', 'Comenta e compartilha · @lumifa.br'), OUT/f'teaser-reel-{slug}.jpg', 1080, 1920)
            res['teaser'][slug] = f'{SB}/{out.name}'
    json.dump(res, open('/home/claude/work/semana03_stories.json', 'w'), indent=1)
    print({k: len(v) for k, v in res.items()})
