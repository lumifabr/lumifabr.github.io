from layouts import *

TAGS = "#lumifa #iluminacao #iluminacaodecorativa #decoracao #designdeinteriores #arquitetura #luminarias #led"
WPP = "📲 Peça seu orçamento: fale com nossa especialista pelo WhatsApp (11) 95978-1849 ou pelo link na bio → lumifa.com.br"

def temps():
    s = ''.join(f"<div style='text-align:center'><div style='width:150px;height:150px;border-radius:50%;margin:0 auto;background:radial-gradient(circle at 50% 40%, {a} 0%, {b} 72%);box-shadow:0 0 70px {a}'></div><div style='margin-top:22px;font-size:26px;color:#cbbf9f;letter-spacing:.08em'>{t}</div></div>"
                for a, b, t in [('#ffd38a', '#c98a2c', '3000K'), ('#fff6e3', '#cfc4ac', '4000K'), ('#e6f0ff', '#8fa9cf', '6000K')])
    return f"<div style='display:flex;gap:70px;margin-top:70px'>{s}</div>"

def big_icon(svg):
    return f"<div style='width:200px;height:200px;margin-top:60px'>{svg}</div>"

from perfil import ICONS

def P(day, time, tipo, slug, titulo, slides, caption):
    return dict(day=day, time=time, tipo=tipo, slug=slug, titulo=titulo, slides=slides, caption=caption)

posts = []

# ---------------- DIA 1 · boas-vindas (mosaico em 3 partes; postar direita → meio → esquerda)
boas = ("✨ Bem-vindo à LumiFa!\n\nIluminação decorativa e técnica para casas, lojas e projetos: pendentes, lustres, arandelas, spots, painéis de LED, fitas e muito mais.\n\n"
        "Aqui você vai encontrar dicas de iluminação, ideias de decoração com luz e os destaques do nosso catálogo.\n\n" + WPP + "\n\n" + TAGS + " #lojadeiluminacao")
posts.append(P(1, '09:00', 'Boas-vindas', 'boas-vindas-3', 'Mosaico de boas-vindas (parte direita)', ['BANNER:2'], boas))
posts.append(P(1, '12:30', 'Boas-vindas', 'boas-vindas-2', 'Mosaico de boas-vindas (parte do meio)', ['BANNER:1'],
               "💡 Luz que transforma ambientes.\n\nA iluminação certa muda tudo: deixa a casa mais aconchegante, valoriza a decoração e faz qualquer loja vender melhor.\n\nConheça o catálogo completo da LumiFa no link da bio.\n\n" + WPP + "\n\n" + TAGS))
posts.append(P(1, '19:30', 'Boas-vindas', 'boas-vindas-1', 'Mosaico de boas-vindas (parte esquerda)', ['BANNER:0'], boas.replace('✨ Bem-vindo à LumiFa!', '✨ Chegamos ao Instagram! Bem-vindo à LumiFa.')))

# ---------------- DIA 2
n = 5
posts.append(P(2, '09:00', 'Dica', 'temperatura-de-cor', 'Dica: luz quente, neutra ou fria', [
    cover('Dica de iluminação', 'Luz quente, neutra ou fria?', 'O guia rápido para acertar a temperatura de cor em cada ambiente.', n, temps()),
    slide(2, n, '3000K', 'Luz quente', 'Amarelada e aconchegante. Ideal para salas de estar, quartos e varandas: ambientes de descanso.', swatch('#ffd38a', '#c98a2c', '2700K – 3000K')),
    slide(3, n, '4000K', 'Luz neutra', 'Branca e equilibrada, sem cansar a vista. Boa para cozinhas, banheiros, home office e lojas.', swatch('#fff6e3', '#cfc4ac', '4000K')),
    slide(4, n, '6000K', 'Luz fria', 'Branca azulada e de alta claridade. Indicada para garagens, áreas de serviço e espaços técnicos.', swatch('#e6f0ff', '#8fa9cf', '6000K – 6500K')),
    cta(5, n, 'Salve este guia', 'Muitos modelos LumiFa vêm em mais de uma temperatura de cor. Na dúvida, a gente te ajuda a escolher.'),
], "Luz quente, neutra ou fria? 💡\n\nA temperatura de cor (medida em Kelvin, K) muda completamente a sensação de um ambiente:\n\n🟠 3000K – luz quente: aconchego para salas, quartos e varandas\n⚪ 4000K – luz neutra: equilíbrio para cozinhas, banheiros, escritórios e lojas\n🔵 6000K – luz fria: claridade para garagens e áreas de serviço\n\nSalve este post para consultar na hora de comprar! 📌\n\n" + WPP + "\n\n" + TAGS + " #temperaturadecor #dicasdeiluminacao"))

