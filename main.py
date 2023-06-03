

from cyber_signature.pdf import add_sign_page_pdf


if __name__ == '__main__':
    
    pag1_pdf = open('pag1.pdf', 'rb')
    fileobj = add_sign_page_pdf(pag1_pdf, 'Cristian Triana')