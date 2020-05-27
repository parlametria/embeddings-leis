import os
import sys
import requests
import pandas as pd
import numpy as np
import argparse
from pathlib import Path
parser = argparse.ArgumentParser(description='Download propositions')
parser.add_argument('--start', help='Date to start downloads from')
parser.add_argument('--end', help='Date to end downloads')
parser.add_argument("--out_dir", required=True, 
                    help='Directory to put downloaded pdfs')

args = parser.parse_args()

out_dir = args.out_dir
df = pd.read_csv("data/proposicoes-2020.csv", sep=';')
df = df.dropna(subset=['urlInteiroTeor'])
df = df[df['siglaTipo'].isin(['PEC','PL','PLP','MPV','PLV','PDL','PRC'])]

print(df.keys())
print(df.head())
print(df[df['ultimoStatus_dataHora'] > '2020-04-01'])
print(df.head())
for i, line in df.iterrows():
    print(line)
    id_prop = line['id']
    url = line['urlInteiroTeor']
    print(url)
    if url is np.nan:
        continue
    response = requests.get(url)
    with open(f'{out_dir}/{id_prop}.pdf', 'wb') as f:
        f.write(response.content)

