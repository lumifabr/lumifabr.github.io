import json, re, math, collections, unicodedata, copy, sys
import openpyxl
from openpyxl.utils import column_index_from_string as cidx

DESCONTO = 0.05          # 5% abaixo do preço do catálogo
KIT_MIN = 20.0           # itens abaixo disso viram kit
KIT_ALVO = 40.0          # valor mínimo aproximado do kit
ESTOQUE = 5
BASE_IMG = 'https://lumifabr.github.io/imagens/'

rows = json.load(open('ok.json'))
TAB = json.load(open('/home/claude/ml4/tabela.json'))  # preço do PDF (preco_tabela); ML = 2x (100% de lucro)
PULA = {f'PROD-{n}' for n in list(range(1195,1206))+list(range(1215,1221))+[3464]}
FALTA = set(json.load(open('finalizados.json'))) - PULA
GRANDES = {'PROD-2097','PROD-3220','PROD-2091','PROD-2110','PROD-2105','PROD-2092','PROD-2115','PROD-2118','PROD-2114','PROD-3219','PROD-2104','PROD-2098','PROD-2117','PROD-2109'}  # >=2m: nao cabem no Mercado Envios
FALTA -= GRANDES
rows = [r for r in rows if r['codigo'] in FALTA]
import os
FOTOS = set(os.listdir('/home/claude/mlfotos'))
RAW = 'https://raw.githubusercontent.com/lumifabr/lumifabr.github.io/ml-fotos/'
def fotos_de(cod, n):
    suf = f'-K{n}' if n > 1 else ''
    out = []
    for nm in (f'{cod}{suf}-1.jpg', f'{cod}-1.jpg'):
        if nm in FOTOS: out.append(nm); break
    for k in ('3', '4'):
        for nm in (f'{cod}{suf}-{k}.jpg', f'{cod}-{k}.jpg'):
            if nm in FOTOS and nm not in out: out.append(nm); break
    return ','.join(RAW + x for x in out) if out else 'https://lumifabr.github.io/imagens/' + cod + '.jpg'
var = json.load(open('/home/claude/ml3/repo/variacoes.json'))

# ---------- conserto de palavras quebradas (mesma lógica do site) ----------
words = collections.Counter()
for r in rows:
    for w in re.findall(r"[A-Za-zÀ-ú]+", r['nome']): words[w.lower()] += 1
def fix_text(s):
    parts = s.split(' '); out = []; i = 0
    while i < len(parts):
        a = parts[i]
        if i + 1 < len(parts):
            b = parts[i+1]
            if re.fullmatch(r"[A-Za-zÀ-ú]{1,4}", a) and re.fullmatch(r"[A-Za-zÀ-ú]{2,}", b):
                j = (a+b).lower()
                if j not in ('mm','cm') and words[j] >= 2 and words[b.lower()] <= 3 and a.lower() not in ('com','para','sem','led'):
                    w = j.upper() if s.isupper() else (j if (a[0].islower() and b[0].islower()) else j[0].upper()+j[1:])
                    out.append(w); i += 2; continue
        out.append(a); i += 1
    return ' '.join(out)
MANUAL = {'Acr Ílico':'Acrílico','Me Tal':'Metal','LED p Reto':'LED Preto','Dou Rado':'Dourado','Dour Ado':'Dourado','Doura Do':'Dourado','P Reto':'Preto'}
def fix_all(s):
    for a,b in MANUAL.items():
        s = s.replace(a,b).replace(a.upper(),b.upper())
    return fix_text(s)
def limpa(n):
    n = re.sub(r'\s*\(\s*Preço Unit[^)]*\)', '', n)
    n = re.sub(r'\(\s*([^)]*?)\s*\)', r'\1', n)
    n = n.replace('⌀', 'D').replace('Ø', 'D').replace('_', ' ').replace('"', '').replace('*', 'x')
    return re.sub(r'\s+', ' ', n).strip()
for r in rows:
    for f in ('nome','especificacoes','descricao'): r[f] = re.sub(r'\s+',' ',fix_all(r.get(f,'') or '')).strip()
    m = re.search(r'Pack (\d+)', r['nome'])
    r['pack'] = int(m.group(1)) if m else 1
    r['nome'] = limpa(r['nome'])

