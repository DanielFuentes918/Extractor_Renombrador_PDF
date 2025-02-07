# Renombrado Automático de PDFs de Antecedentes Penales

Este proyecto es un script en Python que automatiza el proceso de renombrar archivos PDF de antecedentes penales. El script extrae información clave del contenido de cada PDF (usando *PyPDF2* y, en caso necesario, OCR mediante *pdf2image* y *pytesseract*) y renombra el archivo con los datos extraídos. En concreto, se extraen los siguientes campos:

- **NOMBRES:**
- **APELLIDOS:**
- **DOCUMENTO DE IDENTIDAD:**

El archivo resultante se renombra siguiendo el formato:  
`<NOMBRES> <APELLIDOS> <DOCUMENTO DE IDENTIDAD>.pdf`  
Además, el nombre se **sanitiza** para eliminar caracteres no válidos en Windows.

---

## Requisitos

- **Python 3**
- **Librerías Python:**
  - [PyPDF2](https://pypi.org/project/PyPDF2/)
  - [pytesseract](https://pypi.org/project/pytesseract/)
  - [pdf2image](https://pypi.org/project/pdf2image/)
  - **tkinter** (generalmente incluido con Python)

- **Tesseract OCR:**  
  Se debe instalar Tesseract OCR y asegurarse de que el ejecutable se encuentre en la ruta especificada o en el PATH del sistema.  
  [Descargar Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

- **Poppler:**  
  Necesario para que `pdf2image` pueda convertir las páginas del PDF a imágenes. Puedes descargar una versión precompilada para Windows, por ejemplo, desde [poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases).  
  Si prefieres, puedes agregar la carpeta `bin` de Poppler a la variable de entorno PATH o especificar su ruta en el script.

---

## Instalación

1. **Instalar Python 3:**  
   Descarga e instala Python 3 desde la [página oficial](https://www.python.org/).

2. **Instalar las dependencias de Python:**  
   Ejecuta en la terminal:
   ```bash
   pip install PyPDF2 pdf2image pytesseract
   
3. **Instalar Tesseract OCR:**
   Descarga e instala Tesseract OCR para Windows.  
   Asegúrate de que la ruta de instalación (por ejemplo, `C:\Program Files\Tesseract-OCR\tesseract.exe`) esté configurada.  
   Puedes configurar la ruta de Tesseract en el script con:
  
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

