"""Reels da semana 1 (3 por dia: 11:00, 17:00, 21:00). Cada Reel tem música e produtos diferentes."""
from reel import hook, prod, tip, fim

WPP = "📲 Peça seu orçamento: fale com nossa especialista pelo WhatsApp (11) 95978-1849 ou pelo link na bio → lumifa.com.br"
TAGS = "#lumifa #iluminacao #iluminacaodecorativa #decoracao #designdeinteriores #reels"

def top3(kicker, titulo, itens, pergunta, tags, size=124):
    """itens: (code, nome, info, preco_legenda)"""
    scenes = [(hook(kicker, titulo, 'Qual é o seu favorito? 1, 2 ou 3?', size), 6)]
    for i, (c, n, info, _) in enumerate(itens, 1):
        scenes.append((prod(str(i), c, n, info), 6))
    scenes.append((fim(), 8))
    linhas = '\n'.join(f"{['1️⃣','2️⃣','3️⃣'][i]} {n}: {c} · {p}" for i, (c, n, _, p) in enumerate(itens))
    cap = f"{pergunta} Comenta o número aqui 👇\n\n{linhas}\n\n{WPP}\n\n{TAGS} {tags}"
    return scenes, cap

def dica(kicker, titulo, passos, cap_intro, tags, size=118):
    scenes = [(hook(kicker, titulo, 'Salve para não esquecer 📌', size), 6)]
    for i, (t, x) in enumerate(passos, 1):
        scenes.append((tip(f'0{i}', t, x), 8))
    scenes.append((fim('Quer ajuda<br>no seu projeto?', 'Fale com nossa especialista'), 8))
    linhas = '\n'.join(f"{['1️⃣','2️⃣','3️⃣','4️⃣'][i]} {t}: {x}" for i, (t, x) in enumerate(passos))
    cap = f"{cap_intro}\n\n{linhas}\n\nSalve e compartilhe com quem está reformando! 📌\n\n{WPP}\n\n{TAGS} {tags}"
    return scenes, cap

G = "<span class='gold'>"; E = "</span>"
R = []  # (data, hora, slug, scenes, caption)

# ---- 10/11
R.append(('2026-11-10', '11:00', 'pendentes-led', *top3('Pendentes de LED', f"Pendentes que<br>são {G}pura escultura{E}", [
    ('PROD-1664', 'Pendente 3 Anéis LED', '40 + 60 + 80 cm · preto ou marrom', 'a partir de R$ 1.411,20'),
    ('PROD-1657', 'Pendente Ondas LED 80cm', 'Silicone + metal · preto', 'R$ 333,00'),
    ('PROD-1702', 'Pendente Anel LED ⌀20cm', 'Compacto · preto ou dourado', 'R$ 136,80')],
    'Pendentes de LED que parecem escultura ✨ Qual você colocaria na sua casa?', '#pendente #luminariamoderna #led')))
R.append(('2026-11-10', '17:00', 'dica-sala-maior', *dica('Dica rápida', f"3 truques de luz<br>para a sala<br>{G}parecer maior{E}", [
    ('Ilumine as paredes', 'Arandelas e spots voltados para a parede afastam visualmente os limites do ambiente.'),
    ('Luz indireta no teto', 'Fita de LED na sanca ou no rebaixo “levanta” o pé-direito.'),
    ('Fuja do ponto único', 'Luz só no centro encolhe a sala. Espalhe pontos de luz pelo ambiente.')],
    'Sala pequena? A iluminação certa faz ela parecer maior 💡', '#saladeestar #dicasdeiluminacao #decoracaocomluz')))
R.append(('2026-11-10', '21:00', 'arandelas-joia', *top3('Arandelas', f"Arandelas que<br>viram {G}joia{E}<br>na parede", [
    ('PROD-1968', 'Arandela Cristal 22cm', 'Cristal + metal · dourada ou cromada', 'R$ 108,00'),
    ('PROD-1468', 'Arandela Prisma 12W', 'Acabamento gold · luz que desenha a parede', 'R$ 167,84'),
    ('PROD-1471', 'Arandela Revoar 12W', 'Anel de luz · branca', 'R$ 201,44')],
    'Arandelas que deixam qualquer parede mais elegante ✨ Qual é a sua?', '#arandela #decoracao #parede')))
# ---- 11/11
R.append(('2026-11-11', '11:00', 'paineis-led', *top3('Mais vendidos', f"Painéis de LED:<br>os {G}queridinhos{E}<br>das obras", [
    ('PROD-306', 'Painel LED Embutir Quadrado', 'Acabamento preto · 3000K ou 6500K', 'a partir de R$ 46,90'),
    ('PROD-338', 'Painel LED Sobrepor Quadrado', 'Acabamento preto · 3000K, 4000K ou 6500K', 'a partir de R$ 56,96'),
    ('PROD-2505', 'Painel LED Retangular 45W', 'Ideal para escritórios e lojas · 2700K ou 4000K', 'a partir de R$ 202,50')],
    'Painéis de LED estão entre os mais vendidos do nosso catálogo 💡 Lojista, consulte condições!', '#paineldeled #plafon #lojista')))
