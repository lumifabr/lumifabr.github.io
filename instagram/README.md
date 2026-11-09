# Instagram @lumifa.br

Pasta só do Instagram. Nada daqui aparece no catálogo do site; as imagens ficam aqui porque o Instagram precisa de um link público para publicar.

## Estrutura
- `perfil/` — foto de perfil, capas dos destaques e textos da bio (`perfil.md`).
- `posts/semana-XX/` — artes de cada semana. Nome do arquivo: `d<dia>-<hora>-<assunto>[-<slide>].jpg`.
- `calendario-semana-XX.json` — o que vai ao ar em cada dia e horário, com legenda e status.
- `gerador/` — scripts que montam as artes (HTML → JPEG pelo Chrome).

## Regras de conteúdo (resumo)
- Nunca citar o nome da especialista; usar "fale com nossa especialista".
- Não mostrar quantas fábricas representamos nem códigos das fábricas. Usar o código LumiFa (PROD-XXXX).
- Só produtos Ativos e com foto; nenhuma imagem com marca d'água.
- Variações de cor/temperatura = um produto com opções, "a partir de R$".

## Rotina (desde 10/11/2026)
- Feed: 1 publicação por dia às 19:00, alternando **dia de foto** (post/carrossel) e **dia de Reel**. Nunca os dois no mesmo dia.
- Stories: 6 por dia — 08:30 dica · 10:30 produto · 12:30 dica · 15:30 produto · 19:30 chamada para o post/Reel do dia · 21:30 chamada (orçamento/lojista/código).
- Tudo que vai ao ar está em `agenda.json` (data, hora, tipo post|reel|story, status). Os arquivos `calendario-*.json` são o estoque de conteúdo pronto.
- `stories/banco/` = banco de stories (dicas, produtos, chamadas).
Publicação feita pelo Claude via Windsor.ai (conta @lumifa.br).

## Como gerar uma nova semana
```
cd /home/claude/work && npm i @fontsource/cormorant-garamond @fontsource/plus-jakarta-sans
cp /home/claude/lumifabr.github.io/instagram/gerador/*.py .
# criar semanaXX.py no formato de semana01.py e ajustar build.py
python3 build.py
```
