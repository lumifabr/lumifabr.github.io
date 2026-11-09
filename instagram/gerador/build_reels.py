import json, sys
from pathlib import Path
from reel import *
import reels_semana01 as RS
R_ = REPO/'instagram'/'reels'/'semana-01'
BASE = 'https://www.lumifa.com.br/instagram/reels/semana-01'
cal = []
only = sys.argv[1:] 
with Renderer() as r:
    for i, (data, hora, slug, scenes, cap) in enumerate(RS.R, 2):
        name = f"r{i:02d}-{data[8:]}-{hora.replace(':','h')}-{slug}"
        est = estilo(i)
        if not only or slug in only:
            build(scenes, R_/f'{name}.mp4', r, est, work=f'/home/claude/work/_reel_{i}')
        cal.append(dict(id=f'reel-{i:02d}', data=data, hora=hora, titulo=slug, video=f'{BASE}/{name}.mp4', capa=f'{BASE}/{name}-capa.jpg',
                        legenda=cap, musica=f"{est['groove']} {est['bpm']} BPM {est['prog']}", status='programado'))
        print(name, est['groove'], est['bpm'], est['prog'], flush=True)
json.dump(cal, open(REPO/'instagram'/'calendario-reels-semana-01.json','w'), ensure_ascii=False, indent=1)
