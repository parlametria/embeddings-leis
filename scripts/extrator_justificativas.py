import textract
import re
import argparse
import os
import pandas as pd
from numpy import nan
from tqdm import tqdm
from pathlib import Path


NEW_LINE = '\n'
REGEX = r'\s*(justificativa|justificação)\s*'


def extract_text(file_name):
    try:
        text = textract.process(file_name)
        text = text.decode('utf-8')
        text = text.replace(NEW_LINE, ' ')
        text = text.strip()
    except textract.exceptions.ShellError:
        text = ''
    return text


def handle_file_name(file_name):
    id, numero, tipo = Path(file_name).stem.split('_')
    return(id, numero, tipo)


def get_justifications(path, header):
    data = {
        'file_name': [],
        'id': [],
        'numero': [],
        'tipo': [],
        'texto_anterior': [],
        'justificativa': []
    }
    justified_files = 0
    for file_name in tqdm(os.listdir(path)):
        file_path = os.path.join(path, file_name)
        file_name = file_name.split('/')[-1]
        id, numero, tipo = handle_file_name(file_name)
        text = extract_text(file_path)
        previous, justification = split_text(text)
        justified_files += 0 if justification is nan else 1
        data['file_name'].append(file_name)
        data['id'].append(id)
        data['numero'].append(numero)
        data['tipo'].append(tipo)
        data['texto_anterior'].append(previous)
        data['justificativa'].append(justification)
    print(f'{justified_files} arquivos tiveram justificativa encontrada.')
    return data


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
        '--no-header', dest='no_header',
        action='store_true',
        help='Não incluir cabeçalho no arquivo resultante'
    )
    parser.add_argument(
        dest='file_name',
        help='Nome do arquivo com justificativas'
    )
    args = parser.parse_args()
    return args


def main():
    args = handle_args()
    path = args.source
    header = not args.no_header
    result_file = args.file_name
    print('Extraindo justificativas.')
    justificativas = get_justifications(path, header)
    df = pd.DataFrame(justificativas)
    df.to_csv(result_file, sep=';', index=False, header=header)


if __name__ == "__main__":
    main()
