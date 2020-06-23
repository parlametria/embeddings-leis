import os
import sys
import time
import requests
import pandas as pd
import numpy as np
import argparse
import filetype
from pathlib import Path

def handle_args():
    parser = argparse.ArgumentParser(description='Download propositions')
    parser.add_argument('--start', help='Date to start downloads from')
    parser.add_argument('--end', help='Date to end downloads')
    parser.add_argument("--out_dir", required=True,
                        help='Directory to put downloaded pdfs')
    return parser.parse_args()

def subset_dataset(df, start, end):
    df = df[df['ultimoStatus_dataHora'] > start]
    df = df[df['ultimoStatus_dataHora'] < end]

    df = df[df['siglaTipo'].isin(['PEC', 'PL', 'PLP',
                                  'MPV', 'PLV', 'PDL',
                                  'PRC', 'REQ', 'RIC'])]

    df = df.reset_index(drop=True)
    return df

def main():
    args = handle_args()
    start = args.start
    end = args.end
    out_dir = args.out_dir
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    already_downloaded = set(os.listdir(out_dir))
    df = pd.read_csv("data/propositions.csv", sep=';')
    print(df.shape)
    df = subset_dataset(df, start, end)
    print(df.shape)
    # df = df.dropna(subset=['urlInteiroTeor'])

    files_downloaded = 0
    files_in_directory = 0
    invalid_urls = 0
    nonetype = 0
    conn_error = []
    for i, line in df.iterrows():
        id_prop = line['id']
        proposal_num = line['numero']
        proposal_type = line['siglaTipo']
        url = line['urlInteiroTeor']
        if i % 1000 == 0:
            print(f'{i} / {df.shape} files downloaded')

        # if f'{id_prop}_{proposal_num}_{proposal_type}.pdf' in already_downloaded:
        #     files_in_directory += 1
        #     continue

        if url is np.nan:
            invalid_urls += 1
            continue

        try:
            response = requests.get(url)
            # print(file_type)
        except requests.exceptions.ConnectionError:
            conn_error.append(url)

        try:
            file_type = filetype.guess(response.content)
            with open(f'{out_dir}/{id_prop}_{proposal_num}_{proposal_type}.{file_type.extension}', 'wb') as f:
                f.write(response.content)
                files_downloaded += 1
                already_downloaded.add(f'{id_prop}_{proposal_num}_{proposal_type}.pdf')
            # time.sleep(0.5)
        except:
            print("NoneType on response")
            nonetype += 1

    print(f'Connection Error on these files: {conn_error}')
    print(f"Downloaded {files_downloaded} files")
    print(f"There were already {files_in_directory} files downloaded")
    print(f"There were {invalid_urls} invalid URL's on the dataset")
    print(f"There were {nonetype} invalid responses from URL")

if __name__=="__main__":
    main()
