# Gera "fotos.json" a partir da pasta "galeria/": código do produto -> fotos extras.
# Ex.: galeria/PROD-001-3.webp e galeria/PROD-001-4.webp => {"PROD-001": ["3", "4"]}
# -3 = ficha técnica, -4 = temperaturas de cor. O site mostra na ordem do número.
import os, re, json, sys
pasta = sys.argv[1] if len(sys.argv) > 1 else 'galeria'
saida = sys.argv[2] if len(sys.argv) > 2 else 'fotos.json'
fotos = {}
for f in os.listdir(pasta):
    m = re.match(r'^(PROD-\d+)-(\d+)\.webp$', f, re.I)
    if m: fotos.setdefault(m.group(1).upper(), []).append(m.group(2))
num = lambda c: int(re.search(r'\d+', c).group())
dados = {c: sorted(v, key=int) for c, v in sorted(fotos.items(), key=lambda x: num(x[0]))}
with open(saida, 'w', encoding='utf-8') as fh:
    json.dump(dados, fh, separators=(',', ':'))
print(len(dados), 'produtos com fotos extras')
