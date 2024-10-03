import os
import PyPDF2 as pdf
from time import sleep
from sys import exit

"""
TO-DO:
"""


def parse_file(file):
    source_dir = os.path.dirname(__file__)

    try:
        if file.startswith('~'):
            file = os.path.expanduser(file)

        if file.endswith('.txt'):
            if source_dir == '':
                textfile = open(os.path.join(os.getcwd(), file), 'r')
            else:
                textfile = open(os.path.join(source_dir, file), 'r')

            print('|*| Selected: ' + os.path.basename(file))

            return textfile

        elif file.endswith('.pdf'):
            pdf_file = pdf.PdfReader(open(os.path.join(source_dir, file), 'rb'))
            print('|*| Selected: ' + os.path.basename(file))
            return pdf_file
        else:
            return None

    except FileNotFoundError:
        print('[!] File not found error.')
        exit(1)

def crackpdf(wordlist, pdf_file): 
    print('|*| Initializing dictionary attack')

    pdfWriter = pdf.PdfWriter()

    for password in wordlist.read().split():
        #if pdf_file.decrypt(password) == 0:
            #print('Trying: ' + password)

        # Found correct password
        if pdf_file.decrypt(password) == 2:
            print('* * * * * * * * *\n[!] FOUND PASSWORD: ' + password)
            autoDecryption = input('Decrypt the file? [Y/N]: ').lower()

            if autoDecryption == 'y' or autoDecryption == 'yes':
                for page in pdf_file.pages:
                    pdfWriter.add_page(page)

                with open("decrypted.pdf", "wb") as f:
                    pdfWriter.write(f)

                print('[*] File decrypted successfully and saved as decrypted.pdf')
                exit()

            elif autoDecryption == 'n' or autoDecryption == 'no':
                exit()


    if pdf_file.is_encrypted:
        wordlist.close()
        print('\n[!] Password not found in wordlist')
        exit()



def main():
    input_pass = input('Enter path to wordlist: ')
    pass_txt = parse_file(input_pass)

    path_to_pdf = input('Enter path to encrypted PDF: ')
    pdf_file = parse_file(path_to_pdf)

    crackpdf(pass_txt, pdf_file)


if __name__ == '__main__':
    main()
