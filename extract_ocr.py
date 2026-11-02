import fitz
import pytesseract
from PIL import Image
import io
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = os.path.join(os.environ['TEMP'], 'tessdata')

pdf_path = r'd:\Facultad\Economia politica 2026\Economía Política Sede Córdoba Unidad 6\3.1 Material Kirchnerismo.pdf'
output_path = r'd:\Facultad\Economia politica 2026\Economía Política Sede Córdoba Unidad 6\3.1 Material Kirchnerismo - texto.txt'

doc = fitz.open(pdf_path)
total = doc.page_count

with open(output_path, 'w', encoding='utf-8') as f:
    for i in range(total):
        page = doc[i]
        pix = page.get_pixmap(dpi=200)
        img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img, lang='spa')
        f.write(f'--- PÁGINA {i+1} ---\n')
        f.write(text)
        f.write('\n\n')
        if (i+1) % 10 == 0:
            print(f'Procesadas {i+1}/{total} páginas')

doc.close()
print(f'OCR completado. Texto guardado en: {output_path}')
