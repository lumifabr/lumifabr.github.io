import json, datetime as dt
from layouts import *
R = REPO/'instagram'
banco = json.load(open('/home/claude/work/banco.json'))
cal = {c['titulo']: c for c in json.load(open(R/'calendario-semana-01.json'))}
reels = {c['titulo']: c for c in json.load(open(R/'calendario-reels-semana-01.json'))}
SB = 'https://www.lumifa.com.br/instagram/stories/banco'
extra = []
with Renderer() as r:
    for code, nome in [('PROD-046','Arandela de Leitura Read Signature'),('PROD-287','Painel de LED Redondo Preto 12W'),('PROD-3747','Candelabro Preto 5 Cúpulas'),('PROD-1992','Arandela Metal LED Preto 20W')]:
        f = next(R.glob(f'posts/semana-01/*prod-{code[5:]}.jpg'))
        out = r.render(story_post(img(f), 'Destaque LumiFa', nome, f'{code} · peça seu orçamento · link na bio'), R/'stories'/'banco'/f'produto-{code}.jpg', 1080, 1920)
        extra.append(f'{SB}/{out.name}')
    teasers = {}
    for slug in ['pendentes-led','dica-sala-maior','arandelas-joia','paineis-led','dica-banheiro','lustres','spots']:
        c = reels[slug]; capa = R/'reels'/'semana-01'/c['capa'].split('/')[-1]
        out = r.render(story_post(img(capa), 'Reel novo no feed', 'Dá o play lá no perfil ▶', 'Comenta e compartilha · @lumifa.br'), R/'stories'/'banco'/f'teaser-reel-{slug}.jpg', 1080, 1920)
        teasers[slug] = f'{SB}/{out.name}'
produtos = banco['produto'] + extra
dicas = banco['dica']
feed = [('post','Dica: luz quente, neutra ou fria'),('reel','pendentes-led'),('post','Pendente Acrilux Brisa 42cm Gold'),('reel','dica-sala-maior'),
        ('post','Como pedir seu orçamento'),('reel','arandelas-joia'),('post','Dica: altura certa do pendente'),('reel','paineis-led'),
        ('post','Pendente Silicone D800mm LED'),('reel','dica-banheiro'),('post','Inspiração: a luz da sala de jantar'),('reel','lustres'),
        ('post','Dica: as 3 camadas de luz'),('reel','spots')]
ag = []; d0 = dt.date(2026, 11, 10)
for i, (tipo, chave) in enumerate(feed):
    d = (d0 + dt.timedelta(days=i)).isoformat()
    if tipo == 'post':
        c = cal[chave]; ag.append(dict(data=d, hora='19:00', tipo='post', titulo=chave, imagens=c['imagens'], legenda=c['legenda'], status='programado'))
        teaser = c['story']
    else:
        c = reels[chave]; ag.append(dict(data=d, hora='19:00', tipo='reel', titulo=chave, video=c['video'], capa=c['capa'], legenda=c['legenda'], status='programado'))
        teaser = teasers[chave]
    st = [('08:30', dicas[2*i]), ('10:30', produtos[2*i]), ('12:30', dicas[2*i+1]), ('15:30', produtos[2*i+1]), ('19:30', teaser), ('21:30', banco['cta'][i % 3])]
    for h, u in st: ag.append(dict(data=d, hora=h, tipo='story', imagem=u, status='programado'))
json.dump(ag, open(R/'agenda.json','w'), ensure_ascii=False, indent=1)
print(len(ag), ag[-1]['data'])
