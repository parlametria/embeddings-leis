import textract
import re
import argparse
import os
from numpy import nan
from tqdm import tqdm
from sys import stderr


NEW_LINE = '\n'
HEADER = 'arquivo;id;numero;tipo;texto_anterior;justificativa'
REGEX = r'\s*(justificativa|justificação)\s*'


def extract_text(file_name):
    text = textract.process(file_name)
    text = text.decode('utf-8')
    text = text.replace(NEW_LINE, ' ')
    return text


def handle_file_name(file_name):
    id, numero, tipo = file_name[:-4].split('_')
    return(id, numero, tipo)


def get_justifications(path, header):
    justified_files = 0
    if header:
        print(HEADER)
    for file_name in tqdm(os.listdir(path)):
        file_path = os.path.join(path, file_name)
        text = extract_text(file_path)
        file_name = file_name.split('/')[-1]
        id, numero, tipo = handle_file_name(file_name)
        previous, justification = split_text(text)
        justified_files += 0 if justification is nan else 1
        print(
            f'{file_name};{id};{numero};{tipo};"{previous}";"{justification}"'
        )
    print_console(
        f'{justified_files} arquivos tiveram justificativa encontrada.'
    )


def split_text(text):
    pattern = re.compile(REGEX, flags=re.I)
    parts = re.split(pattern, text)
    result = (parts[0], parts[2]) if len(parts) > 1 else (parts[0], nan)
    return result


def print_console(message):
    output = message + NEW_LINE
    stderr.write(output)


def handle_args():
    parser = argparse.ArgumentParser(
        description='Extrai as justificativas dos PDFs de proposições'
    )
    parser.add_argument(
        '--source', dest='source',
        required="True",
        help='Diretório com os PDFs'
    )
    parser.add_argument(
        '--no-header', dest="no_header",
        action='store_true',
        help='Não incluir cabeçalho no arquivo resultante'
    )
    args = parser.parse_args()
    return args


def main():
    args = handle_args()
    path = args.source
    header = not args.no_header
    print_console('Extraindo justificativas.')
    get_justifications(path, header)


if __name__ == "__main__":
    main()