R.append(('2026-11-11', '17:00', 'dica-banheiro', *dica('Dica rápida', f"O erro mais comum<br>na luz do<br>{G}banheiro{E}", [
    ('Luz só no teto', 'Ela fica atrás de você e cria sombras no rosto na frente do espelho.'),
    ('Ilumine de frente', 'Arandelas nas laterais do espelho ou um perfil de LED iluminam o rosto por igual.'),
    ('4000K e IRC alto', 'Luz neutra e fiel às cores para ver a pele e a maquiagem como são.')],
    'Seu espelho do banheiro deixa sombras no rosto? Veja como resolver 🪞', '#banheiro #dicasdeiluminacao #espelho')))
R.append(('2026-11-11', '21:00', 'lustres', *top3('Lustres', f"Lustres que<br>{G}roubam a cena{E}", [
    ('PROD-3745', 'Candelabro 15 Braços ⌀95cm', 'Metal dourado · também em preto', 'a partir de R$ 1.530,00'),
    ('PROD-3756', 'Candelabro Aurum 6 Braços', '⌀68cm · preto ou dourado', 'a partir de R$ 396,00'),
    ('PROD-3757', 'Candelabro Aurum 10 Braços', '⌀74cm · preto ou dourado', 'a partir de R$ 504,00')],
    'Lustres para quem ama um ambiente marcante ✨ Qual você escolheria?', '#lustre #candelabro #saladejantar')))
# ---- 12/11
R.append(('2026-11-12', '11:00', 'spots', *top3('Spots', f"Um spot<br>para cada<br>{G}projeto{E}", [
    ('PROD-499', 'Spot Aster 36W Direcionável', 'Alumínio · branco ou preto', 'R$ 172,88'),
    ('PROD-538', 'Spot Duplo 10W', 'Preto · 3000K, 4000K ou 6500K', 'a partir de R$ 30,80'),
    ('PROD-674', 'Spot de Embutir Luzon 9 LEDs', '3000K · preto ou branco', 'R$ 87,84')],
    'Spots para iluminar com precisão: lojas, salas, cozinhas e muito mais 💡', '#spot #iluminacaocomercial #projetodeiluminacao')))
R.append(('2026-11-12', '17:00', 'dica-cozinha', *dica('Dica rápida', f"Cozinha<br>{G}bem iluminada{E}<br>em 3 passos", [
    ('Luz geral neutra', 'Use 4000K para enxergar bem as cores dos alimentos.'),
    ('LED sob os armários', 'Uma fita de LED ilumina a bancada sem sombras na hora de cortar.'),
    ('Pendentes na ilha', 'Instale de 65 a 80 cm acima da bancada, com a mesma distância entre eles.')],
    'Cozinha bem iluminada é mais bonita e muito mais prática 🍳', '#cozinha #dicasdeiluminacao #fitadeled')))
R.append(('2026-11-12', '21:00', 'plafons-arte', *top3('Plafons', f"Plafons que são<br>{G}arte no teto{E}", [
    ('PROD-1894', 'Plafon LED Flor ⌀32cm', 'Preto, branco ou dourado', 'R$ 216,00'),
    ('PROD-1910', 'Plafon LED Anéis Duplos', 'Marrom ou preto', 'R$ 705,60'),
    ('PROD-1932', 'Plafon LED Quadrado 25cm', 'Acrílico · preto ou dourado', 'R$ 252,00')],
    'Plafons de LED que transformam o teto em peça de decoração ✨', '#plafon #led #decoracao')))
# ---- 13/11
R.append(('2026-11-13', '11:00', 'trilhos', *top3('Trilhos', f"Trilho: liberdade<br>para {G}mudar a luz{E}", [
    ('PROD-3189', 'Kit 3 Spots + Trilho LED', 'Corpo branco · 3000K ou 6000K', 'a partir de R$ 120,96'),
    ('PROD-822', 'Spot LED para Trilho', 'Preto · 3000K ou 4000K', 'a partir de R$ 60,03'),
    ('PROD-3183', 'Spot para Trilho LED 18W', 'Branco ou preto · 3000K', 'R$ 35,98')],
    'Com trilho você muda os spots de lugar quando quiser 🔁 Perfeito para lojas, salas e cozinhas.', '#trilho #spot #iluminacaocomercial')))
R.append(('2026-11-13', '17:00', 'dica-home-office', *dica('Dica rápida', f"Home office<br>com luz que<br>{G}não cansa{E}", [
    ('Luz neutra', 'Use 4000K no ambiente para manter o foco sem cansar a vista.'),
    ('Luminária do lado certo', 'Coloque do lado oposto da mão que escreve para não fazer sombra.'),
    ('Nada de reflexo na tela', 'Evite luz forte atrás de você ou batendo direto no monitor.')],
    'Trabalha em casa? Essa dica é pra você 💻', '#homeoffice #dicasdeiluminacao #escritorio')))
