import pandas as pd
import numpy as np
import os

from xml.etree import ElementTree as ET
from argparse import ArgumentParser
from collections import namedtuple
from sklearn.utils import shuffle

ROOT_NAME = "assin-pt{0}-"

# FILE_FOR_TEST = 'dataset/xml/read_test.xml'
FILES_LOCATION = '../dataset/xml/{0}/{1}'

FOLDERS = namedtuple('FOLDERS', ['eu', 'br', 'eubr'])

FOLDERS = FOLDERS(
    eu=FILES_LOCATION.format("EU", ROOT_NAME.format("pt")),
    br=FILES_LOCATION.format("BR", ROOT_NAME.format("br")),
    eubr = FILES_LOCATION.format("EUBR", ROOT_NAME.format("eubr"))
)


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



def create_df(L):
    df = pd.DataFrame(L)

    df = df.rename(columns={"entailment":"Relacao", "similarity": "Similaridade"})

    #df["Implicação"] = df.Relação.map({"Entailment": "Sim", "None": "Não"})

    return df


def save_df(df: pd.DataFrame, file_path: str):

    file_path = file_path.replace('xml', 'csv')

    with open(file_path, mode='w+', encoding='utf-8', newline="") as f:
        df.to_csv(f, index=False)


def build_dataset(args):
    if args.pt:
        pt_dataset = parse_xml(FOLDERS.pt)
        br_dataset = parse_xml(FOLDERS.br)
        
        corpus = br_dataset + pt_dataset
        corpus = shuffle(np.array(corpus))
        corpus = create_df(corpus)
        
        return corpus



    return create_df(parse_xml(FOLDERS.br))


def main(args):
    build_dataset(args)

    print("FIM.")

if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("-j", "--join", help="join european portuguese dataset into brazilian dataset")
    args = parser.parse_args()


    main(args)
