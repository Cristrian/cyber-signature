from datetime import datetime
from pathlib import Path
from typing import IO

from pypdf import PdfMerger
from reportlab.pdfgen import canvas


def clean_path_name(path_str: str):
    cleaned = path_str.split("/")[-1]
    return cleaned


def add_page_pdf(original_pdf: IO, page_to_add: IO, new_pdf: IO):
    # Añade una página al pdf
    merger = PdfMerger()
    merger.append(fileobj=original_pdf)
    merger.append(fileobj=page_to_add)
    merger.write(fileobj=new_pdf)


def create_signed_page(signature_text: str):
    # Crea la página firmada
    c = canvas.Canvas("temp_files/sign_page.pdf")
    today_date = datetime.now().isoformat()
    c.drawString(200, 450, signature_text)
    c.drawString(200, 430, today_date)
    c.showPage()
    c.save()


def remove_all(root: Path):
    for path in root.iterdir():
        if path.is_file():
            print(f"Deleting the file: {path}")
            path.unlink()
        else:
            remove_all(path)
    print(f"Deleting the empty dir: {root}")
    root.rmdir()


def add_sign_page_pdf(pdf_to_sign: IO, signature_text: str):
    path = Path("temp_files")
    path.mkdir()
    create_signed_page(signature_text)
    page_to_add = open("temp_files/sign_page.pdf", "rb")
    filename = clean_path_name(pdf_to_sign.name)
    signed_pdf = open(f"signed_{filename}", "wb")
    add_page_pdf(original_pdf=pdf_to_sign, page_to_add=page_to_add, new_pdf=signed_pdf)
    page_to_add.close()
    signed_pdf.close()
    # Clean temp files

    remove_all(path)


def verify_is_pdf(pdf):
    pass