posts.append(P(2, '12:30', 'Produto', 'prod-001', 'Pendente Acrilux Brisa 42cm Gold', [
    produto(dict(code='PROD-001', selo='Destaque', categoria='Pendentes', titulo='Pendente Acrilux Brisa 42cm Gold', chips=['13W', '850 lm', '3000K · 4000K · 6000K', 'Bivolt'], opcoes='Também em 60cm')),
], "Pendente Acrilux Brisa 42cm Gold ✨\n\nLeve como uma pétala, com acabamento dourado e LED integrado. Uma peça de destaque para mesas de jantar, bancadas, salas e halls.\n\n• Potência: 13W · 850 lm\n• Temperatura de cor: 3000K / 4000K / 6000K\n• Bivolt (127/220V)\n• Cabo de 130cm\n• Também disponível em 60cm\n\n🔎 Código LumiFa: PROD-001\n💰 A partir de R$ 543,84\n\n" + WPP + "\n\n" + TAGS + " #pendente #pendentedourado #saladejantar"))

n = 4
posts.append(P(2, '19:30', 'Institucional', 'como-pedir-orcamento', 'Como pedir seu orçamento', [
    cover('Passo a passo', 'Como pedir seu orçamento', 'Simples, rápido e direto com a nossa especialista.', n, big_icon(ICONS['orcamento'])),
    slide(2, n, '01', 'Escolha no site', 'Acesse lumifa.com.br e navegue pelas categorias. Viu algo aqui no Instagram? Busque pelo código PROD-XXXX.'),
    slide(3, n, '02', 'Monte o “Meu Orçamento”', 'Adicione os produtos que você quer, com as cores e temperaturas de luz de cada um.'),
    cta(4, n, 'Envie pelo WhatsApp', 'Nossa especialista responde com valores, prazos e condições para lojistas.'),
], "Como pedir seu orçamento na LumiFa? É bem simples 👇\n\n1️⃣ Acesse lumifa.com.br (link na bio) e escolha os produtos\n2️⃣ Adicione tudo ao “Meu Orçamento”\n3️⃣ Envie pelo WhatsApp e receba valores e prazos\n\nViu um produto aqui no Instagram? Cada post tem um código (PROD-XXXX): é só buscar no site ou mandar para a gente.\n\n🏬 Lojista? Temos condições especiais. Fale com nossa especialista!\n\n" + WPP + "\n\n" + TAGS + " #lojista #orcamento"))

# ---------------- DIA 3
n = 6
posts.append(P(3, '09:00', 'Dica', 'altura-do-pendente', 'Dica: altura certa do pendente', [
    cover('Dica de iluminação', 'Qual a altura certa do pendente?', 'As medidas que fazem a diferença na sala de jantar e na cozinha.', n, big_icon(ICONS['pendentes'])),
    slide(2, n, '70–90', 'cm acima da mesa', 'Essa é a distância ideal entre o tampo da mesa de jantar e a base do pendente: ilumina bem sem atrapalhar a conversa.'),
    slide(3, n, '65–80', 'cm acima da bancada', 'Em ilhas e bancadas, use mais de um pendente com a mesma distância entre eles e centralizados no tampo.'),
    slide(4, n, '½ a ⅔', 'da largura da mesa', 'É o tamanho ideal do pendente. Exemplo: mesa de 1 m de largura pede um pendente entre 50 e 65 cm.'),
    slide(5, n, '2,10 m', 'livres em passagens', 'Em halls e corredores, deixe pelo menos 2,10 m entre o piso e a base do pendente para ninguém bater a cabeça.'),
    cta(6, n, 'Salve para a sua obra', 'Precisa de ajuda para escolher o modelo e o tamanho? Fale com a gente.'),
], "Pendente muito alto some no ambiente. Muito baixo, atrapalha. 😅\n\nAs medidas certas:\n📏 Mesa de jantar: 70 a 90 cm entre o tampo e o pendente\n📏 Bancadas e ilhas: 65 a 80 cm\n📏 Tamanho: metade a dois terços da largura da mesa\n📏 Passagens: no mínimo 2,10 m livres do piso\n\nSalve e mande para quem está reformando! 📌\n\n" + WPP + "\n\n" + TAGS + " #pendente #reforma #dicasdeiluminacao"))

