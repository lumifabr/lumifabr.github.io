import json
from layouts import *
R = REPO/'instagram'
cal = json.load(open(R/'calendario-semana-01.json'))
OUT = R/'stories'/'semana-01'
BASE = 'https://www.lumifa.com.br/instagram/stories/semana-01'
K = {'Dica':'Dica nova no feed','Produto':'Destaque do dia','Inspiração':'Inspiração no feed','Institucional':'Novo no feed','Lojista':'Para lojistas','Boas-vindas':'Chegamos!'}
with Renderer() as r:
    # story de lançamento
    r.render(story_post(img(R/'posts/semana-01/d1-12h30-boas-vindas-2.jpg'), 'Chegamos ao Instagram', 'Bem-vindo à LumiFa ✨', 'Siga @lumifa.br · dicas, inspiração e produtos'), OUT/'lancamento.jpg', 1080, 1920)
    for c in cal:
        if c['dia'] == 1: continue
        first = R/'posts/semana-01'/c['imagens'][0].split('/')[-1]
        t = c['titulo'].split(': ',1)[-1]
        t = t[0].upper()+t[1:]
        sub = 'Valor e detalhes na legenda · veja no feed' if c['tipo']=='Produto' else ('Arraste o post para ver tudo · veja no feed' if len(c['imagens'])>1 else 'Veja no feed · @lumifa.br')
        name = first.stem + '-story.jpg'
        r.render(story_post(img(first), K[c['tipo']], t, sub), OUT/name, 1080, 1920)
        c['story'] = f"{BASE}/{name}"
# novas datas: dia 1 publicado hoje (09/11), dias 2-7 de 10/11 a 15/11
datas = {1:'2026-11-09',2:'2026-11-10',3:'2026-11-11',4:'2026-11-12',5:'2026-11-13',6:'2026-11-14',7:'2026-11-15'}
ids = ['18379830925211919','18119259469790353','18108686375627419']
for i,c in enumerate(cal):
    c['data'] = datas[c['dia']]
    if c['dia']==1:
        c['status']='publicado'; c['media_id']=ids[i]
    else:
        c['status']='programado'
json.dump(cal, open(R/'calendario-semana-01.json','w'), ensure_ascii=False, indent=1)
print('ok')
