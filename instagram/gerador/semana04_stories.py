"""Stories novos para 01–07/12/2026: 14 dicas inéditas, 14 produtos inéditos e teasers dos 4 Reels do estoque."""
import json
from layouts import *
from reel import bg
from semana03_stories import dica_story, prod_story
R = REPO/'instagram'
OUT = R/'stories'/'banco'
SB = 'https://www.lumifa.com.br/instagram/stories/banco'

DICAS = [
 ('bocal-certo', f"Confira o <span class='gold'>bocal</span>", 'E27 é a rosca comum; E14 é a rosca fina de lustres e abajures; GU10 tem dois pinos de encaixe, típico de spots. Veja antes de comprar a lâmpada.'),
 ('quadros-30-graus', f"Luz no <span class='gold'>quadro</span> sem reflexo", 'Mire o spot a cerca de 30° da vertical em direção à obra. Assim a luz valoriza a peça sem refletir no vidro nem fazer sombra da moldura.'),
 ('luz-indireta', f"O poder da luz <span class='gold'>indireta</span>", 'Fita ou perfil na sanca joga a luz no teto e ela volta suave para o ambiente: sem ofuscar e com sensação de pé-direito mais alto.'),
 ('ofuscamento', f"Diga não ao <span class='gold'>ofuscamento</span>", 'Lâmpada aparente na linha dos olhos cansa a vista. Prefira spots recuados, difusores e cúpulas que escondem a fonte de luz.'),
 ('escada', f"Escada <span class='gold'>segura</span> à noite", 'Balizadores na parede ou fita sob os degraus marcam cada passo, ajudam a evitar tropeços e ainda criam um efeito lindo.'),
 ('closet', f"Luz no <span class='gold'>closet</span>", 'Fita de LED nas prateleiras com luz neutra (4000K) mostra as cores reais das roupas. Com sensor, acende ao abrir a porta.'),
 ('jardim-de-baixo-para-cima', f"Jardim iluminado <span class='gold'>de baixo</span>", 'Um espeto mirando a copa da árvore de baixo para cima cria volume, textura e sombras bonitas no muro. Em área externa, use IP65 ou mais.'),
 ('vida-util-led', f"O que significa a <span class='gold'>vida útil</span>", 'As 25.000 h da embalagem indicam, em geral, o tempo até o LED cair para 70% do brilho inicial (L70). Ele não apaga de repente.'),
 ('cor-das-paredes', f"A cor da <span class='gold'>parede</span> conta", 'Paredes e teto claros refletem muito mais luz. Ambientes com cores escuras pedem mais lúmens para ficar com a mesma claridade.'),
 ('espacamento-de-spots', f"Quanto espaço entre os <span class='gold'>spots</span>?", 'Em pé-direito de cerca de 2,60 m, deixe em torno de 1 a 1,5 m entre os spots e uns 50 cm da parede para uma luz uniforme.'),
 ('leitura-na-cama', f"Luz para <span class='gold'>ler na cama</span>", 'A luz deve vir de lado, um pouco acima do ombro. Arandela articulada ou abajur de cúpula na cabeceira evitam sombra no livro.'),
 ('bivolt', f"<span class='gold'>Bivolt</span>, 127V ou 220V?", 'Bivolt funciona em 127V e 220V. Produtos de 12V ou 24V, como fitas e trilhos magnéticos, precisam de fonte (driver) adequada.'),
 ('economia-led', f"Quanto o LED <span class='gold'>economiza</span>", 'Uma lâmpada LED de 9W ilumina como uma incandescente de 60W: cerca de 85% menos energia para a mesma luz.'),
 ('descarte-de-lampadas', f"Descarte <span class='gold'>consciente</span>", 'Lâmpadas fluorescentes contêm mercúrio: não jogue no lixo comum. Leve a um ponto de coleta. Trocar por LED já é um bom começo.'),
]
PRODS = [
 ('PROD-050', 'Pendente Bambu Ninho', 'Trama natural de bambu · 30 x 15 cm · bocal E27'),
 ('PROD-3679', 'Lustre Scribble Linea', 'Traço de luz LED 80W · dourado · 3000K'),
 ('PROD-104', 'Abajur LED Flome', 'Acrílico + rose gold · LED 3 temperaturas'),
 ('PROD-2571', 'Arandela Mezzaluna', 'Área externa · IP65 · branca ou preta'),
 ('PROD-1274', 'Pendente Glass Champagne', 'Vidro rosé · bocal E27'),
 ('PROD-2124', 'Spot Tiny Mag', 'Trilho magnético 24V · 3000K · IRC 90'),
 ('PROD-3672', 'Pendente Pei LED', 'Linear dourado · 48W · 3000K'),
 ('PROD-2385', 'Balizador Glow LED', 'Para escadas e caminhos · IP67 · 3000K'),
 ('PROD-131', 'Arandela Cilindroluxo', 'Preta · LED 12W · 3 temperaturas'),
 ('PROD-2667', 'Perfil Wall Washer', 'Banho de luz na parede · preto · 1 m'),
 ('PROD-2209', 'Spot Hub Micro Borda', 'Recuado duplo · AR70 GU10 · preto ou branco'),
 ('PROD-2538', 'Espeto de Jardim LED', '7W · bivolt · para destacar plantas'),
 ('PROD-2145', 'Módulo Difuso Tiny Mag', 'Trilho magnético 24V · 3000K · IRC 90'),
 ('PROD-2295', 'Downlight Hide Recuado', 'Embutir · LED 18W · 4000K'),
]
TEASERS = ['pendentes-design', 'dica-home-office', 'fitas-neon', 'dica-varanda']

if __name__ == '__main__':
    reels = {c['titulo']: c for c in json.load(open(R/'calendario-reels-semana-01.json'))}
    res = {'dica': [], 'produto': [], 'teaser': {}}
    with Renderer() as r:
        for slug, t, x in DICAS:
            out = r.render(dica_story(t, x), OUT/f'dica-{slug}.jpg', 1080, 1920); res['dica'].append(f'{SB}/{out.name}')
        for code, n, info in PRODS:
            out = r.render(prod_story(code, n, info), OUT/f'produto-{code}.jpg', 1080, 1920); res['produto'].append(f'{SB}/{out.name}')
        for slug in TEASERS:
            capa = R/'reels'/'semana-01'/reels[slug]['capa'].split('/')[-1]
            out = r.render(story_post(img(capa), 'Reel novo no feed', 'Dá o play lá no perfil ▶', 'Comenta e compartilha · @lumifa.br'), OUT/f'teaser-reel-{slug}.jpg', 1080, 1920)
            res['teaser'][slug] = f'{SB}/{out.name}'
    json.dump(res, open('/home/claude/work/semana04_stories.json', 'w'), indent=1)
    print({k: len(v) for k, v in res.items()})
