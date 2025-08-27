
import os, uuid
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

TMP = Path('report/_tmp'); TMP.mkdir(parents=True, exist_ok=True)

def _save(fig, name):
    p = TMP / f"{name}_{uuid.uuid4().hex[:8]}.png"
    fig.savefig(p, bbox_inches='tight', dpi=180)
    plt.close(fig)
    return str(p)

def product_chart(series, title, ylabel=''):
    fig = plt.figure(figsize=(4,2.2))
    for s in series:
        plt.plot(s.get('x',[]), s.get('y',[]), label=s.get('label',''))
    plt.title(title); plt.xlabel('Period'); plt.ylabel(ylabel)
    if any(s.get('label') for s in series):
        plt.legend(fontsize=7, loc='best', frameon=False)
    return _save(fig, 'prod')

def waterfall(items, title):
    # items: [{'label':..., 'value':..., 'measure':'relative|total'}]
    from matplotlib import pyplot as plt
    fig = plt.figure(figsize=(4,2.2))
    x_labels = [i['label'] for i in items]
    values = [i['value'] for i in items]
    running = 0
    ys, bottoms, colors = [], [], []
    for it in items:
        if it.get('measure','relative') == 'total':
            ys.append(running); bottoms.append(0); colors.append('#444444')
        else:
            ys.append(abs(it['value'])); bottoms.append(min(running, running+it['value']))
            colors.append('#1b9f97' if it['value']>=0 else '#c0392b')
            running += it['value']
    plt.bar(range(len(items)), ys, bottom=bottoms, color=colors)
    plt.xticks(range(len(items)), x_labels, rotation=0, fontsize=8)
    plt.title(title)
    return _save(fig, 'wf')

def ecrs_funnel(n_from:int, n_to:int, title='ECRS Funnel'):
    fig = plt.figure(figsize=(4,2.2))
    plt.bar([0,1],[n_from,n_to], color=['#d0d4d9','#1b9f97'])
    plt.xticks([0,1],[f'Initial ({n_from})', f'Final ({n_to})'])
    plt.title(title)
    return _save(fig, 'ecrs')