def na(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')

# ---------- cor ----------
COR = {'preto':'Preto','preta':'Preto','branca':'Branco','dourada':'Dourado','cromada':'Cromado','prateada':'Prata','black':'Preto','branco':'Branco','white':'Branco','dourado':'Dourado','ouro':'Dourado','gold':'Dourado',
 'cobre':'Cobre','cromado':'Cromado','champagne':'Champagne','champanhe':'Champagne','bronze':'Bronze','grafite':'Grafite',
 'cinza':'Cinza','prata':'Prata','prateado':'Prata','rose gold':'Rose Gold','rosegold':'Rose Gold','rose':'Rosé','nude':'Nude','marrom':'Marrom','bege':'Bege',
 'fendi':'Fendi','verde':'Verde','azul':'Azul','vermelho':'Vermelho','amarelo':'Amarelo','amarela':'Amarelo','rosa':'Rosa','laranja':'Laranja',
 'transparente':'Transparente','fume':'Fumê','ambar':'Âmbar','corten':'Corten','inox':'Inox','niquel':'Níquel','titanio':'Titânio','areia':'Areia','off white':'Off White','creme':'Creme','sisal':'Sisal','efeito madeira':'Efeito Madeira','madeira':'Madeira'}
LUZ = r'branco (quente|frio|neutro)|luz (quente|fria|neutra|amarela|branca|natural|dia|verde|azul|vermelha|rgb)|branca (quente|fria|neutra)'
def cor_de(texto):
    t = re.sub(LUZ, ' ', na(texto)); t = re.sub(r'\bbc\b', 'branco', t); t = re.sub(r'\bpt\b', 'preto', t)
    found = []
    for k in sorted(COR, key=len, reverse=True):
        for m in re.finditer(r'(?<![a-z])'+re.escape(k)+r'(?![a-z])', t):
            if not any(m.start() < e and s < m.end() for s,e,_ in found): found.append((m.start(), m.end(), k))
    found.sort(); lab = []
    for _,_,k in found:
        if COR[k] not in lab: lab.append(COR[k])
    return '/'.join(lab[:2])

# ---------- atributos técnicos ----------
def campo(r, nome):
    m = re.search(nome + r':\s*([^|]+)', r['especificacoes'])
    return m.group(1).strip() if m else ''
def temps(r):
    t = na(r['nome'] + ' | ' + campo(r, 'Temperatura de cor'))
    ks = sorted(set(int(x) for x in re.findall(r'(?<!\d)(\d{4})\s?k\b', t)))
    rgb = bool(re.search(r'\brgbw?\b', t))
    return ks, rgb
def potencia(r):
    p = campo(r, 'Potência')
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*W\b', p) or re.search(r'(?<![\d.,])(\d+(?:[.,]\d+)?)\s?W\b', r['nome'])
    if not m: return None
    v = float(m.group(1).replace(',', '.'))
    return v if 0 < v < 5000 else None
def fluxo(r):
    m = re.search(r'(\d+)\s*lm', campo(r, 'Fluxo').replace('.', ''), re.I)
    return int(m.group(1)) if m else None
def tensao(r):
    t = na(campo(r, 'Tensão') + ' ' + r['nome'])
    if re.search(r'bivolt|127\s*/\s*220|127v\s*/\s*220|127-220|110\s*/\s*220|100-240|85-265', t): return '127/220V'
    for v in ('220','127','48','24','12','5'):
        if re.search(r'(?<!\d)'+v+r'\s?v\b', t): return {'127':'127V','220':'220V'}.get(v, v+'V')
    return ''
def luz_cat(k):
    if k <= 3500: return 'Branco-quente'
    if k < 5000: return 'Branco-neutro'
    return 'Branco-frio'
def led_integrado(r):
    t = na(r['nome'] + ' ' + r['especificacoes'])
    if re.search(r'\b(e27|e14|gu10|g9|gu5\.?3|mr16|mr11|par20|par30|ar70|ar111|bocal|soquete|s/lampada)\b', t) and not re.search(r'led integrado', t):
        return False
    return 'led' in t or bool(re.search(r'potencia:\s*\d', t)) or bool(re.search(r'\d\s*lm\b', t))
def material(r):
    t = na(campo(r, 'Material') + ' ' + r['nome'])
    for k,v in [('acril','Acrílico'),('cristal','Vidro'),('vidro','Vidro'),('glass','Vidro'),('aluminio','Alumínio'),('inox','Aço inoxidável'),
                ('bambu','Bambu'),('ceramica','Cerâmica'),('ferro','Ferro'),('madeira','Madeira'),('rattan','Rotim'),('rotim','Rotim'),('corda','Tecido'),('tecido','Tecido'),('linho','Tecido'),
                ('silicone','Plástico'),('plastico','Plástico'),('policarbonato','Plástico'),('pvc','Plástico'),('abs','Plástico'),('resina','Plástico'),('metal','Metal')]:
        if k in t: return v
    return 'Metal'
def soquete(r):
    t = na(campo(r, 'Base') + ' ' + r['nome'])
    for k,v in [('gu10','GU10'),('gu5.3','GU5.3'),('gu5,3','GU5.3'),('e27','E27'),('e14','E14'),('e40','E40'),('g9','G9'),('g4','G4'),('r7s','R7s'),('b22','B22d'),('gx53','GX53'),
                ('t8','G13'),('g13','G13'),('t5','G5'),('mr16','GU5.3')]:
        if re.search(r'(?<![a-z0-9])'+re.escape(k)+r'(?![0-9])', t): return v
    if re.search(r'\bpar(20|30|38)\b|balloon', t): return 'E27'
    return ''
def forma(r):
    t = na(r['nome'])
    for k,v in [('balloon','Balão'),('vela','Vela'),('tubular','Tubular'),(r'\bt[58]\b','Tubular'),('linear','Linear'),('r7s','Linear'),('espiral','Espiral'),
                ('dicroica','Dicroica'),('mr1','Dicroica'),(r'\bpar\d','Dicroica'),(r'\bar\d','Dicroica'),(r'\bg9\b','Cápsula'),(r'\bg4\b','Cápsula'),('bipino','Cápsula'),('halopim','Cápsula')]:
        if re.search(k, t): return v
    return 'Bulbo'
def ean(r):
    m = re.search(r'EAN:?\s*(\d{8,14})', r.get('ean_ncm','') or '')
    if not m: return ''
    e = m.group(1)
    if len(e) == 13:
        s = sum(int(d)*(1 if i%2==0 else 3) for i,d in enumerate(e[:12]))
        if (10 - s%10) % 10 != int(e[12]): return ''
    return e

# ---------- aba de destino ----------
def aba(r):
    k = int(r['codigo'].split('-')[1])
    if 1206 <= k <= 1208 or 3696 <= k <= 3716: return 'Fita de LED'
    if 1371 <= k <= 1385 or k in (2366, 2367) or 2579 <= k <= 2597: return 'Luminárias de Piso'
    if 2090 <= k <= 2143 or 3108 <= k <= 3111 or 3207 <= k <= 3226: return 'Luminárias de Teto'
    raise Exception(r['codigo'])
def aba_old(r):
    n = na(r['nome']); c = r['categoria']
    if c == 'Ventiladores' or n.startswith('ventilador'): return None
    if n.startswith('arandela'): return 'Arandelas'
    if re.match(r'(refletor|relfetor|projetor)', n): return 'Refletores'
    if c == 'Abajures & Mesa' or re.search(r'\babaju', n): return 'Luminárias de Mesa'
    if c == 'Lâmpadas & Filamentos':
        if soquete(r) and not re.search(r'soquete|driver|fonte|reator|adaptador|bocal', n): return 'Lâmpadas'
        return 'Outros'
    if c in ('Pendentes','Lustres','Plafons'): return 'Luminárias de Teto'
    if c == 'Painéis de LED': return 'Outros' if re.search(r'^(drive|driver|fonte)', n) else 'Luminárias de Teto'
    if c == 'Spots':
        if re.match(r'(spot|mini spot|tiny spot|luminaria de|luminaria led|luminaria decorativa)', n) and 'publica' not in n: return 'Luminárias de Teto'
        return 'Outros'
    if c == 'Trilhos & Acessórios' and re.match(r'(spot para trilho|luminaria spot)', n): return 'Luminárias de Teto'
    return 'Outros'

# ---------- preço ----------
def num(p): return float(str(p).replace('R$','').replace('.','').replace(',','.')) if re.search(r',', str(p)) else float(p)
def preco_ml(v):
    alvo = v * (1 - DESCONTO)
    psic = math.floor(alvo) - 0.10
    if psic >= v * (1 - DESCONTO - 0.03) and psic > 0: return round(psic, 2)
    return round(alvo, 2)
def kit_n(unit):
    if unit >= KIT_MIN: return 1
    for n in (2,3,4,5,6,10):
        if n*unit >= KIT_ALVO: return n
    return 10

# ---------- título ----------
SUBS = [(r'p(?:ara|/) Lamp(?:ada)? Mini Dicroica (MR11),? Base (\w+)', r'\1 \2'),
        (r'p(?:ara|/) (\d) Lâmpadas (?:Dicroica )?(\w+),? Base (\w+)', r'\1x \2 \3'),
        (r'p(?:ara|/) Lâmpada (?:Dicroica )?(\w+),? Base (\w+)', r'\1 \2'),
        (r'\b(127V?\s*/\s*220V|127-220V|110V?\s*/\s*220V|127/220v|127V/220V)\b', 'Bivolt'),
        (r',?\s*com LED Integrado,?', ' LED'), (r'\bTam(?:anho)?:\s*', ''), (r'\bLargura\b', 'Larg'), (r'\bInterno até\b', 'Int'), (r'\bConexão\b', 'Conex'), (r'\bLuminária de LED\b', 'Luminária LED'),
        (r'\s*-\s*Pot\.? Max\.?\s*', ' Até '), (r'\bPot\.? Max\.?\s*', 'Até '), (r'\bpara\b', 'p/'),
        (r'\bDimerizável\b', 'Dimerizável'), (r'\s*-\s*', ' '), (r'\s*,\s*', ' '),
        (r'\(Caixa com (\d+)\s*Pcs\)', r'Cx \1un'), (r'\s+', ' ')]
FIM_RUIM = {'de','da','do','p/','com','e','para','-','em','no','na','sem','a','o','/'}
def encurta(t, lim):
    if len(t) <= lim: return t
    for pat, rep in SUBS:
        t = re.sub(pat, rep, t, flags=re.I).strip()
        if len(t) <= lim: return t
    STOP = {'de','da','do','das','dos','com','e','para','p/','em'}
    ws = t.split(' ')
    while len(' '.join(ws)) > lim:
        idx = [i for i, w in enumerate(ws) if i > 0 and w.lower() in STOP]
        if not idx: break
        ws.pop(idx[0])
    t = ' '.join(ws)
    if len(t) > lim and ' Bivolt' in t: t = t.replace(' Bivolt', '', 1)
    if len(t) <= lim: return t
    ws = t.split(' '); out = ''
    for w in ws:
        if len((out + ' ' + w).strip()) > lim: break
        out = (out + ' ' + w).strip()
    while out.split(' ')[-1].lower() in FIM_RUIM: out = ' '.join(out.split(' ')[:-1])
    return out.strip(' ,-/')
def prefixo(nome, n):
    if n <= 1: return ''
    return f'Pack {n} ' if nome.lower().startswith('kit') else f'Kit {n} '
def titulo(nome, n):
    pre = prefixo(nome, n)
    return pre + encurta(nome, 60 - len(pre))

# ---------- descrição ----------
def descricao(r, n, opcoes=None):
    nome = r['nome']
    d = re.split(r'\s*Tags:', r['descricao'])[0].strip()
    d = re.sub(r'\s*Imagem meramente ilustrativa\.?', '', d).strip()
    d = re.sub(r'https?://\S+|www\.\S+', '', d)
    partes = [p.strip() for p in r['especificacoes'].split('|')[1:] if p.strip() and ':' in p and p.split(':',1)[1].strip()]
    L = [nome, '']
    if n > 1: L += [f'ESTE ANÚNCIO É UM KIT COM {n} UNIDADES.', '']
    if d and d.lower() != nome.lower(): L += [d, '']
    if partes:
        L += ['Especificações:'] + ['- ' + p for p in partes] + ['']
    if opcoes: L += ['Opções disponíveis neste anúncio: ' + ', '.join(opcoes) + '.', '']
    L += ['Produto novo, enviado com nota fiscal.', 'Imagem meramente ilustrativa.']
    return '\n'.join(L).strip()

# ---------- modelo ----------
def modelo(nome):
    w = nome.split(' ')
    m = ' '.join(w[1:]) if len(w) > 2 else nome
    return encurta(m, 60)

# ---------- monta itens ----------
itens = []
for r in rows:
    tab = aba(r)
    if tab is None: continue
    unit = num(r['preco'])
    n = kit_n(unit)
    if r['pack'] > 1: n = max(n, r['pack'])
    ks, rgb = temps(r)
    it = dict(r=r, cod=r['codigo'], tab=tab, unit=unit, n=n, preco=round(2*TAB[r['codigo']]*n,2), cor=cor_de(r['nome']) or cor_de(campo(r,'Acabamento')),
              ks=ks, rgb=rgb, pot=potencia(r), lm=fluxo(r), v=tensao(r), led=led_integrado(r), mat=material(r), soq=soquete(r), ean=ean(r))
    if not it['cor'] and r['parceira'] == 'Luminatti' and tab in ('Luminárias de Teto','Arandelas') and re.match(r'(spot|mini spot|downlight|luminaria|tiny)', na(r['nome'])):
        it['cor'] = 'Branco'
    itens.append(it)
by = {i['cod']: i for i in itens}

# ---------- variações ----------
MAPCOR = {'Cromado':'Prateado','Prata':'Prateado','Inox':'Prateado','Níquel':'Prateado','Titânio':'Cinza','Rose Gold':'Rosa','Rosé':'Rosa','Areia':'Bege','Champagne':'Dourado',
          'Grafite':'Cinza-escuro','Cobre':'Marrom','Bronze':'Marrom','Fendi':'Bege','Off White':'Branco','Corten':'Marrom','Fumê':'Cinza','Âmbar':'Laranja','Efeito Madeira':'Marrom','Madeira':'Marrom','Sisal':'Bege','Transparente':'Branco'}
LISTA_COR = set(c.value for c in openpyxl.load_workbook('/home/claude/ml3/in/base.xlsx')['extra info'][13] if c.value)
def cor_lista(cor):
    if not cor: return ''
    c = cor.split('/')[0]
    c = MAPCOR.get(c, c)
    return c if c in LISTA_COR else ''
def eixo(it, tab):
    """valores de variação suportados por aba: (cor, luz)"""
    luz = 'RGB' if it['rgb'] else (luz_cat(it['ks'][0]) if len(it['ks']) == 1 else '')
    cor = cor_lista(it['cor']) if tab in ('Luminárias de Mesa', 'Refletores') else it['cor']
    return cor, luz
SUP = {'Luminárias de Teto': ('cor',), 'Arandelas': ('cor',), 'Lâmpadas': ('luz',), 'Refletores': ('cor','luz'), 'Luminárias de Mesa': ('cor',), 'Outros': (), 'Fita de LED': (), 'Luminárias de Piso': ()}
grupos = collections.defaultdict(list)
for cod,(gid,cor,temp) in var['itens'].items():
    if cod in by: grupos[gid].append(cod)
var_de = {}
for gid, cods in grupos.items():
    sub = collections.defaultdict(list)
    for c in cods: sub[(by[c]['tab'], by[c]['preco'], by[c]['n'])].append(c)
    for (tab, p, n), cs in sub.items():
        if len(cs) < 2: continue
        vals = {c: eixo(by[c], tab) for c in cs}
        sup = SUP[tab]
        cores = {v[0] for v in vals.values()}; luzes = {v[1] for v in vals.values()}
        varia_cor = len(cores) > 1; varia_luz = len(luzes) > 1
        if (varia_cor and 'cor' not in sup) or (varia_luz and 'luz' not in sup): continue
        if not varia_cor and not varia_luz: continue
        if (varia_cor and '' in cores) or (varia_luz and '' in luzes): continue
        combos = collections.Counter(vals.values())
        if any(x > 1 for x in combos.values()): continue
        # temperatura exata diferente mas mesma faixa de luz -> já barrado pelo combos
        nomeg = limpa(fix_all(var['grupos'][gid]))
        chave = f'{gid}-{tab}-{p}'
        for c in cs: var_de[c] = (chave, nomeg)

# ---------- linhas por aba ----------
ordem = collections.defaultdict(list)
vistos = set()
for it in itens:
    if it['cod'] in vistos: continue
    if it['cod'] in var_de:
        key = var_de[it['cod']][0]
        membros = [x for x in itens if var_de.get(x['cod'], (None,))[0] == key]
        for x in membros: vistos.add(x['cod'])
        ordem[it['tab']].append(('V', var_de[it['cod']][1], membros))
    else:
        vistos.add(it['cod'])
        ordem[it['tab']].append(('S', it['r']['nome'], [it]))

# títulos únicos (por aba e global)
def toks(t): return [w for w in re.split(r'[\s,]+', t) if w]
todos = []
for tab, L in ordem.items():
    for k, (tp, nome, mem) in enumerate(L):
        todos.append([tab, k, nome, mem, titulo(nome, mem[0]['n'])])
def feats(it):
    r = it['r']; f = {}
    f['temp'] = 'RGB' if it['rgb'] else ('/'.join(f'{k}K' for k in it['ks']) if it['ks'] else '')
    f['pot'] = (('%g' % it['pot']).replace('.', ',') + 'W') if it['pot'] else ''
    f['v'] = {'127/220V': 'Bivolt'}.get(it['v'], it['v'])
    f['cor'] = it['cor'].replace('/', ' ')
    c = campo(r, 'Cabo'); f['cabo'] = ('Cabo ' + c) if c else ''
    f['dim'] = campo(r, 'Dimensões')
    m = re.search(r'Tam(?:anho)?:?\s*([\d,]+\s?(?:m|metros?)\b)', r['nome'], re.I)
    f['tam'] = m.group(1).replace(' ', '').replace('metros', 'm').replace('metro', 'm') if m else ''
    f['raw'] = r['especificacoes'].split('|')[0].strip()
    return f
def resolve(xs):
    nomes = [x[2] for x in xs]
    tk = [toks(n) for n in nomes]
    com = set.intersection(*[set(t) for t in tk])
    difs = [' '.join(w for w in t if w not in com).strip(' ,-') for t in tk]
    if all(difs) and len(set(d.lower() for d in difs)) == len(difs) and max(len(d) for d in difs) <= 30:
        for x, t, d in zip(xs, tk, difs):
            pre = prefixo(x[2], x[3][0]['n'])
            base = ' '.join(w for w in t if w in com)
            x[4] = pre + (encurta(base, 60 - len(pre) - len(d) - 1) + ' ' + d).strip()
        return
    fs = [feats(x[3][0]) for x in xs]
    difere = [k for k in ('temp','pot','v','cor','tam','cabo','dim') if len({f[k] for f in fs}) > 1]
    if not difere and len({f['raw'] for f in fs}) > 1:
        tr = [set(re.split(r'[\s,*/]+', f['raw'])) for f in fs]
        c2 = set.intersection(*tr)
        for f in fs:
            f['rawd'] = ' '.join(w for w in re.split(r'[\s,*/]+', f['raw']) if w and w not in c2)[:22].title()
        difere = ['rawd']
    for x, f, d in zip(xs, fs, difs):
        partes = [f[k] for k in difere if f.get(k) and f[k].lower() not in x[4].lower()]
        if d and len(d) <= 30 and d.lower() not in x[4].lower(): partes = [d] + [p for p in partes if p.lower() not in d.lower()]
        suf = ' '.join(partes).strip()
        if not suf: continue
        pre = prefixo(x[2], x[3][0]['n'])
        nome = x[2]
        for p in partes:
            nome = re.sub(r'\s*' + re.escape(p) + r'\b', '', nome, flags=re.I)
        x[4] = pre + (encurta(nome, 60 - len(pre) - len(suf) - 1) + ' ' + suf).strip()
for rodada in range(8):
    col = collections.defaultdict(list)
    for x in todos: col[x[4].lower()].append(x)
    dup = [xs for xs in col.values() if len(xs) > 1]
    if not dup: break
    for xs in dup: resolve(xs)
# último recurso: referência
cnt = collections.Counter(x[4].lower() for x in todos)
for x in todos:
    if cnt[x[4].lower()] > 1:
        pre = prefixo(x[2], x[3][0]['n'])
        ref = 'Ref ' + x[3][0]['cod'].split('-')[1]
        x[4] = pre + encurta(x[2], 60 - len(pre) - len(ref) - 1) + ' ' + ref
for tab, k, nome, mem, t in todos:
    tp = ordem[tab][k][0]
    ordem[tab][k] = (tp, nome, mem, t)
for x in todos:
    tab, k, nome, mem, t = x
    if ordem[tab][k][0] == 'V' and t != titulo(nome, mem[0]['n']):
        cs = []
        for m in mem:
            for c in (m['cor'] or '').split('/'):
                if c and c not in cs: cs.append(c)
        if cs:
            sfx = '/'.join(cs)
            pre = prefixo(nome, mem[0]['n'])
            x[4] = pre + encurta(nome, 60 - len(pre) - len(sfx) - 1) + ' ' + sfx
for tab, k, nome, mem, t in todos:
    ordem[tab][k] = (ordem[tab][k][0], nome, mem, t)
assert len({x[4].lower() for x in todos}) == len(todos), 'titulos duplicados'

json.dump({'ordem': {t: [(tp, nome, [m['cod'] for m in mem], tt) for tp, nome, mem, tt in L] for t, L in ordem.items()}}, open('plano.json','w'), ensure_ascii=False, indent=0)

# ---------- escreve planilha ----------
import os
wb = openpyxl.load_workbook(os.environ.get('TPL','in/tpl.xlsx'))
INI = {'Outros': 8}
def hdr(ws):
    return {str(ws.cell(3, c).value).split('\n')[0].strip(): c for c in range(1, ws.max_column + 1) if ws.cell(3, c).value}
def garante_linha(ws, row, ini):
    if ws.cell(row, 3).value is not None or row <= 1001: return
    for c in range(1, ws.max_column + 1):
        src = ws.cell(ini, c); dst = ws.cell(row, c)
        if src.value is not None: dst.value = src.value
        if src.has_style: dst._style = copy.copy(src._style)
LUGAR = {'Arandelas': 'Parede', 'Luminárias de Teto': 'Teto'}
stats = collections.Counter(); rel = []
for tab, L in ordem.items():
    if tab not in wb.sheetnames: continue
    ws = wb[tab]; H = hdr(ws); ini = INI.get(tab, 9); row = ini
    def put(col, val):
        if val is None or val == '': return
        ws.cell(row, H[col]).value = val
    TIT = [k for k in H if k.startswith('Título')][0]
    for tp, nome, mem, tt in L:
        opcoes = None
        if tp == 'V':
            opcoes = [ (m['cor'] if SUP[tab] and 'cor' in SUP[tab] and len({x['cor'] for x in mem})>1 else '') + ((' ' if len({x['cor'] for x in mem})>1 and 'cor' in SUP[tab] else '') + (eixo(m,tab)[1] if len({eixo(x,tab)[1] for x in mem})>1 else '')) for m in mem]
            opcoes = [o.strip() for o in opcoes]
        desc = descricao(mem[0]['r'], mem[0]['n'], opcoes)
        for m in mem:
            garante_linha(ws, row, ini)
            r = m['r']; n = m['n']
            if tab in ('Arandelas', 'Luminárias de Teto') and tp == 'S' and cor:
                ws_ = tt.split(' ')
                cw = set(na(x) for x in re.split(r'[/ ]', cor))
                while len(ws_) > 3 and na(ws_[-1]) in cw: ws_.pop()
                tt = ' '.join(ws_)
            put(TIT, tt)
            cod_univ = 'O produto é um kit ou pack' if n > 1 else (m['ean'] or 'O produto não tem código cadastrado')
            if tab == 'Luminárias de Piso': cod_univ = m['ean'] or ''
            put('Código universal de produto', cod_univ)
            put('Fotos', fotos_de(m['cod'], n))
            put('SKU', m['cod'] + (f'-K{n}' if n > 1 else ''))
            put('Estoque', ESTOQUE)
            put('Preço [R$]', m['preco'])
            put('Descrição', desc)
            put('Tipo de anúncio', 'Clássico')
            put('Tipo de garantia', 'Garantia do vendedor'); put('Tempo de garantia', 45); put('Unidade de Tempo de garantia', 'dias')
            put('Marca', 'Generic')
            put('Modelo', modelo(r['nome']))
            cor, luz = eixo(m, tab)
            if 'Formato de venda' in H: put('Formato de venda', 'Kit' if n > 1 else 'Unidade')
            for q in ('Quantidade de luminárias','Quantidade de lâmpadas','Quantidade de refletores'):
                if q in H: put(q, n)
            if tab in ('Arandelas', 'Luminárias de Teto'):
                if not cor: stats['sem cor ' + tab] += 1
                put('Varia por: Nome comercial da cor', cor or 'Conforme Foto')
                put('Varia por: Voltagem', m['v'] if tp == 'V' else '')
                put('Materiais', m['mat'])
                put('Lâmpadas', 'Sim' if m['led'] else 'Não')
                if m['rgb']: put('Cor da luz', 'Multicolor')
                elif len(m['ks']) > 1: put('Cor da luz', 'CCT Ajustável')
                elif m['ks']: put('Cor da luz', luz_cat(m['ks'][0])); put('Temperatura de cor', m['ks'][0]); put('Unidade de Temperatura de cor', 'K')
                if m['pot']: put('Potência', m['pot']); put('Unidade de Potência', 'W')
                if m['led']: put('Tipos de fontes de luz', 'LED')
                put('Tipo de alimentação', 'Corrente doméstica' if m['v'] in ('127/220V','127V','220V','') else '')
                nn = na(r['nome'])
                if tab == 'Luminárias de Teto':
                    if 'plafon' in nn: put('Formato da luminária', 'Plafon')
                    elif re.search(r'lustre|candelabro', nn): put('Formato da luminária', 'Lustre')
                put('Lugares de montagem', LUGAR[tab])
            elif tab == 'Lâmpadas':
                put('Varia por: Voltagem', m['v'] if tp == 'V' else ''); put('Varia por: Cor da luz', luz if tp == 'V' else '')
                put('Tecnologia de iluminação', 'LED'); put('Tipos de soquete', m['soq']); put('Forma', forma(r)); put('Wi-Fi', 'Não')
                if m['pot']: put('Potência', m['pot'])
                if m['lm']: put('Fluxo luminoso', m['lm'])
                if len(m['ks']) == 1: put('Temperatura de cor', m['ks'][0])
                put('Dimerizável', 'Sim' if 'dimeriz' in na(r['nome']) else 'Não')
            elif tab == 'Refletores':
                put('Varia por: Voltagem', m['v'] if tp == 'V' else ''); put('Varia por: Cor da carcaça', cor if tp == 'V' else ''); put('Varia por: Cor da luz', luz if tp == 'V' else '')
                if m['pot']: put('Potência', m['pot']); put('Unidade de Potência', 'W')
                put('Tipo de lâmpada', 'LED')
                ip = re.search(r'IP6[56]|IP44', r['nome'] + ' ' + r['especificacoes'], re.I)
                if ip and ip.group(0).upper() in ('IP66','IP44'): put('Classificação IP', ip.group(0).upper())
                if len(m['ks']) == 1: put('Temperatura de cor', m['ks'][0]); put('Unidade de Temperatura de cor', 'K')
            elif tab == 'Luminárias de Mesa':
                put('Varia por: Cor da estrutura', cor if tp == 'V' else '')
                put('Varia por: Voltagem', m['v'] if tp == 'V' else '')
                put('USB', 'Sim' if 'usb' in na(r['nome']+r['especificacoes']) else 'Não')
                put('Tecnologia de iluminação', 'LED' if m['led'] else '')
                if m['soq'] in ('E27','GU10','G9','E14','GX53'): put('Tipos de soquete', m['soq'])
                elif m['led']: put('Tipos de soquete', 'LED integrado')
            elif tab == 'Fita de LED':
                put('Fonte de alimentação', 'Sim')
                put('Dimerizável', 'Sim' if 'dimeriz' in na(r['nome']) else 'Não')
                put('Controlador de cor', 'Não'); put('Wi-Fi', 'Não')
            elif tab == 'Luminárias de Piso':
                put('Lâmpada', 'Sim' if m['led'] else 'Não')
            elif tab == 'Outros':
                put('Varia por: Voltagem', m['v'] if tp == 'V' else '')
            rel.append([tab, row, m['cod'], r['parceira'], r['categoria'], tt, m['unit'], n, m['preco'], 'variação' if tp == 'V' else 'simples'])
            stats[tab] += 1; row += 1
wb.save(os.environ.get('OUT','out_raw.xlsx'))
json.dump(rel, open('rel.json','w'), ensure_ascii=False)
print(stats); print('total', sum(v for k,v in stats.items() if not k.startswith('sem')))
print('variacoes', sum(1 for x in rel if x[-1]=='variação'), 'kits', sum(1 for x in rel if x[7] > 1))
