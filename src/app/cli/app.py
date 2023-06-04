from pathlib import Path
from typing import IO
from cyber_signature.pdf import add_sign_page_pdf
import typer
from typing_extensions import Annotated
app = typer.Typer()

def sign_pdf(pdf_file: IO):
    extra_page = typer.confirm(
        text="Do you want an extra page inside the pdf with a custom signature and the date?",
        default=False
    )
    if extra_page:
        # Firma con página extra
        signature = typer.prompt("Please specify the name in the signature (e.g. John Doe)")
        add_sign_page_pdf(pdf_file, signature)
    else:
        # Firma sin página extra TODO
        pass

@app.command()
def sign(
    file_path: Annotated[
        str, 
        typer.Argument(help="The path of the file to sign.")
        ],
    pdf: Annotated[
        bool, 
        typer.Option(help="Specify if you want to sign a pdf file in the metadata.")
        ] = False
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
    
    file_to_sign = open(str(path), 'rb')
    
    #Now we verify if the file is pdf
    if pdf:
        sign_pdf(file_to_sign)
    else:
        print("se firmó el archivo, se han guardado la firma y la llave pública")
    
    file_to_sign.close()
    


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")
