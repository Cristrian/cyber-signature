from pathlib import Path

import cyber_signature.pdf as pdf_signer
import typer
from typing_extensions import Annotated

app = typer.Typer()


def sign_pdf(pdf_file: Path):
    extra_page = typer.confirm(
        text="Do you want an extra page inside the pdf with a custom signature and the date?",
        default=False,
    )

    file_to_sign = pdf_file

    if extra_page:
        # Firma con página extra
        signature = typer.prompt(
            "Please specify the name in the signature (e.g. John Doe)"
        )
        file_to_sign = pdf_signer.add_sign_page_pdf(pdf_file, signature)

    return file_to_sign


@app.command()
def sign(
    file_path: Annotated[str, typer.Argument(help="The path of the file to sign.")],
    pdf: Annotated[
        bool,
        typer.Option(help="Specify if you want to sign a pdf file in the metadata."),
    ] = False,
):
    """
    Signs the file in FILE_PATH
    """
    # path = Path('/home/cristiantriana/Documents/Maestria/pag1.pdf')
    path = Path(file_path)
    path.is_file()
    "Validate if the path exists"
    if not path.exists():
        print(f"The path '{file_path}' was not found.")
        raise typer.Exit(1)
    "Validates if the path is a file"
    if not path.is_file():
        print(f"The path '{file_path}' is not a file.")
        raise typer.Exit(1)

    file_to_sign = path

    if pdf:
        file_to_sign = sign_pdf(path)

    # Firma el archivo
    signed_file = pdf_signer.sign_pdf(file_to_sign)

    print(f"El archivo firmado se encuentra en: {file_to_sign}")
    print(f"La firma se encuentra en el archivo: {signed_file}")
    print(f"La llave pública se encuentra en el archivo: {signed_file.stem}.pub")


@app.command()
def verify(
    file_path: Annotated[str, typer.Argument(help="The path of the file to verify.")],
):
    """
    Verifies the file in FILE_PATH
    """
    # path = Path('/home/cristiantriana/Documents/Maestria/pag1.pdf')
    path = Path(file_path)
    path.is_file()
    "Validate if the path exists"
    if not path.exists():
        print(f"The path '{file_path}' was not found.")
        raise typer.Exit(1)
    "Validates if the path is a file"
    if not path.is_file():
        print(f"The path '{file_path}' is not a file.")
        raise typer.Exit(1)

    if pdf_signer.verify_pdf(path):
        print("La firma es válida")
    else:
        print("La firma no es válida")