posts.append(P(3, '12:30', 'Produto', 'prod-1722', 'Pendente Silicone D800mm LED', [
    produto(dict(code='PROD-1722', selo='Design moderno', categoria='Pendentes', titulo='Pendente Silicone D800mm LED', chips=['LED 3200K', 'Bivolt', '80 cm', 'Cabo 2m'], opcoes='Branco ou dourado')),
], "Pendente Silicone D800mm LED 〰️\n\nLinhas onduladas de luz que viram o centro das atenções. Perfeito sobre mesas de jantar, bancadas e em projetos comerciais.\n\n• LED integrado 3200K (luz neutra)\n• Bivolt (127/220V)\n• 80 cm de comprimento · cabo de 2m\n• Silicone + metal\n• Opções: branco ou dourado\n\n🔎 Código LumiFa: PROD-1722 (dourado: PROD-1723)\n💰 A partir de R$ 288,00\n\n" + WPP + "\n\n" + TAGS + " #pendente #luminariamoderna"))

n = 3
posts.append(P(3, '19:30', 'Inspiração', 'sala-de-jantar', 'Inspiração: a luz da sala de jantar', [
    cover('Inspiração', 'A luz certa na sala de jantar', 'Peça única de destaque ou composição de pendentes? Depende da sua mesa.', n,
          f"<div style='margin-top:60px;display:flex;justify-content:center'>{arch(photo('PROD-001'), 420, 470)}</div>", 96),
    slide_photo(2, n, 'Pendente Cristal ⌀120mm · PROD-1587', 'Brilho em dupla ou trio', 'Pequenos e marcantes, ficam lindos alinhados sobre a mesa retangular. Dourado ou cromado.', photo('PROD-1587')),
    cta(3, n, 'Redonda ou retangular?', 'Mesa redonda pede um pendente central de destaque. Mesa longa fica linda com 2 ou 3 pendentes alinhados ou um modelo linear.'),
], "A sala de jantar é o lugar perfeito para a luminária virar protagonista ✨\n\n🔸 Mesa redonda ou quadrada: um pendente central de destaque\n🔸 Mesa retangular: 2 ou 3 pendentes menores alinhados, ou um modelo linear\n\nNos posts: Pendente Acrilux Brisa (PROD-001) e Pendente Cristal ⌀120mm, em dourado ou cromado (PROD-1587 / PROD-1586), a partir de R$ 108,00.\n\nQual combina mais com a sua casa? Conta aqui nos comentários 👇\n\n" + WPP + "\n\n" + TAGS + " #saladejantar #pendente #decoracaocomluz"))