R.append(('2026-11-13', '21:00', 'pendentes-design', *top3('Pendentes', f"Pendentes que<br>decoram até<br>{G}apagados{E}", [
    ('PROD-1272', 'Pendente Glass Globo', 'Vidro âmbar ou fumê · E27', 'R$ 211,02'),
    ('PROD-1284', 'Pendente Diamante', '6+3W · grafite', 'R$ 158,24'),
    ('PROD-1288', 'Pendente Orbis 9W', 'Black · design aramado', 'R$ 159,84')],
    'Pendentes com design marcante, lindos acesos ou apagados ✨', '#pendente #decoracao #designdeinteriores')))
# ---- 14/11
R.append(('2026-11-14', '11:00', 'fitas-neon', *top3('Fitas e neon', f"Fitas e neon<br>de LED para<br>{G}projetos{E}", [
    ('PROD-1180', 'Neon Flexível 10x10mm', 'Rolo de 50m · 6500K ou 4000K', 'R$ 1.073,44'),
    ('PROD-1155', 'Fita LED COB', 'Rolo de 50m · 3000K ou 4000K', 'R$ 703,84'),
    ('PROD-1165', 'Mangueira Neon', 'Rolo de 100m · 6500K ou 3000K', 'R$ 1.359,84')],
    'Rolos de fita e neon de LED para instaladores, lojistas e projetos 💡', '#fitadeled #neon #lojista')))
R.append(('2026-11-14', '17:00', 'dica-varanda', *dica('Dica rápida', f"Varanda e<br>área gourmet<br>{G}aconchegantes{E}", [
    ('Luz quente', 'Use 3000K para criar clima de encontro e conversa.'),
    ('Luz na bancada', 'Pendentes ou fita de LED onde se prepara a comida.'),
    ('Proteção contra umidade', 'Em áreas descobertas, escolha luminárias com grau de proteção IP adequado.')],
    'Fim de semana pede varanda bem iluminada 🍷', '#varanda #areagourmet #dicasdeiluminacao')))
R.append(('2026-11-14', '21:00', 'luminarias-mesa', *top3('Luminárias de mesa', f"Para estudar<br>e trabalhar com<br>{G}estilo{E}", [
    ('PROD-2518', 'Luminária de Mesa LED Lite', '5W · 3000K · preta ou branca', 'R$ 179,10'),
    ('PROD-1425', 'Luminária de Mesa Luma', 'E27 · preta ou branca', 'R$ 62,24'),
    ('PROD-2521', 'Luminária Articulável', 'Com base · E27 · preta ou branca', 'R$ 98,01')],
    'Luminárias de mesa para escrivaninha, criado-mudo e home office 📚', '#luminariademesa #homeoffice #decoracao')))
# ---- 15/11
R.append(('2026-11-15', '11:00', 'luz-caminho', *top3('Externa e escadas', f"Luz que<br>{G}guia o caminho{E}", [
    ('PROD-1077', 'Balizador de Solo Hex', 'IP67 · antiofuscante · inox ou preto', 'a partir de R$ 119,84'),
    ('PROD-1092', 'Espeto LED de Jardim 5W', '3000K ou 6000K', 'R$ 23,84'),
    ('PROD-2364', 'Balizador de Parede LED 1W', 'Para escadas internas · branco ou preto', 'R$ 83,88')],
    'Caminhos, jardins e escadas mais bonitos e seguros à noite 🌙', '#jardim #iluminacaoexterna #balizador')))
R.append(('2026-11-15', '17:00', 'dica-vitrine', *dica('Para lojistas', f"Vitrine que<br>{G}vende mais{E}", [
    ('Mais clara que o interior', 'O contraste chama o olhar de quem passa pela calçada.'),
    ('Destaque nos produtos', 'Spots direcionáveis e trilhos colocam a luz onde está a venda.'),
    ('IRC 90 ou mais', 'Cores reais deixam o cliente seguro para comprar.')],
    'Lojista: a iluminação certa faz o cliente entrar e comprar 🛍️', '#lojista #vitrine #iluminacaocomercial')))
R.append(('2026-11-15', '21:00', 'lampadas-decorativas', *top3('Lâmpadas decorativas', f"Clima de festa<br>com {G}lâmpadas{E}<br>decorativas", [
    ('PROD-1341', 'Lâmpada S14 Lente Cristal', 'IP66 · filamento · pack com 10', 'a partir de R$ 5,62 a unidade'),
    ('PROD-1326', 'Lâmpada S14 Meteoro Colorida', 'IP65 · várias cores · pack com 10', 'R$ 10,38 a unidade'),
    ('PROD-1292', 'Pendente Retrô E27', 'Para lâmpadas aparentes · preto ou dourado', 'a partir de R$ 39,92')],
    'Varal de luzes para varandas, festas e áreas gourmet 🎉', '#lampadadecorativa #varaldeluz #festa')))
