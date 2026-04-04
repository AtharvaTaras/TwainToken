import re

def simple_preprocess(text:str) -> str:
    # Performs basic text preprocessing
    
    pairs = [
    ['--', ' '], 
    ['__', ''], 
    ['“', '"'], 
    ['”', '"'],
    ]

    for pair in pairs:
        text = re.sub(pair[0], pair[1], text)

    text = re.sub(r'([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~])', r' \1 ', text) # Add spaces around punctuation
    text = re.sub(r'(\d{1})', r'\1 ', text)                                   # Add spaces after digits
    text = re.sub(r'\s+', ' ', text)                                          # Replace multiple spaces with a single space

    return text.lower()


def simple_postprocess(text:str) -> str:
    text = re.sub(r'\s([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~])', r'\1', text)
    text = re.sub(r'\s(\d{1})', r'\1', text)
    return text

def generate_vocabulary(text:str) -> dict:
    # Generates a dictionary of unique tokens and their frequencies in the text.

    tokens = text.split()
    unique = {}
    unique[' '] = len(tokens)

    for token in tokens:
        if token in unique:
            unique[token] += 1

        else:
            unique[token] = 1

    return unique


def generate_tokenizer_lookup(vocab:None|dict, text:None|str) -> dict:
    # Returns tokens sorted by frequency, with the most common token at index 0

    if text is not None:
        vocab = generate_vocabulary(text)
        return dict(sorted(vocab.items(), key=lambda x: x[1], reverse=True))
    
    elif vocab is not None:
        return dict(sorted(vocab.items(), key=lambda x: x[1], reverse=True))
    
    else:
        raise ValueError('Either vocab or text must be provided.')
    