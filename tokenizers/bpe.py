import os, sys, re, json
from typing import Optional

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)


def get_stats(tokens:list) -> dict:
    """
    returns {
    (token1, token2): count,
     ...
     }
    """

    token_pairs = {}
    for i in range(len(tokens) - 1):
        pair = (tokens[i], tokens[i + 1])
        token_pairs[pair] = token_pairs.get(pair, 0) + 1
    
    return token_pairs


class BPETokenizer():
    def __init__(self, encodings:Optional[str]=None) -> None:
        if encodings is not None:
            if os.path.exists(encodings) and encodings.endswith('.json'):
                with open(encodings, 'r', encoding='utf-8') as f:
                    self.encodings = json.load(f)
            
            else:
                raise ValueError('Encodings file must be a .json file and must exist.')

        else:
            encoding_file = os.path.join(ROOT_DIR, 'encodings', 'simple_bpe_words_v2.json')
            if os.path.exists(encoding_file):
                with open(encoding_file, 'r', encoding='utf-8') as f:
                    self.encodings = json.load(f)

        # print(list(self.encodings.items())[:10])
        self.reverse_table = {int(token_id) : tuple(pair) for token_id, pair in self.encodings.items()}
        # self.reverse_table = {v: k for k, v in self.encodings.items()}
        self.encodings = {tuple(pair): int(token_id) for token_id, pair in self.encodings.items()}


    def train(self, corpus_path:str, num_merges:int=100, save_file:bool=False) -> None:
        """
        Train the BPE tokenizer on a custom corpus.
        """

        if os.path.exists(corpus_path):
            with open(corpus_path, 'r', encoding='utf-8') as f:
                corpus = f.read()

        else:
            raise FileNotFoundError('Text corpus file must exist.')
    
        self.encodings = {}
        self.reverse_table = {}

        tokens = list(corpus.encode('utf-8'))
        token_counts = get_stats(tokens)
        merge_count = 0
        merge_table = {}

        while merge_count < num_merges:
            if not token_counts:
                break

            new_id = 256 + merge_count
            best_pair = max(token_counts, key=token_counts.get)
            tokens = self.merge_tokens(tokens, best_pair, new_id)
            merge_table[best_pair] = new_id
            token_counts = get_stats(tokens)
            merge_count += 1
            print(f'Merge {merge_count}/{num_merges}', end='\r')

        self.encodings = merge_table
        self.reverse_table = {v: k for k, v in merge_table.items()}

        if save_file:
            strdict = {}
            os.makedirs('.temp', exist_ok=True)
        
            for (t1, t2), new_id in merge_table.items():
                strdict[new_id] = [chr(t1), chr(t2)]

            with open(r'.temp\saved_encodings.json', 'w', encoding='utf-8') as f:
                json.dump(strdict, f, indent=4, ensure_ascii=False)

        return tokens, merge_table


    def continue_train(self, savefile_path:str=None, num_merges:int=100, save_file:bool=False):
        print('continue train')
        with open(r'.temp\saved_encodings.json', 'r', encoding='utf-8') as f:
            merge_table = json.load(f)
                
        # print(merge_table)
        merge_count = [k for k, v in merge_table.items()][-1]
        print(merge_count)

        while merge_count < num_merges + merge_count:
            new_id = merge_count + 1


            merge_count += 1

    def merge_tokens(self, tokens:list, pair:tuple, new_id:int) -> list:
        new_tokens = []
        i = 0

        while i < len(tokens) - 1:
            if (tokens[i], tokens[i + 1]) == pair:
                new_tokens.append(new_id)
                i += 2
            
            else:
                new_tokens.append(tokens[i])
                i += 1

        if i == len(tokens) - 1:
            new_tokens.append(tokens[-1])

        return new_tokens


    def encode_text(self, text:str) -> list:
        tokens = list(text.encode('utf-8'))

        for pair, new_id in self.encodings.items():
            tokens = self.merge_tokens(tokens, pair, new_id)

        return tokens


    def expand_token(self,token:int) -> list:
        """
        Revert compressed token pairs back to their original byte sequences
        """
        if token < 256:
            return [token]

        left, right = self.reverse_table[token]
        
        return self.expand_token(left) + self.expand_token(right)


    def decode_tokens(self, tokens:list,) -> str:
        decoded_tokens = []

        for token in tokens:
            if token < 256:
                decoded_tokens.append(token)

            elif token in self.reverse_table:
                decoded_tokens.extend(self.expand_token(token))

            else:
                decoded_tokens.append(ord('?'))

        return bytes(decoded_tokens).decode('utf-8', errors='replace')


if __name__ == "__main__":
    tokenizer = BPETokenizer(encodings=r'.temp\saved_encodings.json')
    text = "Hello, world! This is a test."
    encoded = tokenizer.encode_text(text)
    print("Encoded:", encoded)
    decoded = tokenizer.decode_tokens(encoded)
    print("Decoded:", decoded)

    # tokenizer.train(r'data\data_p1.txt', num_merges=100, save_file=True)
    tokenizer.continue_train(savefile_path=r'.temp\saved_encodings.json', num_merges=1, save_file=False)

    # encoded = tokenizer.encode_text("Hello, world! This is a test.")
    # print("Encoded:", encoded)
    # decoded = tokenizer.decode_tokens(encoded)
    # print("Decoded:", decoded)
    