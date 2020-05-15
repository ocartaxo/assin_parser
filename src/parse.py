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

FILES_LOCATION = 'dataset/xml'

MODES = namedtuple('MODER', ['r', 'w'])

MODES = MODES(r=stat.S_IREAD, w=stat.S_IWRITE)

logger = logging.getLogger()

def parse_xml(file_path):


    file_path = '/'.join([FILES_LOCATION, file_path])
    logger.info("Parsing xml file")
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

    logging.info("Dataframe created.")
    
    return df


def save_as_csv(df: pd.DataFrame, file_path: str):
    logging.info(f"Saving dataframe in {file_path}")
    file_path = file_path.replace('xml', 'csv')

    if 'csv' not in os.listdir('dataset'):
      #  os.chmod(r'dataset/csv', mode=MODES.w)
        os.mkdir(r'dataset/csv')

    with open(file_path, mode='w+', encoding='utf-8', newline="") as f:
        df.to_csv(f, index=False)

    # logging.info("Dataframe saved.")

def build_dataset(args: Optional[ArgumentParser]=None):

    files_name = os.listdir(FILES_LOCATION)
    for f in files_name:
        parsed_file = parse_xml(f)
        df = create_df(parsed_file)
        save_as_csv(df, os.path.join(FILES_LOCATION, f))

def main(args):
    build_dataset(args)

    logger.info("FIM.")

if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("-j", "--join", help="join european portuguese dataset into brazilian dataset")
    parser.add_argument("-s", "--save", help="salva o dataset em um diretório")
    args = parser.parse_args()


    main(args)
