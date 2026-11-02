import re

with open(r'd:\Facultad\Economia politica 2026\Economía Política Sede Córdoba Unidad 6\2. Linea de tiempo - texto.txt', 'r', encoding='utf-8') as f:
    content = f.read()

pages = content.split('--- PÁGINA ')

sections = {}

# Check which pages have good content for each section
keywords = {
    'timeline': [1],
    'seggiaro_intro': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
    'alfonsin_seggiaro': [22, 24, 26, 28, 30, 32, 34, 36, 38],
    'menem1_seggiaro': [40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88],
    'rapoport_intro': [90, 92, 94, 96],
    'rapoport_privatizaciones': [98, 100, 102, 104],
    'rapoport_reformas': [106, 108, 110, 112, 114, 116, 118, 120, 122],
}

for section, page_nums in keywords.items():
    print(f'\n{"="*60}')
    print(f'SECTION: {section}')
    print(f'{"="*60}')
    for n in page_nums:
        if n >= len(pages):
            continue
        text = pages[n]
        clean = re.sub(r'[^a-zA-Z\s,.\d%$();:/\-]', '', text)
        lines = [l.strip() for l in clean.split('\n') if len(l.strip()) > 50]
        if lines:
            print(f'\n--- Page {n} ---')
            for l in lines[:5]:
                print(f'  {l[:150]}')
