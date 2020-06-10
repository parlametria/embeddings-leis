import textract
import re
import argparse
import os
from numpy import nan
from tqdm import tqdm
from sys import stderr
from pathlib import Path


NEW_LINE = '\n'
HEADER = 'arquivo|id|numero|tipo|"texto_anterior"|"justificativa"'
REGEX = r'\s*(justificativa|justificação)\s*'


def extract_text(file_name):
    text = textract.process(file_name)
    text = text.decode('utf-8')
    text = text.replace(NEW_LINE, ' ')
    text = text.strip()
    return text


def handle_file_name(file_name):
    id, numero, tipo = Path(file_name).stem.split('_')
    return(id, numero, tipo)


def get_justifications(path, header):
    justified_files = 0
    if header:
        print(HEADER)
    for file_name in tqdm(os.listdir(path)):
        file_path = os.path.join(path, file_name)
        try:
            file_name = file_name.split('/')[-1]
            id, numero, tipo = handle_file_name(file_name)
            text = extract_text(file_path)
            previous, justification = split_text(text)
            justified_files += 0 if justification is nan else 1
            print(
                f'{file_name}|{id}|{numero}|{tipo}|"{previous}"|"{justification}"'
            )
        except textract.exceptions.ShellError:
            print(
                f'{file_name}|{id}|{numero}|{tipo}|"{nan}"|"{nan}"'
            )
    print_console(
        f'{justified_files} arquivos tiveram justificativa encontrada.'
    )


def split_text(text):
    pattern = re.compile(REGEX, flags=re.I)
    parts = re.split(pattern, text)
    if len(parts) > 1 and is_not_empty(parts[0]) and is_not_empty(parts[2]):
        result = (parts[0], parts[2])
    elif len(parts) == 1 and is_not_empty(parts[0]):
        result = (parts[0], nan)
    else:
        result = (nan, nan)
    return result


def is_not_empty(text):
    return bool(text and text.strip())


def print_console(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


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
