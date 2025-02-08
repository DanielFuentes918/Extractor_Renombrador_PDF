import os
import re
import tkinter as tk
from tkinter import filedialog
import PyPDF2
import pytesseract

# Configura la ruta de Tesseract y la variable de entorno TESSDATA_PREFIX
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

# Intentamos importar la librería para OCR
try:
    from pdf2image import convert_from_path
except ImportError:
    print("Para usar OCR, instala pdf2image y pytesseract:\n  pip install pdf2image pytesseract")
    pytesseract = None
    convert_from_path = None

def sanitize_filename(filename):
    """Elimina caracteres no válidos para nombres de archivo en Windows."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def extraer_texto_pdf(ruta_pdf):
    """
    Intenta extraer texto usando PyPDF2. Si no se obtiene texto (por ejemplo, porque el PDF es escaneado),
    se intenta extraer texto mediante OCR usando pdf2image y pytesseract.
    """
    texto_completo = ""
    # Intento de extracción con PyPDF2
    try:
        with open(ruta_pdf, "rb") as archivo:
            lector = PyPDF2.PdfReader(archivo)
            for pagina in lector.pages:
                texto = pagina.extract_text()
                if texto:
                    texto_completo += texto + "\n"
    except Exception as e:
        print(f"Error al extraer con PyPDF2 de {ruta_pdf}: {e}")
    
    if not texto_completo.strip():
        print("No se extrajo texto con PyPDF2. Intentando con OCR...")
        if convert_from_path and pytesseract:
            try:
                # Especifica la ruta a la carpeta 'bin' de Poppler
                poppler_path = r"C:\Users\Sistemas2\Desktop\Antecedentes _Penales_Script\poppler-24.08.0\Library\bin"
                paginas = convert_from_path(ruta_pdf, dpi=300, poppler_path=poppler_path)
                for i, pagina in enumerate(paginas):
                    texto = pytesseract.image_to_string(pagina, lang="spa")
                    texto_completo += texto + "\n"
                    print(f"OCR - Texto extraído de la página {i+1}:\n{texto}\n")
            except Exception as e:
                print(f"Error al extraer con OCR de {ruta_pdf}: {e}")
        else:
            print("No se tienen las librerías necesarias para OCR.")
    
    return texto_completo

def extraer_datos(ruta_pdf):
    """
    Extrae el texto del PDF y luego busca los valores que siguen a las etiquetas
    "NOMBRES:", "APELLIDOS:" y "DOCUMENTO DE IDENTIDAD:".
    Retorna una tupla (nombres, apellidos, documento) o ('', '', '') si no se encuentran.
    """
    texto_completo = extraer_texto_pdf(ruta_pdf)
    
    # Imprime el texto extraído para su verificación
    print(f"\nTexto extraído de {ruta_pdf}:\n{'-'*60}\n{texto_completo}\n{'-'*60}")
    
    # Patrón combinado que captura los tres campos.
    # Se usa re.DOTALL para que el . incluya saltos de línea si fuera necesario.
    patron = r"NOMBRES:\s*(?P<nombres>.*?)\s*APELLIDOS:\s*(?P<apellidos>.*?)\s*DOCUMENTO DE IDENTIDAD:\s*(?P<documento>[^\n]+)"
    m = re.search(patron, texto_completo, re.IGNORECASE | re.DOTALL)
    
    if m:
        nombres = m.group("nombres").strip().upper()
        apellidos = m.group("apellidos").strip().upper()
        documento = m.group("documento").strip().upper()
    else:
        nombres, apellidos, documento = "", "", ""
    
    return nombres, apellidos, documento

def main():
    # Inicializa tkinter y oculta la ventana principal
    root = tk.Tk()
    root.withdraw()

    # Abre el diálogo para seleccionar archivos PDF
    rutas_pdf = filedialog.askopenfilenames(
        title="Selecciona los archivos PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    if not rutas_pdf:
        print("No se seleccionaron archivos.")
        return

    for ruta in rutas_pdf:
        print(f"\nProcesando: {ruta}")
        nombres, apellidos, documento = extraer_datos(ruta)

        if nombres and apellidos and documento:
            # Genera el nuevo nombre de archivo y lo sanitiza
            nuevo_nombre = f"{nombres} {apellidos} {documento}.pdf"
            nuevo_nombre = sanitize_filename(nuevo_nombre)
            ruta_directorio = os.path.dirname(ruta)
            ruta_nueva = os.path.join(ruta_directorio, nuevo_nombre)
            
            try:
                os.rename(ruta, ruta_nueva)
                print(f"Archivo renombrado a: {ruta_nueva}")
            except Exception as e:
                print(f"Error al renombrar {ruta}: {e}")
        else:
            print(f"No se encontraron los campos 'NOMBRES:', 'APELLIDOS:' y 'DOCUMENTO DE IDENTIDAD:' en {ruta}")

if __name__ == "__main__":
    main()