# ---------------- DIA 4
n = 5
posts.append(P(4, '09:00', 'Dica', 'camadas-de-luz', 'Dica: as 3 camadas de luz', [
    cover('Dica de iluminação', 'Os 3 tipos de luz que todo ambiente precisa', 'O segredo de um projeto bonito e funcional é combinar camadas.', n, big_icon(ICONS['led']), 92),
    slide(2, n, '1', 'Luz geral', 'Ilumina o ambiente por igual. Painéis de LED, plafons e spots embutidos fazem esse papel.'),
    slide(3, n, '2', 'Luz de tarefa', 'Foco onde você lê, cozinha ou trabalha: pendentes sobre bancadas, arandelas de leitura e luminárias de mesa.'),
    slide(4, n, '3', 'Luz de destaque', 'Cria clima e valoriza detalhes: fitas de LED em nichos e sancas, spots direcionáveis e arandelas na parede.'),
    cta(5, n, 'Combine as três', 'Com camadas, você liga só o que precisa em cada momento e o ambiente muda de clima.'),
], "Um único ponto de luz no meio do teto deixa qualquer ambiente sem graça. A solução são as camadas de luz 💡\n\n1️⃣ Luz geral: ilumina tudo por igual (painéis, plafons, spots)\n2️⃣ Luz de tarefa: foco para ler, cozinhar e trabalhar (pendentes, arandelas, luminárias de mesa)\n3️⃣ Luz de destaque: clima e charme (fitas de LED, spots direcionáveis, arandelas)\n\nSalve para planejar o seu próximo ambiente! 📌\n\n" + WPP + "\n\n" + TAGS + " #projetodeiluminacao #dicasdeiluminacao"))

posts.append(P(4, '12:30', 'Produto', 'prod-046', 'Arandela Leitura Nobre Read Signature', [
    produto(dict(code='PROD-046', selo='Cabeceira', categoria='Arandelas', titulo='Arandela de Leitura Read Signature', chips=['3W', '210 lm', '3000K', 'Facho 24°', 'Bivolt'], opcoes='Dourada, branca ou preta')),
], "Arandela de Leitura Nobre Read Signature 📖\n\nO detalhe que transforma a cabeceira: foco de leitura direcionável, prateleira de apoio e acabamento dourado.\n\n• 3W · 210 lm · facho de 24°\n• Luz quente 3000K\n• Bivolt (127/220V)\n• Opções: dourada, branca ou preta\n\n🔎 Código LumiFa: PROD-046 (branca: PROD-044 · preta: PROD-045)\n💰 A partir de R$ 359,84\n\n" + WPP + "\n\n" + TAGS + " #arandela #quartodecasal #cabeceira"))

n = 4
posts.append(P(4, '19:30', 'Inspiração', 'quarto-aconchegante', 'Inspiração: quarto aconchegante', [
    cover('Inspiração', 'Quarto aconchegante em 3 passos', 'Luz quente e em camadas: o quarto vira refúgio.', n, big_icon(ICONS['dicas'])),
    slide(2, n, '01', 'Luz geral suave', 'Prefira luz quente (3000K) no plafon ou nos spots. Ela relaxa e prepara para o sono.'),
    slide_photo(3, n, 'Arandela Read Signature · PROD-046', 'Leitura na cabeceira', 'Um foco direcionável para ler sem acender o quarto inteiro, nem incomodar quem dorme ao lado.', photo('PROD-046')),
    cta(4, n, 'Luz indireta', 'Uma fita de LED atrás da cabeceira ou dentro de um nicho completa o clima. Quer ajuda para montar o seu?'),
], "Quarto aconchegante em 3 passos 🛏️✨\n\n1️⃣ Luz geral suave e quente (3000K)\n2️⃣ Arandela de leitura na cabeceira: foco só onde precisa\n3️⃣ Luz indireta com fita de LED atrás da cabeceira ou em nichos\n\nNo post: Arandela de Leitura Read Signature, código PROD-046.\n\n" + WPP + "\n\n" + TAGS + " #quarto #quartodecasal #decoracaocomluz"))

