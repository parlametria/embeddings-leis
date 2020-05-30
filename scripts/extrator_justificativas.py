import os
import textract
import re
import pandas as pd
from sys import argv
from tqdm import tqdm


def extract_text(path, files):
    base = {
        'arquivo': [],
        'texto_anterior': [],
        'justificativa': []
    }
    for file_name in tqdm(files):
        text = textract.process(path + '/' + file_name)
        text = text.decode('utf-8')
        previous, justification = split_text(text)
        base['arquivo'].append(file_name)
        base['texto_anterior'].append(previous)
        base['justificativa'].append(justification)
    return base


def split_text(text):
    pattern = r'JUSTIFICATIVA|JUSTIFICAÇÃO|Justificativa'
    parts = re.split(pattern, text)
    result = (parts[0], parts[1]) if len(parts) > 1 else (parts[0], 'N/A')
    return result


def create_csv(base, output_filename):
    df = pd.DataFrame(base)
    df.to_csv(output_filename + '.csv', index=False)


def main():
    args = argv[1:]
    path = args[0]
    output_filename = args[1]
    files = os.listdir(path)
    print(f'Foram encontrados {len(files)} arquivos')
    print('Extraindo textos')
    base = extract_text(path, files)
    create_csv(base, output_filename)
    print(f'Pronto! O arquivo {output_filename}.csv foi criado')


if __name__ == "__main__":
    main()
