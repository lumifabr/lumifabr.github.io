import json, cv2, numpy as np, pytesseract, sys, re
from multiprocessing import Pool
rows = json.load(open('/home/claude/ml/ok.json'))
def f(c):
    im = cv2.imread('imagens/' + c + '.jpg')
    h, w = im.shape[:2]
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    s = 1000 / max(h, w); g2 = cv2.resize(g, None, fx=s, fy=s)
    blur = cv2.Laplacian(g2, cv2.CV_64F).var()
    border = np.concatenate([g[:8].ravel(), g[-8:].ravel(), g[:, :8].ravel(), g[:, -8:].ravel()])
    white_border = float((border > 235).mean())
    ys, xs = np.where(g < 235)
    fill = (np.ptp(xs) * np.ptp(ys)) / (w * h) if len(xs) else 0
    txt = pytesseract.image_to_data(g2, lang='eng', config='--psm 11', output_type=pytesseract.Output.DICT)
    words = [t for t, cf in zip(txt['text'], txt['conf']) if len(t.strip()) >= 3 and float(cf) > 70 and re.search(r'[A-Za-z0-9]{3}', t)]
    return c, dict(w=w, h=h, blur=round(blur, 1), wb=round(white_border, 2), fill=round(fill, 2), words=words[:12], nw=len(words))
if __name__ == '__main__':
    with Pool(2) as p: res = dict(p.map(f, [r['codigo'] for r in rows], chunksize=20))
    json.dump(res, open('/home/claude/work/qa.json', 'w'))
    print(len(res))
