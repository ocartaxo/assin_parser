import pandas as pd
import numpy as np
import os
import logging
import stat

from typing import Optional
from xml.etree import ElementTree as ET
from argparse import ArgumentParser
from collections import namedtuple
from sklearn.utils import shuffle

MODES = namedtuple('MODER', ['r', 'w'])

MODES = MODES(r=stat.S_IREAD, w=stat.S_IWRITE)

#logger = logging.getLogger()

def parse_xml(file_path):

    tree = ET.parse(file_path)
    root = tree.getroot()
    info_pares_sentencas = list()

    for child in root:
        d = child.attrib
        d.update(T=child[0].text, H=child[1].text)
        
        del d["id"]

        info_pares_sentencas.append(d)

    return info_pares_sentencas

def create_df(L: list):
    logging.info("Creating dataframe")
    df = pd.DataFrame(L)
    df = df.rename(columns={"entailment":"Relacao", "similarity": "Similaridade"})
    #df["Implicação"] = df.Relação.map({"Entailment": "Sim", "None": "Não"})
   
    return df


def save_as_csv(df: pd.DataFrame, file_path: str):
    file_path = file_path.replace('xml', 'csv')
    dir_to_save, _ = file_path.rsplit('/', 1)

    if not os.path.isdir(dir_to_save):
        os.mkdir(dir_to_save)

    with open(file_path, mode='w+', encoding='utf-8', newline="") as f:
        df.to_csv(f, index=False)

def build_dataset(path):

    '''
      path (str): path do xml files
    '''

    files_name = os.listdir(path)
    for f in files_name:
        path_file = os.path.join(path, f)
        parsed_file = parse_xml(path_file)
        df = create_df(parsed_file)
        save_as_csv(df, path_file)

def main(args):
    build_dataset(args)

if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("-j", "--join", help="join european portuguese dataset into brazilian dataset")
    parser.add_argument("-s", "--save", help="salva o dataset em um diretório")
    args = parser.parse_args()


    main(args)
