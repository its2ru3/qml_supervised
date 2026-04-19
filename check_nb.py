import json
nb = json.load(open('main.ipynb', 'r', encoding='utf-8'))
print('Total cells:', len(nb['cells']))
for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])[:80]
    print(f'  Cell {i}: {c["cell_type"]} | {src}')