# ---------------- DIA 5
n = 5
posts.append(P(5, '09:00', 'Dica', 'watts-e-lumens', 'Dica: watts não medem claridade', [
    cover('Dica de iluminação', 'Watts não medem claridade', 'Entenda o número que realmente importa na hora de comparar lâmpadas e luminárias.', n, big_icon(ICONS['led'])),
    slide(2, n, 'W', 'Watt é consumo', 'Indica quanta energia a lâmpada gasta, não quanta luz ela entrega.'),
    slide(3, n, 'lm', 'Lúmen é luz', 'O fluxo luminoso (lm) mostra a quantidade de luz. Quanto mais lúmens, mais claro.'),
    slide(4, n, '≈ 800 lm', 'LED de ~9W = incandescente de 60W', 'Por isso o LED gasta muito menos para iluminar o mesmo tanto. Um painel de LED de 12W, por exemplo, entrega 800 lm.', title_size=64),
    cta(5, n, 'Compare pelos lúmens', 'Todos os produtos do nosso site têm ficha técnica com potência e fluxo luminoso.'),
], "Quem nunca escolheu lâmpada pelos watts? 🤔\n\n⚡ Watt (W) = consumo de energia\n💡 Lúmen (lm) = quantidade de luz\n\nUma lâmpada LED de cerca de 9W ilumina como uma incandescente de 60W (aprox. 800 lm), gastando muito menos.\n\nNa hora de comparar, olhe o fluxo luminoso na ficha técnica. No site da LumiFa, todo produto tem a sua.\n\n" + WPP + "\n\n" + TAGS + " #economiadeenergia #dicasdeiluminacao"))

posts.append(P(5, '12:30', 'Produto', 'prod-287', 'Painel de LED Embutir Redondo Preto 12W', [
    produto(dict(code='PROD-287', selo='Mais vendido', categoria='Painéis de LED', titulo='Painel de LED Embutir Redondo Preto 12W', chips=['12W', '800 lm', '3000K · 4000K · 6500K', 'Bivolt'], opcoes='Alumínio, ângulo 120°', ts=56)),
], "Painel de LED de Embutir Redondo Preto 12W ⚫\n\nNossos painéis de LED estão entre os mais vendidos, e o acabamento preto deixa o teto moderno e elegante.\n\n• 12W · 800 lm · ângulo de 120°\n• Temperaturas: 3000K, 4000K ou 6500K\n• Bivolt (127/220V)\n• Corpo em alumínio\n\nPara casas, lojas, escritórios, cozinhas, banheiros e consultórios.\n\n🔎 Códigos LumiFa: PROD-286 (3000K) · PROD-287 (4000K) · PROD-288 (6500K)\n💰 A partir de R$ 23,15\n\n🏬 Lojista: consulte condições por volume!\n\n" + WPP + "\n\n" + TAGS + " #paineldeled #plafon #ledembutir"))

n = 5
posts.append(P(5, '19:30', 'Lojista', 'lojista-paineis-led', 'Para lojistas: painéis de LED no mix', [
    cover('Para lojistas', 'Por que ter painéis de LED no seu mix', 'O produto que todo cliente de reforma e obra procura.', n, big_icon(ICONS['led'])),
    slide(2, n, '01', 'Campeões de venda', 'Os painéis de LED estão entre os itens mais pedidos do nosso catálogo, com giro rápido na prateleira.'),
    slide(3, n, '02', 'Atendem todo cliente', 'Residências, lojas, escritórios, consultórios, cozinhas e banheiros: serve para tudo.'),
    slide(4, n, '03', 'Variedade que vende', 'Vários tamanhos e formatos, acabamento branco ou preto e temperaturas de 3000K a 6500K.'),
    cta(5, n, 'Monte seu pedido', 'Condições especiais para lojistas. Fale com nossa especialista e receba sua tabela.'),
], "🏬 Lojista, esse post é para você!\n\nPor que ter painéis de LED no seu mix:\n✅ Estão entre os mais vendidos do nosso catálogo\n✅ Atendem casas, lojas, escritórios e consultórios\n✅ Vários tamanhos, formatos e temperaturas de cor\n\nMonte seu pedido no site (Meu Orçamento) e envie pelo WhatsApp. Temos condições especiais para revenda.\n\n" + WPP + "\n\n" + TAGS + " #lojista #revenda #paineldeled"))

