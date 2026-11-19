"""Acrescenta 24–30/11/2026 ao agenda.json usando o estoque (posts e Reels) + stories do banco."""
import json, datetime as dt
from pathlib import Path
R = Path('/home/claude/lumifabr.github.io/instagram')
SB = 'https://www.lumifa.com.br/instagram/stories/banco'
S1 = 'https://www.lumifa.com.br/instagram/stories/semana-01'
novos = json.load(open('/home/claude/work/semana03_stories.json'))
calp = json.load(open(R/'calendario-semana-01.json')); calr = json.load(open(R/'calendario-reels-semana-01.json'))
P = {c['titulo']: c for c in calp}; RL = {c['titulo']: c for c in calr}
ag = json.load(open(R/'agenda.json'))
assert max(e['data'] for e in ag) == '2026-11-23'

feed = [('post', 'Inspiração: quarto aconchegante'), ('reel', 'dica-cozinha'), ('post', 'Dica: o que é IRC'), ('reel', 'plafons-arte'),
        ('post', 'Candelabro de Metal Preto com 5 Cúpulas'), ('reel', 'trilhos'), ('post', 'Para lojistas: painéis de LED no mix')]
dicas = [f'{SB}/dica-dica-varanda-3.jpg', f'{SB}/dica-dica-vitrine-1.jpg', f'{SB}/dica-dica-vitrine-2.jpg', f'{SB}/dica-dica-vitrine-3.jpg'] + novos['dica']
produtos = novos['produto']
assert len(dicas) == 14 and len(produtos) == 14
d0 = dt.date(2026, 11, 24)
for i, (tipo, chave) in enumerate(feed):
    d = (d0 + dt.timedelta(days=i)).isoformat()
    if tipo == 'post':
        c = P[chave]; ag.append(dict(data=d, hora='19:00', tipo='post', titulo=chave, imagens=c['imagens'], legenda=c['legenda'], status='programado'))
        teaser = c['story']; c['status'] = f'agendado ({d} 19:00, agenda.json)'
    else:
        c = RL[chave]; ag.append(dict(data=d, hora='19:00', tipo='reel', titulo=chave, video=c['video'], capa=c['capa'], legenda=c['legenda'], status='programado'))
        teaser = novos['teaser'][chave]; c['status'] = f'agendado ({d} 19:00, agenda.json)'
    st = [('08:30', dicas[2*i]), ('10:30', produtos[2*i]), ('12:30', dicas[2*i+1]), ('15:30', produtos[2*i+1]), ('19:30', teaser), ('21:30', f'{SB}/cta-{[3,1,2][i % 3]}.jpg')]
    for h, u in st: ag.append(dict(data=d, hora=h, tipo='story', imagem=u, status='programado'))
json.dump(ag, open(R/'agenda.json', 'w'), ensure_ascii=False, indent=1)
json.dump(calp, open(R/'calendario-semana-01.json', 'w'), ensure_ascii=False, indent=1)
json.dump(calr, open(R/'calendario-reels-semana-01.json', 'w'), ensure_ascii=False, indent=1)
print(len(ag), ag[-1]['data'])
