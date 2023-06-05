from datetime import datetime
from pathlib import Path
from typing import IO

from pypdf import PdfMerger, PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from cryptography.hazmat.primitives import serialization

from .signature_service import sign, verify


def clean_path_name(path_str: str):
    cleaned = path_str.split("/")[-1]
    return cleaned


def add_page_pdf(original_pdf: IO, page_to_add: IO, new_pdf: IO):
    # Añade una página al pdf
    merger = PdfMerger()
    merger.append(fileobj=original_pdf)
    merger.append(fileobj=page_to_add)
    merger.write(fileobj=new_pdf)


def create_signed_page(signature_text: str, path: Path):
    # Crea la página firmada
    c = canvas.Canvas(str(path))
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


def add_sign_page_pdf(pdf_to_sign: Path, signature_text: str) -> Path:
    tmp = Path("temp_files")
    tmp.mkdir()
    signature_page = tmp / "sign_page.pdf"
    create_signed_page(signature_text, signature_page)

    input_filename = clean_path_name(pdf_to_sign.name)
    signed_pdf_path = Path(f"signed_{input_filename}")

    with signature_page.open("rb") as page_to_add:
        with signed_pdf_path.open("wb") as signed_pdf:
            add_page_pdf(original_pdf=pdf_to_sign, page_to_add=page_to_add, new_pdf=signed_pdf)

    # Clean temp files
    remove_all(tmp)

    return signed_pdf_path 


def sign_pdf(pdf_file: Path) -> Path:
    """Sign a pdf file and store files with the signature and the public key."""

    # Sign the pdf
    with pdf_file.open("rb") as pdf:
        signature, private_key = sign(pdf.read())

    public_key = private_key.public_key()

    # Write the signature and the public key to files
    signature_file = Path(f"{pdf_file.stem}.sig")
    public_key_file = Path(f"{pdf_file.stem}.pub")

    with signature_file.open("wb") as sig:
        sig.write(signature)
    
    with public_key_file.open("wb") as pub:
        pub.write(public_key.public_bytes_raw())
    
    return signature_file

def verify_pdf(pdf_file: Path) -> bool:
    """Verify the signature of a pdf file."""

    # Read the signature and the public key from files
    signature_file = Path(f"{pdf_file.stem}.sig")
    public_key_file = Path(f"{pdf_file.stem}.pub")

    with signature_file.open("rb") as sig:
        signature = sig.read()

    with public_key_file.open("rb") as pub:
        public_key = pub.read()

    # Verify the signature
    with pdf_file.open("rb") as pdf:
        return verify(pdf.read(), signature, public_key)