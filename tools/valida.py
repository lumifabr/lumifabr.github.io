import openpyxl, re, collections, sys, json
arq = sys.argv[1]
wb = openpyxl.load_workbook(arq)
ex = wb['extra info']
def lista(ref):
    m = re.match(r"'extra info'!\$([A-Z]+)\$(\d+):\$([A-Z]+)\$(\d+)", ref)
    r = int(m.group(2))
    return [c.value for c in ex[r] if c.value is not None]
imgs = set(l.strip().split('/')[-1] for l in open('/home/claude/ml/imgs.txt'))
PLACE = {'Insira ou selecione um valor', 'Selecionar', None, ''}
erros = collections.Counter(); exemplos = collections.defaultdict(list); total = 0
LIVRE = {'Marca', 'Código universal de produto', 'Varia por: Nome comercial da cor'}   # aceitam texto livre
def err(k, msg):
    erros[k] += 1
    if len(exemplos[k]) < 4: exemplos[k].append(msg)
titulos_global = collections.defaultdict(set)
for ws in wb.worksheets[2:5]:
    H = {}
    for c in range(1, ws.max_column + 1):
        v = ws.cell(3, c).value
        if v: H[c] = (str(v).split('\n')[0].strip(), ws.cell(4, c).value == 'Obrigatório')
    ini = 8 if ws.title == 'Outros' else 9
    dv = {}
    for d in ws.data_validations.dataValidation:
        col = re.match(r'([A-Z]+)', str(d.sqref)).group(1)
        dv[openpyxl.utils.column_index_from_string(col)] = d
    tcol = [c for c, (n, _) in H.items() if n.startswith('Título')][0]
    pcol = [c for c, (n, _) in H.items() if n == 'Preço [R$]'][0]
    fcol = [c for c, (n, _) in H.items() if n == 'Fotos'][0]
    dcol = [c for c, (n, _) in H.items() if n == 'Descrição'][0]
    vcols = [c for c, (n, _) in H.items() if n.startswith('Varia por')]
    grupos = []
    prev = None
    for r in range(ini, ws.max_row + 1):
        t = ws.cell(r, tcol).value
        if not t: continue
        total += 1
        if prev and prev[0] == t: prev[1].append(r)
        else:
            prev = (t, [r]); grupos.append(prev)
        if len(t) > 60: err('titulo>60', f'{ws.title}!{r}')
        for c, (n, obrig) in H.items():
            v = ws.cell(r, c).value
            if n in ('BUYBOX_FORMULA', 'HIDDEN_PICTURES', 'Quantidade de caracteres', 'Tarifa de venda'): continue
            if obrig and (v in PLACE):
                if n == 'Fotos': pass
                err('obrigatorio vazio: ' + ws.title + ' / ' + n, f'{r}')
            if v in PLACE or (isinstance(v, str) and v.startswith('=')): continue
            d = dv.get(c)
            if d is not None:
                if d.type == 'list' and n not in LIVRE:
                    if v not in lista(d.formula1): err(f'fora da lista: {ws.title} / {n}', f'{r}: {v!r}')
                elif d.type == 'decimal':
                    if not isinstance(v, (int, float)): err(f'nao numerico: {n}', f'{ws.title}!{r}: {v!r}')
                elif d.type == 'textLength':
                    if len(str(v)) > int(float(d.formula1)): err(f'texto longo: {n}', f'{ws.title}!{r}')
        p = ws.cell(r, pcol).value
        if not isinstance(p, (int, float)) or p <= 0 or round(p, 2) != p: err('preco invalido', f'{ws.title}!{r}: {p}')
        f = ws.cell(r, fcol).value or ''
        import os
        FT = set(os.listdir('/home/claude/mlfotos'))
        for u in f.split(','):
            if not (re.fullmatch(r'https://raw\.githubusercontent\.com/lumifabr/lumifabr\.github\.io/ml-fotos/PROD-[\w-]+\.jpg', u) and u.split('/')[-1] in FT): err('foto invalida', f'{ws.title}!{r}: {u}')
        dsc = ws.cell(r, dcol).value or ''
        if re.search(r'https?://|www\.|@|\(\d{2}\)\s?\d|whats', dsc, re.I): err('descricao com contato/link', f'{ws.title}!{r}')
        if re.search('[\U0001F300-\U0001FAFF]', dsc): err('emoji', f'{ws.title}!{r}')
        if '<' in dsc and '>' in dsc: err('html?', f'{ws.title}!{r}')
    # grupos (variações)
    for t, rs in grupos:
        titulos_global[t.lower()].add((ws.title, rs[0]))
        if len(rs) > 1:
            ps = {ws.cell(r, pcol).value for r in rs}
            if len(ps) > 1: err('variacao com precos diferentes', f'{ws.title}!{rs}')
            combos = [tuple(ws.cell(r, c).value for c in vcols) for r in rs]
            if len(set(combos)) < len(combos): err('variacao combinacao repetida', f'{ws.title}!{rs}: {combos}')
            skus = [ws.cell(r, [c for c,(n,_) in H.items() if n=='SKU'][0]).value for r in rs]
            if len(set(skus)) < len(skus): err('sku repetido no grupo', f'{ws.title}!{rs}')
for t, locs in titulos_global.items():
    if len(locs) > 1: err('titulo repetido em grupos diferentes', f'{t} {sorted(locs)[:3]}')
print('linhas preenchidas:', total)
print('ERROS:', sum(erros.values()))
for k, v in erros.most_common(): print(f'  {v:5d}  {k}   ex: {exemplos[k]}')
