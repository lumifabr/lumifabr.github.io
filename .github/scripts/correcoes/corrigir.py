"""Correção de português dos anúncios (nome, especificacoes, descricao).

Uso: python3 corrigir.py <Página1.csv> <saida correcoes.json>
Gera {"PROD-x": {"campo": [valor_atual_na_planilha, valor_corrigido]}}.
O site só aplica a correção enquanto a planilha ainda tem o valor antigo.
"""
import csv, json, re, sys

# palavra errada -> certa (sem acento/erro de digitação). Maiúsculas/minúsculas são preservadas.
PALAVRAS = {
    'alvore': 'árvore', 'arvore': 'árvore', 'arvores': 'árvores',
    'aluminio': 'alumínio', 'alumino': 'alumínio', 'luminaria': 'luminária', 'luminarias': 'luminárias',
    'lumianria': 'luminária', 'acrilico': 'acrílico', 'acrilicos': 'acrílicos', 'lampada': 'lâmpada',
    'lampadas': 'lâmpadas', 'magnetico': 'magnético', 'magneticos': 'magnéticos', 'magnetica': 'magnética',
    'ate': 'até', 'compativel': 'compatível', 'compativeis': 'compatíveis', 'acessorio': 'acessório',
    'acessorios': 'acessórios', 'potencia': 'potência', 'moveis': 'móveis', 'modulo': 'módulo',
    'modulos': 'módulos', 'direcionavel': 'direcionável', 'direcionaveis': 'direcionáveis',
    'fixacao': 'fixação', 'ambar': 'âmbar', 'flexivel': 'flexível', 'dimerizavel': 'dimerizável',
    'dimerizacao': 'dimerização', 'presenca': 'presença', 'balao': 'balão', 'pecas': 'peças',
    'conexao': 'conexão', 'chao': 'chão', 'rodape': 'rodapé', 'tres': 'três', 'cilindrico': 'cilíndrico',
    'juncao': 'junção', 'ceramica': 'cerâmica', 'vertice': 'vértice', 'relogio': 'relógio',
    'cupula': 'cúpula', 'plastico': 'plástico', 'ajustavel': 'ajustável', 'ajustaveis': 'ajustáveis',
    'codigo': 'código', 'codigos': 'códigos', 'geracao': 'geração', 'abracadeira': 'abraçadeira',
    'galaxia': 'galáxia', 'funcoes': 'funções', 'lapis': 'lápis', 'carcaca': 'carcaça',
    'eletrica': 'elétrica', 'eletrico': 'elétrico', 'esperanca': 'esperança', 'armario': 'armário',
    'classica': 'clássica', 'classico': 'clássico', 'piramide': 'pirâmide', 'braco': 'braço',
    'celula': 'célula', 'elegancia': 'elegância', 'circulo': 'círculo', 'aneis': 'anéis',
    'fatima': 'fátima', 'aniversario': 'aniversário', 'ligacao': 'ligação', 'perola': 'pérola',
    'regulavel': 'regulável', 'carregavel': 'carregável', 'recarregavel': 'recarregável',
    'mobilia': 'mobília', 'aurea': 'áurea', 'aureola': 'auréola', 'marmore': 'mármore',
    'vitoria': 'vitória', 'virgula': 'vírgula', 'publica': 'pública', 'publico': 'público',
    'rele': 'relé', 'instalaçao': 'instalação', 'instalacao': 'instalação',
    # erros de digitação
    'abaju': 'abajur', 'arandele': 'arandela', 'ångulo': 'ângulo', 'simpes': 'simples',
    'brranco': 'branco', 'bubbes': 'bubbles', 'balizaror': 'balizador', 'feixeis': 'feixes',
    'fexeis': 'feixes', 'champgne': 'champagne', 'quaduplo': 'quádruplo', 'starwarss': 'starwars',
    'rendondo': 'redondo', 'connecor': 'conector', 'relfetor': 'refletor', 'soquet': 'soquete',
    'parde': 'parede', 'reflatora': 'refletora', 'soberpor': 'sobrepor', 'cordoalho': 'cordoalha',
    'imetro': 'inmetro', 'jlho': 'joelho', 'hast': 'haste', 'enrada': 'entrada', 'luxuo': 'luxo',
    'mni': 'mini',
}

