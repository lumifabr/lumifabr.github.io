"""Motor de renderização das artes do Instagram da LumiFa (HTML -> JPEG via Chrome)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

REPO = Path('/home/claude/lumifabr.github.io')
FONTS = Path('/home/claude/work/node_modules/@fontsource')
IMG = REPO / 'imagens'

GOLD = '#D4AF37'
GOLD2 = '#96701A'
INK = '#15110D'
CREAM = '#F6F1E7'

def ff(fam, w, style='normal'):
    f = FONTS / fam / 'files' / f'{fam}-latin-{w}-{style}.woff2'
    name = 'Corm' if 'cormorant' in fam else 'Jak'
    return f"@font-face{{font-family:'{name}';src:url('file://{f}') format('woff2');font-weight:{w};font-style:{style}}}"

FONTCSS = ''.join(ff('cormorant-garamond', w, s) for w in (400, 500, 600, 700) for s in ('normal', 'italic')) + \
          ''.join(ff('plus-jakarta-sans', w) for w in (400, 500, 600, 700))

CSS = FONTCSS + f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:W;height:H;overflow:hidden}}
body{{font-family:'Jak';color:{CREAM};-webkit-font-smoothing:antialiased}}
.c{{position:relative;width:100%;height:100%;overflow:hidden}}
.dark{{background:radial-gradient(ellipse 80% 55% at 50% 0%, #3a2c14 0%, #1d160e 45%, {INK} 75%);}}
.cream{{background:{CREAM};color:{INK}}}
.serif{{font-family:'Corm'}}
.gold{{color:{GOLD}}}
.kick{{font-family:'Jak';font-weight:600;letter-spacing:.32em;text-transform:uppercase;font-size:22px;color:{GOLD}}}
.logo{{position:absolute;top:70px;left:90px;height:58px}}
.pg{{position:absolute;top:84px;right:90px;font-size:22px;letter-spacing:.2em;color:{GOLD};font-weight:600}}
.foot{{position:absolute;left:90px;right:90px;bottom:64px;display:flex;justify-content:space-between;align-items:center;font-size:23px;letter-spacing:.06em;color:#cbbf9f}}
.foot b{{color:{GOLD};font-weight:600}}
.rule{{width:90px;height:3px;background:{GOLD};border-radius:2px}}
h1{{font-family:'Corm';font-weight:500;line-height:1.02;letter-spacing:-.005em}}
p{{line-height:1.45}}
.chip{{display:inline-block;border:1.5px solid {GOLD};color:{GOLD};border-radius:999px;padding:12px 26px;font-size:24px;font-weight:600;letter-spacing:.06em;margin:0 12px 14px 0}}
.cream .chip{{border-color:{GOLD2};color:{GOLD2}}}
.code{{display:inline-block;background:{INK};color:{GOLD};padding:12px 26px;border-radius:10px;font-weight:700;letter-spacing:.14em;font-size:26px}}
"""

def page(body, w=1080, h=1350, extra_css=''):
    css = CSS.replace('W', f'{w}px', 1).replace('H', f'{h}px', 1)
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}{extra_css}</style></head><body>{body}</body></html>"

def img(p):
    return f"file://{p}"

LOGO_DARK = img(IMG / 'logo-escuro.png')
LOGO_LIGHT = img(IMG / 'logo.png')
ICONE = img(IMG / 'icone.png')

class Renderer:
    def __enter__(self):
        self.pw = sync_playwright().start()
        self.b = self.pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        return self
    def __exit__(self, *a):
        self.b.close(); self.pw.stop()
    def render(self, html, out, w=1080, h=1350):
        out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
        pg = self.b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        tmp = Path('/home/claude/work/tmp.html'); tmp.write_text(html, encoding='utf-8')
        pg.goto(f'file://{tmp}'); pg.wait_for_timeout(250)
        pg.evaluate('document.fonts.ready')
        png = out.with_suffix('.png')
        pg.screenshot(path=str(png)); pg.close()
        Image.open(png).convert('RGB').save(out, 'JPEG', quality=90, optimize=True, progressive=True)
        png.unlink()
        return out
