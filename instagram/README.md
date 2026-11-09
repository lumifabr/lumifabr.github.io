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

## Rotina
3 posts por dia: 09:00 dica · 12:30 produto · 19:30 inspiração/institucional (horário de Brasília).
Publicação feita pelo Claude via Windsor.ai (conta @lumifa.br).

## Como gerar uma nova semana
```
cd /home/claude/work && npm i @fontsource/cormorant-garamond @fontsource/plus-jakarta-sans
cp /home/claude/lumifabr.github.io/instagram/gerador/*.py .
# criar semanaXX.py no formato de semana01.py e ajustar build.py
python3 build.py
```