# ---------------- DIA 6
n = 5
posts.append(P(6, '09:00', 'Dica', 'irc', 'Dica: o que é IRC', [
    cover('Dica de iluminação', 'Você já ouviu falar em IRC?', 'O número que mostra se a luz revela as cores de verdade.', n, big_icon(ICONS['dicas'])),
    slide(2, n, 'IRC', 'Índice de Reprodução de Cor', 'Vai de 0 a 100 e indica o quanto a luz mostra as cores reais de objetos, roupas, alimentos e pele.', title_size=70),
    slide(3, n, '80+', 'Para a sua casa', 'Acima de 80, as cores ficam naturais em salas, quartos e cozinhas.'),
    slide(4, n, '90+', 'Para lojas e closets', 'Em vitrines, provadores, closets e maquiagem, IRC 90 ou mais faz tudo parecer como realmente é.'),
    cta(5, n, 'Olhe a ficha técnica', 'O IRC aparece nas especificações de fitas, lâmpadas e luminárias. Na dúvida, pergunte!'),
], "Já comprou uma roupa que parecia de uma cor na loja e de outra em casa? A culpa pode ser do IRC 👀\n\nIRC (Índice de Reprodução de Cor) vai de 0 a 100 e mostra o quanto a luz revela as cores reais.\n\n🏠 Em casa: IRC acima de 80\n🛍️ Em lojas, closets e maquiagem: IRC 90 ou mais\n\nSalve para lembrar na próxima compra! 📌\n\n" + WPP + "\n\n" + TAGS + " #irc #iluminacaocomercial #dicasdeiluminacao"))

posts.append(P(6, '12:30', 'Produto', 'prod-3747', 'Candelabro de Metal Preto com 5 Cúpulas', [
    produto(dict(code='PROD-3747', selo='Clássico', categoria='Lustres', titulo='Candelabro Preto com 5 Cúpulas de Tecido', chips=['80 cm', 'Altura 40 cm', '5x E14', 'Cabo 2m'], opcoes='Preto ou dourado/bege', ts=56)),
], "Candelabro de Metal com 5 Cúpulas de Tecido 🕯️\n\nO charme clássico que nunca sai de moda, com braços curvos e cúpulas de tecido. Lindo em salas de estar, de jantar e halls de entrada.\n\n• Diâmetro de 80 cm · altura de 40 cm\n• 5 bocais E14 (lâmpadas não inclusas)\n• Cabo de 2m\n• Opções: preto ou dourado com cúpulas bege\n\n🔎 Código LumiFa: PROD-3747 (dourado/bege: PROD-3743)\n💰 A partir de R$ 774,00\n\n" + WPP + "\n\n" + TAGS + " #lustre #candelabro #saladeestar"))

n = 6
posts.append(P(6, '19:30', 'Inspiração', 'erros-de-iluminacao', 'Inspiração: 4 erros de iluminação', [
    cover('Evite', '4 erros que deixam a casa sem graça', 'E como resolver cada um deles com a luz certa.', n, big_icon(ICONS['dicas'])),
    slide(2, n, '01', 'Um só ponto no teto', 'A luz fica chapada e cria sombras. Combine luz geral, de tarefa e de destaque.'),
    slide(3, n, '02', 'Misturar temperaturas', 'Luz quente e fria no mesmo ambiente deixa tudo desencontrado. Escolha uma e mantenha.'),
    slide(4, n, '03', 'Pendente na altura errada', 'Sobre a mesa, o ideal é de 70 a 90 cm do tampo. Mais alto some, mais baixo atrapalha.'),
    slide(5, n, '04', 'Esquecer a luz indireta', 'Fitas de LED em nichos e sancas e arandelas na parede trazem profundidade e aconchego.'),
    cta(6, n, 'Qual você já cometeu?', 'Conta nos comentários! E se quiser ajuda para acertar a iluminação, fale com a gente.'),
], "4 erros de iluminação que deixam a casa sem graça (e como resolver) 💡\n\n❌ Um único ponto de luz no teto → combine camadas de luz\n❌ Misturar luz quente e fria → escolha uma temperatura por ambiente\n❌ Pendente na altura errada → 70 a 90 cm acima da mesa\n❌ Esquecer a luz indireta → fitas de LED e arandelas\n\nQual desses você já cometeu? 😅 Conta aqui 👇\n\n" + WPP + "\n\n" + TAGS + " #decoracaocomluz #dicasdeiluminacao"))

