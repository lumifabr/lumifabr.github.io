from base import *

OUT = REPO / 'instagram' / 'perfil'
S = 'fill="none" stroke="#D4AF37" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"'

ICONS = {
 'pendentes': f'<svg viewBox="0 0 200 200" {S}><line x1="100" y1="20" x2="100" y2="80"/><path d="M45 130 Q100 60 155 130 Z"/><path d="M85 142 Q100 160 115 142"/></svg>',
 'arandelas': f'<svg viewBox="0 0 200 200" {S}><rect x="40" y="40" width="22" height="120" rx="6"/><path d="M62 100 H95"/><path d="M95 70 L150 80 L150 120 L95 130 Z"/><path d="M160 92 L178 86 M160 108 L178 114"/></svg>',
 'led': f'<svg viewBox="0 0 200 200" {S}><circle cx="100" cy="100" r="62"/><circle cx="100" cy="100" r="36"/><path d="M100 18 V30 M100 170 V182 M18 100 H30 M170 100 H182 M42 42 L51 51 M149 149 L158 158 M158 42 L149 51 M51 149 L42 158"/></svg>',
 'dicas': f'<svg viewBox="0 0 200 200" {S}><path d="M100 30 C65 30 48 58 52 84 C55 104 70 114 76 130 H124 C130 114 145 104 148 84 C152 58 135 30 100 30 Z"/><path d="M80 150 H120 M86 168 H114"/><path d="M100 60 V100 M88 88 L100 100 L112 88"/></svg>',
 'orcamento': f'<svg viewBox="0 0 200 200" {S}><path d="M45 155 L55 120 A62 62 0 1 1 82 148 Z"/><path d="M78 92 H124 M78 112 H112"/></svg>',
 'sobre': f'<svg viewBox="0 0 200 200" {S}><path d="M40 160 V40 M40 160 H96 M120 160 V40 H168 M120 98 H156"/><circle cx="178" cy="34" r="6" fill="#D4AF37"/></svg>',
 'externa': f'<svg viewBox="0 0 200 200" {S}><path d="M30 165 H170"/><path d="M60 165 V95 L100 60 L140 95 V165"/><rect x="88" y="120" width="24" height="45"/><path d="M152 100 V125 M146 100 H158"/><path d="M162 112 L176 106"/></svg>',
}

def foto_perfil(r):
    body = f"""<div class='c' style='background:radial-gradient(circle at 50% 42%, #3a2c14 0%, #1d160e 40%, {INK} 70%)'>
    <img src='{ICONE}' style='position:absolute;width:520px;left:280px;top:270px'></div>"""
    r.render(page(body, 1080, 1080), OUT / 'foto-perfil.jpg', 1080, 1080)

def destaque(r, nome):
    body = f"""<div class='c' style='background:radial-gradient(circle at 50% 50%, #2e2312 0%, {INK} 55%)'>
    <div style='position:absolute;left:290px;top:710px;width:500px;height:500px;border-radius:50%;border:3px solid rgba(212,175,55,.45)'></div>
    <div style='position:absolute;left:390px;top:810px;width:300px;height:300px'>{ICONS[nome]}</div></div>"""
    r.render(page(body, 1080, 1920), OUT / 'destaques' / f'{nome}.jpg', 1080, 1920)

if __name__ == '__main__':
    with Renderer() as r:
        foto_perfil(r)
        for n in ICONS: destaque(r, n)
