import os
import sys
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--start", type=int, help='Begin downloads from aaaa year')
parser.add_argument("--end", type=int, help='End downloads from aaaa year')
args = parser.parse_args()

start = args.start
end = args.end

if end < start:
    raise ValueError("Start date should be smaller than end date")
    sys.exit()

df = None

print(os.listdir('.'))

for year in range(start, end):
    url_base = f'https://dadosabertos.camara.leg.br/arquivos/proposicoes/csv/proposicoes-{year}.csv'
    if df is None:
        df = pd.read_csv(url_base, sep=';')
        df = df[['id', 'siglaTipo', 'numero', "ultimoStatus_dataHora",
                 'ano', 'codTipo', 'descricaoTipo',
                 'ementa', 'ementaDetalhada', 'keywords',
                 'dataApresentacao', 'urlInteiroTeor']]
    else:
        aux = pd.read_csv(url_base, sep=';')
        aux = aux[['id', 'siglaTipo', 'numero', "ultimoStatus_dataHora",
                 'ano', 'codTipo', 'descricaoTipo',
                 'ementa', 'ementaDetalhada', 'keywords',
                 'dataApresentacao', 'urlInteiroTeor']]
        df = pd.concat([aux, df])

    print(df.shape)

df.to_csv("data/proposicoes_final.csv", sep=';')
