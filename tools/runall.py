import json, re, sys
from multiprocessing import Pool
sys.path.insert(0, '/home/claude/work')
import gen
rel = json.load(open('/home/claude/ml/rel.json'))
cat = {r['codigo']: r for r in json.load(open('/home/claude/ml/ok.json'))}
excl = json.load(open('excluir.json'))
MAN = {'Dour Ado':'Dourado','Dou Rado':'Dourado','Doura Do':'Dourado','P Reto':'Preto','Acr Ílico':'Acrílico','Me Tal':'Metal','Crist Al':'Cristal','Cris Tal':'Cristal','Silic One':'Silicone','Doura do':'Dourado','Dourado Rado':'Dourado','Efeitomade Ira':'Efeito Madeira','Brancoebordaefeito':'Branco e Borda Efeito','Omado':''}
def limpa(n):
    for a, b in MAN.items(): n = n.replace(a, b)
    n = re.sub(r'\s*\(\s*Preço Unit[^)]*\)', '', n); n = re.sub(r'\(\s*([^)]*?)\s*\)', r'\1', n)
    n = n.replace('⌀', 'D').replace('_', ' ').replace('*', 'x')
    return re.sub(r'\s+', ' ', n).strip()
def job(a):
    cod, n = a
    try: return cod, n, gen.gera(cod, limpa(cat[cod]['nome']), n, cat[cod])
    except Exception as e: return cod, n, 'ERRO ' + repr(e)
if __name__ == '__main__':
    jobs = sorted({(r[2], r[7]) for r in rel if r[2] not in excl})
    with Pool(2) as p: res = p.map(job, jobs, chunksize=10)
    json.dump(res, open('gen_res.json', 'w'))
    print(len(res), sum(1 for x in res if isinstance(x[2], str)))