# ---------------- DIA 7
n = 6
posts.append(P(7, '09:00', 'Dica', 'arandelas-onde-instalar', 'Dica: arandelas, onde e como instalar', [
    cover('Dica de iluminação', 'Arandela: onde e como instalar', 'Guia rápido para corredores, quartos, escadas e áreas externas.', n, big_icon(ICONS['arandelas'])),
    slide(2, n, '1,60–1,80', 'm do piso', 'Em corredores e salas, essa altura média evita que a luz ofusque quem passa.', title_size=70),
    slide(3, n, 'Cabeceira', 'Foco no livro', 'A arandela de leitura fica ao lado da cama, com o foco direcionado, sem incomodar quem dorme ao lado.', title_size=70),
    slide(4, n, 'Escadas', 'Luz baixa guia o caminho', 'Arandelas perto dos degraus iluminam o piso e evitam tropeços à noite.', title_size=70),
    slide(5, n, 'IP65+', 'Para áreas externas', 'Fora de casa, escolha modelos com grau de proteção IP adequado contra chuva e poeira.', title_size=70),
    cta(6, n, 'Salve este guia', 'Temos arandelas para todos esses usos. Fale com nossa especialista para escolher a sua.'),
], "Arandela: onde e como instalar? 🧭\n\n📍 Corredores e salas: em média entre 1,60 m e 1,80 m do piso\n📍 Cabeceira: ao lado da cama, com foco direcionado para leitura\n📍 Escadas: perto dos degraus, para guiar o caminho\n📍 Áreas externas: modelos com proteção IP contra chuva e poeira\n\nSalve e compartilhe com quem está reformando! 📌\n\n" + WPP + "\n\n" + TAGS + " #arandela #dicasdeiluminacao #reforma"))

posts.append(P(7, '12:30', 'Produto', 'prod-1992', 'Arandela Metal D300mm LED Preto', [
    produto(dict(code='PROD-1992', selo='Fachadas', categoria='Arandelas', titulo='Arandela Metal LED Preto 20W', chips=['20W', 'LED 3200K', 'Bivolt', '30 cm'], opcoes='Metal preto')),
], "Arandela Metal LED Preto 20W 🖤\n\nLinha de luz vertical que valoriza paredes, corredores, escadas e fachadas, criando efeitos de luz marcantes.\n\n• 20W · LED 3200K (luz neutra)\n• Bivolt (127/220V)\n• 30 cm\n• Metal com acabamento preto\n\n🔎 Código LumiFa: PROD-1992\n💰 R$ 158,40\n\n" + WPP + "\n\n" + TAGS + " #arandela #fachada #iluminacaoexterna"))

n = 4
posts.append(P(7, '19:30', 'Inspiração', 'fachada-a-noite', 'Inspiração: fachada que se destaca à noite', [
    cover('Inspiração', 'Fachada que se destaca à noite', 'Pequenos pontos de luz valorizam a arquitetura e trazem segurança.', n,
          f"<div style='margin-top:60px;display:flex;justify-content:center'>{arch(photo('PROD-1992'), 420, 470, fit='cover')}</div>", 96),
    slide(2, n, '01', 'Luz rasante na parede', 'Arandelas de linha valorizam texturas como pedra, madeira e cimento queimado.'),
    slide(3, n, '02', 'Caminhos marcados', 'Balizadores e espetos de jardim guiam quem chega e destacam plantas e canteiros.'),
    cta(4, n, 'Prefira luz quente', 'Luz de 3000K deixa a fachada acolhedora. Fale com nossa especialista para montar o projeto.'),
], "Fachada bonita de dia e ainda mais linda à noite 🌙✨\n\n🔸 Arandelas de linha valorizam texturas de parede\n🔸 Balizadores e espetos marcam caminhos no jardim\n🔸 Luz quente deixa a entrada acolhedora\n\nNo post: Arandela Metal LED Preto 20W, código PROD-1992.\n\n" + WPP + "\n\n" + TAGS + " #fachada #iluminacaoexterna #jardim"))
