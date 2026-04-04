import os, sys, re, json
from typing import Optional

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from extras.utils import simple_preprocess

class SimpleTokenizer():
    def __init__(self, encodings:Optional[str] = None) -> None:
        if encodings is not None:
            if os.path.exists(encodings) and encodings.endswith('.json'):
                with open(encodings, 'r') as f:
                    self.encodings = json.load(f)
            
            else:
                raise ValueError('Encodings file must be a .json file and must exist.')

        else:
            encoding_file = os.path.join(ROOT_DIR, 'encodings', 'v2.json')
            if os.path.exists(encoding_file):
                with open(encoding_file, 'r') as f:
                    self.encodings = json.load(f)

            else:
                raise ValueError('Default encodings file not found. Please provide a valid encodings file.')
            

    def encode(self, text:str) -> list[int]:
        preprocessed = simple_preprocess(text)
        tokens = preprocessed.split()
        return [self.encodings.get(token, self.encodings[' ']) for token in tokens]
    

    def decode(self, token_ids:list[int]) -> str:
        reverse_lookup = {v: k for k, v in self.encodings.items()}
        tokens = [reverse_lookup.get(token_id, ' ') for token_id in token_ids]
        return ' '.join(tokens)
    

if __name__ == '__main__':
    tokenizer = SimpleTokenizer()
    text = "Hello, world! This is a test."
    encoded = tokenizer.encode(text)
    print("Encoded:", encoded)
    decoded = tokenizer.decode(encoded)
    print("Decoded:", decoded)