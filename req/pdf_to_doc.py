'pip install pdf2docx'

from pdf2docx import Converter
def pdf_converter_docx(pdf:str):
    docx_file = f'{pdf.split(".")[0]}.docx'
    cv = Converter(pdf)
    cv.convert(docx_file)
    cv.close()
    return docx_file