# pedaços de palavra separados por espaço (vieram quebrados da tabela da fábrica)
INTEIRAS = ['dourado', 'metal', 'cristal', 'alumínio', 'acrílico', 'silicone', 'cromado', 'preto',
            'plástico', 'ouro', 'madeira']

def caso(modelo, novo):
    if modelo.isupper() and len(modelo) > 1:
        return novo.upper()
    if modelo[:1].isupper():
        return novo[:1].upper() + novo[1:]
    return novo

def corrigir(t):
    if not t:
        return t
    s = t
    # "Dourado Rado", "Cromado Omado" (sufixo repetido)
    s = re.sub(r'\b([A-Za-zÀ-ÿ]{5,}) ([A-Za-zÀ-ÿ]{3,})\b',
               lambda m: m.group(1) if m.group(1).lower() in INTEIRAS and m.group(1).lower().endswith(m.group(2).lower()) and m.group(1).lower() != m.group(2).lower() else m.group(0), s)
    # junta pedaços: "Dou Rado" -> "Dourado", "acr ílico" -> "acrílico"
    for w in INTEIRAS:
        for i in range(1, len(w)):
            a, b = w[:i], w[i:]
            s = re.sub(r'(?<![A-Za-zÀ-ÿ])(' + re.escape(a) + r') (' + re.escape(b) + r')(?![A-Za-zÀ-ÿ])',
                       lambda m: caso(m.group(1), w), s, flags=re.I)
    s = re.sub(r'\b(\d+) ?Metro S\b', lambda m: m.group(1) + (' METROS' if m.group(0).isupper() else ' Metros'), s, flags=re.I)
    # palavras grudadas
    for errado, certo in (('efeitomade ira', 'efeito madeira'), ('brancoebordaefeito', 'branco e borda efeito')):
        s = re.sub(r'\b' + errado + r'\b', lambda m: (certo.upper() if m.group(0).isupper() else
                   certo.title().replace(' E ', ' e ') if m.group(0)[:1].isupper() else certo), s, flags=re.I)

    def troca(m):
        w = m.group(0)
        n = PALAVRAS.get(w.lower())
        return caso(w, n) if n else w
    s = re.sub(r'[A-Za-zÀ-ÿ]+', troca, s)
    s = re.sub(r'\b(Inmetro|INMETRO|inmetro)\b', lambda m: 'INMETRO' if m.group(0).isupper() else 'Inmetro', s)
    s = re.sub(r'\bRgb\b', 'RGB', s)
    s = re.sub(r'(\d) À (\d)', r'\1 a \2', s)            # "3500K À 6500K"
    s = re.sub(r'\(\s+', '(', s)                          # "( para Lâmpada E27 )"
    s = re.sub(r'\s+\)', ')', s)
    s = re.sub(r'(?<!\.)\.\.(?!\.)', '.', s)               # ".." (nome que já terminava em ponto)
    s = re.sub(r'  +', ' ', s)
    return s

def corrigir_nome(t):
    return corrigir(t).rstrip(' .')

def main(src, out):
    rows = list(csv.DictReader(open(src, encoding='utf-8')))
    res = {}
    for r in rows:
        ch = {}
        for f in ('nome', 'especificacoes', 'descricao'):
            novo = corrigir_nome(r[f]) if f == 'nome' else corrigir(r[f])
            if novo != r[f]:
                ch[f] = [r[f], novo]
        if ch:
            res[r['codigo']] = ch
    # ajustes feitos à mão (ex.: arquivar produto sem foto certa) — {"PROD-x": {"status": ["Ativo", "Arquivado"]}}
    import os
    man = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'manuais.json')
    if os.path.exists(man):
        for code, ch in json.load(open(man, encoding='utf-8')).items():
            res.setdefault(code, {}).update(ch)
    json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(len(res), 'produtos corrigidos')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
