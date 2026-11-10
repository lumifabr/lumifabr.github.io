"""Gera modelos/v2/{a-cinema,b-galeria,c-vitrine}.html a partir do index.html atual.
Rodar de novo sempre que o index mudar: python3 build_v2.py"""
import re, pathlib
SITE = pathlib.Path(__file__).resolve().parents[3]
src = (SITE / 'index.html').read_text()
WA = 'https://wa.me/5511959781849?text='

STRIP = '''
  <section class="v2-strip"><div class="wrap"><ul>
    <li><i class="fa-brands fa-whatsapp"></i><span><b>Orçamento pelo WhatsApp</b>Monte a lista e envie em um clique</span></li>
    <li><i class="fa-solid fa-store"></i><span><b>Condições para lojistas</b>Preços e prazos especiais para CNPJ</span></li>
    <li><i class="fa-solid fa-shield-halved"></i><span><b>Garantia dos fabricantes</b>Produtos de marcas selecionadas</span></li>
    <li><i class="fa-regular fa-lightbulb"></i><span><b>Atendimento consultivo</b>Ajuda para escolher a luz certa</span></li>
  </ul></div></section>'''

STEPS = '''
  <section class="v2-steps wrap" data-reveal>
    <div class="sec-h"><div><span class="eyebrow">Como funciona</span><h2>Do catálogo ao orçamento em 3 passos</h2></div></div>
    <ol>
      <li><b>Escolha no catálogo</b><span>Navegue pelas categorias ou busque pelo código, nome, potência ou temperatura.</span></li>
      <li><b>Monte o seu orçamento</b><span>Adicione os itens com cor, temperatura e quantidade. Tudo fica salvo no seu aparelho.</span></li>
      <li><b>Envie pelo WhatsApp</b><span>Nossa especialista confirma estoque, prazo de entrega e as melhores condições.</span></li>
    </ol>
  </section>'''

LOJISTA = f'''
  <section class="v2-lojista" data-reveal><div class="wrap">
    <div><span class="eyebrow">Para o seu negócio</span>
      <h3>Revenda iluminação com <em>condições de lojista</em></h3>
      <p>Atendemos lojas, arquitetos e instaladores com tabela especial, pedidos montados direto pelo catálogo e acompanhamento do início ao fim.</p>
      <a class="btn-solid" target="_blank" rel="noopener" href="{WA}Ol%C3%A1!%20Tenho%20uma%20loja%20e%20quero%20conhecer%20as%20condi%C3%A7%C3%B5es%20para%20lojistas%20da%20LumiFa."><i class="fa-brands fa-whatsapp"></i> Quero ser lojista LumiFa</a></div>
    <ul>
      <li><i class="fa-solid fa-tags"></i>Tabela e condições especiais para CNPJ</li>
      <li><i class="fa-solid fa-clipboard-list"></i>Pedido pelo catálogo, com códigos e fotos prontos</li>
      <li><i class="fa-solid fa-user-tie"></i>Atendimento direto com a especialista</li>
    </ul>
  </div></section>'''

REELS_LIST = [('reel-01-pendentes', 'Pendentes'), ('semana-01/r04-10-21h00-arandelas-joia', 'Arandelas'), ('semana-01/r07-11-21h00-lustres', 'Lustres'),
              ('semana-01/r10-12-21h00-plafons-arte', 'Plafons'), ('semana-01/r13-13-21h00-pendentes-design', 'Pendentes de design'), ('semana-01/r16-14-21h00-luminarias-mesa', 'Luminárias de mesa')]
REELS = '''
  <section class="sec wrap v2-reels" data-reveal>
    <div class="sec-h"><div><span class="eyebrow">Luz em movimento</span><h2>Veja os produtos em vídeo</h2><p>Os vídeos do nosso Instagram, direto no catálogo.</p></div>
      <div class="arrows"><button onclick="slide('reels',-1)" aria-label="Anteriores"><i class="fa-solid fa-chevron-left"></i></button><button onclick="slide('reels',1)" aria-label="Próximos"><i class="fa-solid fa-chevron-right"></i></button></div></div>
    <div class="rail" id="reels">''' + ''.join(
    f'<a class="v2-reel" href="https://www.instagram.com/lumifa.br/" target="_blank" rel="noopener"><video muted loop playsinline preload="none" poster="img/reel-{r.split("/")[-1]}.jpg" data-src="../../instagram/reels/{r}.mp4"></video><span><i class="fa-brands fa-instagram"></i> {n}</span></a>'
    for r, n in REELS_LIST) + '''</div>
  </section>'''

