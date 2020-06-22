import sys
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--start", type=int, help='Begin downloads from aaaa year')
parser.add_argument("--end", type=int, help='End downloads from aaaa year')
args = parser.parse_args()

start = args.start
end = args.end

if start < 2000 or end < 2000:
    raise ValueError("There are only propositions from 2000 forward")

if start > 2020 or end > 2020:
    raise ValueError("Cannot get propositions from the future")

if end < start:
    raise ValueError("Start date should be smaller than end date")

df = None

dtypes = {
    'id': 'int64',
    'uri': 'object',
    'siglaTipo': 'object',
    'numero': 'int64',
    'ano': 'int64',
    'codTipo': 'int64',
    'descricaoTipo': 'object',
    'ementa': 'object',
    'ementaDetalhada': 'object',
    'keywords': 'object',
    'dataApresentacao': 'object',
    'uriOrgaoNumerador': 'object',
    'uriPropAnterior': 'float64',
    'uriPropPrincipal': 'object',
    'uriPropPosterior': 'object',
    'urlInteiroTeor': 'object',
    'urnFinal': 'float64',
    'ultimoStatus_dataHora': 'object',
    'ultimoStatus_sequencia': 'int64',
    'ultimoStatus_uriRelator': 'object',
    'ultimoStatus_idOrgao': 'float64',
    'ultimoStatus_siglaOrgao': 'object',
    'ultimoStatus_uriOrgao': 'object',
    'ultimoStatus_regime': 'object',
    'ultimoStatus_descricaoTramitacao': 'object',
    'ultimoStatus_idTipoTramitacao': 'int64',
    'ultimoStatus_descricaoSituacao': 'object',
    'ultimoStatus_idSituacao': 'float64',
    'ultimoStatus_despacho': 'object',
    'ultimoStatus_url': 'object',
}

for year in range(start, end+1):
    url_base = f'https://dadosabertos.camara.leg.br/arquivos/proposicoes/csv/proposicoes-{year}.csv'
    if df is None:
        df = pd.read_csv(url_base, sep=';', dtype=dtypes)
    else:
        df = pd.concat([pd.read_csv(url_base, sep=';', dtype=dtypes), df])

print(df.iloc[:5, 14])
print(df.keys())
print(df.dtypes)
# df = df.astype(dtype= {})
df.to_csv("data/propositions.csv", sep='|', line_terminator='\n')
