"""Acrescenta 01–07/12/2026 ao agenda.json usando o estoque (posts e Reels) + stories novos (semana04_stories.py)."""
import json, re, datetime as dt
from pathlib import Path
R = Path('/home/claude/lumifabr.github.io/instagram')
SB = 'https://www.lumifa.com.br/instagram/stories/banco'
novos = json.load(open('/home/claude/work/semana04_stories.json'))
calp = json.load(open(R/'calendario-semana-01.json')); calr = json.load(open(R/'calendario-reels-semana-01.json'))
P = {c['titulo']: c for c in calp}; RL = {c['titulo']: c for c in calr}
ag = json.load(open(R/'agenda.json'))
assert max(e['data'] for e in ag) == '2026-11-30'

def leg_reel(t):
    # preço no padrão "💰 a partir de R$" e sem hashtags repetidas
    t = re.sub(r'(PROD-\d+) · R\$ ([\d.,]+)', r'\1 · 💰 a partir de R$ \2', t)
    lines = t.split('\n'); last = lines[-1]
    if last.startswith('#'):
        seen = []; [seen.append(h) for h in last.split() if h not in seen]; lines[-1] = ' '.join(seen)
    return '\n'.join(lines)

feed = [('reel', 'pendentes-design'), ('post', 'Inspiração: 4 erros de iluminação'), ('reel', 'dica-home-office'),
        ('post', 'Arandela Leitura Nobre Read Signature'), ('reel', 'fitas-neon'), ('post', 'Inspiração: fachada que se destaca à noite'),
        ('reel', 'dica-varanda')]
dicas, produtos = novos['dica'], novos['produto']
assert len(dicas) == 14 and len(produtos) == 14
d0 = dt.date(2026, 12, 1)
for i, (tipo, chave) in enumerate(feed):
    d = (d0 + dt.timedelta(days=i)).isoformat()
    if tipo == 'post':
        c = P[chave]; ag.append(dict(data=d, hora='19:00', tipo='post', titulo=chave, imagens=c['imagens'], legenda=c['legenda'], status='programado'))
        teaser = c['story']
    else:
        c = RL[chave]; c['legenda'] = leg_reel(c['legenda'])
        ag.append(dict(data=d, hora='19:00', tipo='reel', titulo=chave, video=c['video'], capa=c['capa'], legenda=c['legenda'], status='programado'))
        teaser = novos['teaser'][chave]
    c['status'] = f'agendado ({d} 19:00, agenda.json)'
    st = [('08:30', dicas[2*i]), ('10:30', produtos[2*i]), ('12:30', dicas[2*i+1]), ('15:30', produtos[2*i+1]), ('19:30', teaser), ('21:30', f'{SB}/cta-{[1,2,3][i % 3]}.jpg')]
    for h, u in st: ag.append(dict(data=d, hora=h, tipo='story', imagem=u, status='programado'))
json.dump(ag, open(R/'agenda.json', 'w'), ensure_ascii=False, indent=2)
json.dump(calp, open(R/'calendario-semana-01.json', 'w'), ensure_ascii=False, indent=1)
json.dump(calr, open(R/'calendario-reels-semana-01.json', 'w'), ensure_ascii=False, indent=1)
print(len(ag), ag[-1]['data'])
