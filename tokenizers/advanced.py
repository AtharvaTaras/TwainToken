import os, sys, re, json
from typing import Optional

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)


def advanced_preprocess(text:str) -> str:
	# Performs more advanced text preprocessing
	pairs = [
	['--', ' '], 
	['__', ''], 
	['“', '"'], 
	['”', '"'],
	]

	for pair in pairs:
		text = re.sub(pair[0], pair[1], text)

	text = re.sub(r'([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~])', r' \1 ', text) # Add spaces around punctuation
	text = re.sub(r'(\d+)', r'\1 ', text)                                   # Add spaces after digits
	text = re.sub(r'\n', ' <newline> ', text)                                   # Replace newlines with a token
	# text = re.sub(r'([A-Z])', '<caps> \1', text)                              # Add a token before capital letters
	text = re.sub(r'\b([A-Z][a-z]*)\b', lambda m: ' <caps> ' + m.group(1).lower(), text) 

	return text.lower()


def advanced_postprocess(text: str) -> str:
    tokens = text.split()
    result = []
    i = 0

    # --- 1. Handle <caps> ---
    while i < len(tokens):
        if tokens[i] == "<caps>" and i + 1 < len(tokens):
            next_token = tokens[i + 1]

            if re.match(r'^[a-zA-Z]+$', next_token):
                result.append(next_token.capitalize())
            else:
                result.append(next_token)

            i += 2
        else:
            result.append(tokens[i])
            i += 1

    text = " ".join(result)

    # --- 2. REMOVE leftover <caps> EARLY ---
    text = re.sub(r'\b<caps>\b\s*', '', text)

    # --- 3. Restore newlines ---
    text = re.sub(r'\s*<newline>\s*', '\n', text)

    # --- 4. Fix contractions ---
    text = re.sub(r"([a-zA-Z])'\s([a-zA-Z])", r"\1'\2", text)

    # --- 5. Remove space BEFORE punctuation ---
    text = re.sub(r'\s+([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~])', r'\1', text)

    # --- 6. Ensure space AFTER punctuation ---
    text = re.sub(r'([,:;.!?])([^\s\n])', r'\1 \2', text)

    # --- 7. Fix brackets ---
    text = re.sub(r'\[\s+', '[', text)
    text = re.sub(r'\s+\]', ']', text)
    text = re.sub(r'([^\s])(\[)', r'\1 \2', text)
    text = re.sub(r'\](\w)', r'] \1', text)

    # --- 8. Fix # spacing ---
    text = re.sub(r'\s+#\s+', ' #', text)
    text = re.sub(r'([^\s])#', r'\1 #', text)

    # --- 9. Fix URLs ---
    text = re.sub(r'(\w)\.\s+(\w)', r'\1.\2', text)
    text = re.sub(r'\s*/\s*', '/', text)

    # --- 10. Normalize spaces (preserve newlines) ---
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r' *\n *', '\n', text)

    return text.strip()


class AdvancedTokenizer():
    def __init__(self, encodings:Optional[str] = None) -> None:
        if encodings is not None:
            if os.path.exists(encodings) and encodings.endswith('.json'):
                with open(encodings, 'r') as f:
                    self.encodings = json.load(f)
            
            else:
                raise ValueError('Encodings file must be a .json file and must exist.')

        else:
            encoding_file = os.path.join(ROOT_DIR, 'encodings', 'v3.json')
            if os.path.exists(encoding_file):
                with open(encoding_file, 'r') as f:
                    self.encodings = json.load(f)

            else:
                raise ValueError('Default encodings file not found. Please provide a valid encodings file.')
            

    def encode(self, text:str) -> list[int]:
        preprocessed = advanced_preprocess(text)
        tokens = preprocessed.split()
        return [self.encodings.get(token, self.encodings[' ']) for token in tokens]
    

    def decode(self, token_ids:list[int]) -> str:
        reverse_lookup = {value: key for key, value in self.encodings.items()}
        tokens = [reverse_lookup.get(token_id, ' ') for token_id in token_ids]

        # Capitalize logic
        tokens[0] = tokens[0].capitalize() if tokens else ''

        for i in range(1, len(tokens)):
            if tokens[i-1] in ['.', '!', '?']:
                tokens[i] = tokens[i].capitalize()

        text = ' '.join(tokens)
        return advanced_postprocess(text)


if __name__ == '__main__':
    tokenizer = AdvancedTokenizer()
    text = "Hello, world! This is a test."
    encoded = tokenizer.encode(text)
    print("Encoded:", encoded)
    decoded = tokenizer.decode(encoded)
    print("Decoded:", decoded)