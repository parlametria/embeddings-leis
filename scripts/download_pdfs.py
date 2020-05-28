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

start = args.start
end = args.end
out_dir = args.out_dir
df = pd.read_csv("data/proposicoes-2020.csv", sep=';')
# df = df.dropna(subset=['urlInteiroTeor'])
df = df[df['ultimoStatus_dataHora'] > start]
df = df[df['ultimoStatus_dataHora'] < end]

df = df[df['siglaTipo'].isin(['PEC','PL','PLP','MPV','PLV','PDL','PRC'])]

files_downloaded = 0
files_in_directory = 0
invalid_urls = 0
for i, line in df.iterrows():
    id_prop = line['id']
    if f'{id_prop}.pdf' in os.listdir(out_dir):
        files_in_directory += 1
        continue
    url = line['urlInteiroTeor']
    if url is np.nan:
        invalid_urls += 1
        continue

    response = requests.get(url)
    with open(f'{out_dir}/{id_prop}.pdf', 'wb') as f:
        f.write(response.content)
        files_downloaded += 1

print(f"Downloaded {files_downloaded} files")
print(f"There were already {files_in_directory} files downloaded")
print(f"There were {invalid_urls} invalid URL's on the dataset")
