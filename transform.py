import argparse
import logging

import numpy as np
import pandas as pd
import yaml
from fuzzywuzzy import fuzz

pd.set_option('display.max_columns', 5000)
pd.set_option('display.max_rows', 5000)
logging.basicConfig(format='%(message)s', level=logging.INFO)

DEFAULT_OUTPUT_FILE = 'output.csv'

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='filename of csv file')
parser.add_argument('-t', '--type', type=str, help='type of the file (e.g. sparkasse,dkb)')
parser.add_argument('-o', '--output', type=str, help='name of the output file (default is output.csv)',
                    default=DEFAULT_OUTPUT_FILE)

args = parser.parse_args()

logging.info("Running the extraction job for file {} of type {}".format(args.filename, args.type))
setup_file = 'conf/' + args.type + '.yaml'

logging.info("Loading setup file from  {}".format(setup_file))
with open(setup_file) as stream:
    try:
        setup = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise Exception('Could not read file {}'.format(setup_file))

mapping = setup['mapping']
df = pd.read_csv(args.filename, delimiter=';', quotechar='"', encoding="ISO-8859-1")

df = df[list(mapping.keys())]

df.rename(columns=mapping,
          inplace=True)
field_name = 'Category'
df[field_name] = np.nan
for option in setup['categories']:
    title_to_give = option['title']
    for rule in option['rules']:
        if rule['exact']:
            df[field_name] = df.apply(
                lambda row: title_to_give if rule['input'] in row[rule['field']] else row[field_name], axis=1)
        else:
            df[field_name] = df.apply(
                lambda row: title_to_give if fuzz.partial_ratio(str(rule['input']).lower(),
                                                                str(row[rule['field']]).lower()) == 100 else
                row[field_name], axis=1)
df['Amount'] = df['Amount'].apply(lambda x: x.replace(',', '.')).astype(float)

logging.info("Exported file of {} rows and {} columns.".format(df.shape[0], df.shape[1]))
df.to_csv(DEFAULT_OUTPUT_FILE, encoding='utf-8')
