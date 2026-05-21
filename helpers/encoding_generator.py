import os, sys, re, json
from typing import Optional

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from helpers.utils import advanced_preprocess, generate_tokenizer_lookup

corpus = os.path.join(ROOT_DIR, 'data\\original.txt')
outfile = os.path.join(ROOT_DIR, 'encodings\\v3.json')

with open(corpus, 'r', encoding='utf-8') as f:
    data = f.read()

clean_data = advanced_preprocess(data)
encodings = generate_tokenizer_lookup(text=clean_data)

with open(outfile, 'w') as f:
    json.dump(encodings, f, indent=4)
    print('Completed')
    