FOOT = f'''<footer class="v2-foot"><div class="wrap">
    <div class="fgrid">
      <div><a href="{{self}}" class="brand" data-brand data-dark></a><p>Catálogo de iluminação decorativa e LED. Escolha, monte seu orçamento e fale com nossa especialista.</p></div>
      <div><h4>Categorias</h4><button class="lk" data-set-cat="Pendentes">Pendentes</button><button class="lk" data-set-cat="Lustres">Lustres</button><button class="lk" data-set-cat="Arandelas">Arandelas</button><button class="lk" data-set-cat="Painéis de LED">Painéis de LED</button><button class="lk" data-set-cat="Spots">Spots</button></div>
      <div><h4>Atendimento</h4><a href="{WA}Ol%C3%A1!%20Vim%20pelo%20cat%C3%A1logo%20da%20LumiFa." target="_blank" rel="noopener"><i class="fa-brands fa-whatsapp"></i> (11) 95978-1849</a><a href="https://www.instagram.com/lumifa.br/" target="_blank" rel="noopener"><i class="fa-brands fa-instagram"></i> @lumifa.br</a><a href="{WA}Ol%C3%A1!%20Tenho%20uma%20loja%20e%20quero%20conhecer%20as%20condi%C3%A7%C3%B5es%20para%20lojistas." target="_blank" rel="noopener">Seja lojista</a></div>
      <div><h4>Catálogo</h4><button class="lk" data-open-cart>Meu orçamento</button><button class="lk" data-reset>Todos os produtos</button><button class="lk" data-scroll-top>Voltar ao topo</button></div>
    </div>
    <div class="fbase"><span>© <span data-year></span> LumiFa Iluminação. Imagens meramente ilustrativas.</span><span>Valores sujeitos a confirmação de estoque e condições comerciais.</span></div>
  </div></footer>'''

MODELS = {
    'a': dict(file='a-cinema.html', nome='Cinema',
              h1='A luz certa para <em>cada projeto</em>',
              hero_top='<video muted loop playsinline autoplay preload="auto" poster="img/hero-wide.jpg" data-wide="img/hero-wide.mp4" data-tall="img/hero-tall.mp4" aria-hidden="true"></video><button class="v2-vctl" type="button" aria-label="Pausar vídeo"><i class="fa-solid fa-pause"></i></button><a class="v2-scroll" href="#produtos">Role</a>',
              after_hero=STRIP, before_band=STEPS + LOJISTA),
    'b': dict(file='b-galeria.html', nome='Galeria',
              h1='Iluminação com <em>olhar de ateliê</em>',
              hero_top='', after_hero=STRIP + STEPS, before_band=REELS + LOJISTA),
    'c': dict(file='c-vitrine.html', nome='Vitrine',
              h1='Peças que <em>acendem</em> o ambiente',
              hero_top='', after_hero=STRIP, before_band=STEPS + REELS),
}

def build(k, m):
    h = src
    h = h.replace('<html lang="pt-BR" data-skin="atelie">', f'<html lang="pt-BR" data-skin="atelie" data-modelo="{k}">')
    h = re.sub(r'<title>.*?</title>', f'<title>Modelo {k.upper()} · {m["nome"]} (prévia) | LumiFa Iluminação</title>\n  <meta name="robots" content="noindex">', h, count=1)
    h = h.replace('href="imagens/', 'href="../../imagens/')
    h = re.sub(r'(href|src)="assets/', r'\1="../../assets/', h)
    h = h.replace('</style>\n<script>', '</style>\n<link rel="stylesheet" href="v2.css?v=2">\n<script>', 1)
    h = h.replace('<a href="./" class="brand"', f'<a href="{m["file"]}" class="brand"')
    # capa
    h = h.replace('<section class="hero"><div class="wrap hero-in">', f'<section class="hero">{m["hero_top"]}<div class="wrap hero-in">', 1)
    h = re.sub(r'<h1>.*?</h1>', f'<h1>{m["h1"]}</h1>', h, count=1)
    h = h.replace('</div></section>\n\n  <main>', '</div></section>\n' + m['after_hero'] + '\n\n  <main>', 1)
    # seções com entrada suave
    h = h.replace('<section class="sec wrap">', '<section class="sec wrap" data-reveal>')
    # blocos novos antes da faixa de atendimento
    h = h.replace('  <section class="band">', m['before_band'] + '\n\n  <section class="band" data-reveal>', 1)
    # rodapé novo
    h = re.sub(r'<footer>.*?</footer>', FOOT.replace('{self}', m['file']), h, count=1, flags=re.S)
    h = re.sub(r'motor\.js\?v=\w+', 'motor.js?v=20261110a', h)
    h = h.replace("root: './'", "root: '../../', paged: true")
    # botão do card: "Cotar"
    h = h.replace('<i class="fa-solid fa-plus"></i> Orçar</button>', '<i class="fa-solid fa-plus"></i> Cotar</button>')
    # produtos por página + paginação
    h = h.replace('<div class="view">', '<label class="per"><span>Mostrar</span><select data-per aria-label="Produtos por página"><option value="50">50</option><option value="100">100</option><option value="150">150</option><option value="all">Todos</option></select></label>\n            <div class="view">', 1)
    h = h.replace('<div class="more" data-more hidden>', '<nav class="pager" data-pager hidden aria-label="Páginas"></nav>\n        <div class="more" data-more hidden>', 1)
    h = h.replace('</body>', '<script src="v2.js?v=2"></script>\n</body>')
    assert 'data-pager' in h and 'Cotar' in h and 'data-per' in h and 'data-hero-art' in h and "root: '../../'" in h and 'v2.js' in h and 'v2-foot' in h, k
    (SITE / 'modelos/v2' / m['file']).write_text(h)
    print('ok', m['file'], len(h))

for k, m in MODELS.items(): build(k, m)
