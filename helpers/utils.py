import re
from typing import Optional


# def advanced_postprocess(text:str) -> str:
# 	tokens = text.split()
# 	result = []
# 	i = 0

# 	while i < len(tokens):
# 		if tokens[i] == "<caps>" and i + 1 < len(tokens):
# 			next_token = tokens[i + 1]

# 			# Capitalize ONLY if it's alphabetic
# 			if next_token.isalpha():
# 				result.append(next_token.capitalize())
# 			else:
# 				result.append(next_token)

# 			i += 2  # skip <caps> + next token
# 		else:
# 			result.append(tokens[i])
# 			i += 1

# 	text = " ".join(result)
# 	text = re.sub(r'\s<caps>\s([a-z])', r' \1', text)                               # Remove caps tokens and restore original capitalization
# 	text = re.sub(r'\s*([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~])\s*', r'\1', text)   # Remove spaces around punctuation
# 	text = re.sub(r'\s(\d+)\s', r'\1', text)                                        # Remove spaces after digits
# 	text = re.sub(r"([a-zA-Z])'\s([a-zA-Z])", r"\1'\2", text)                       # Fix contractions (e.g., "it's" instead of "it 's")
# 	text = re.sub(r'([.!?])(\d)', r'\1 \2', text)                                   # Add space after punctuation

# 	text = re.sub(r'\s+([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~])', r'\1', text)
# 	text = re.sub(r'([,:;.!?])([^\s])', r'\1 \2', text)
# 	text = re.sub(r'\[\s+', '[', text)
# 	text = re.sub(r'\s+\]', ']', text)
# 	text = re.sub(r'([^\s])(\[)', r'\1 \2', text)

# 	text = re.sub(r'[ \t]+', ' ', text)
# 	text = re.sub(r' *\n *', '\n', text)
# 	text = re.sub(r' *\n *', '\n', text)

# 	text = re.sub(r'\s*<newline>\s*', r'\n', text)                                  # Replace newline tokens with actual newlines
# 	text = re.sub(r'\s+#\s+', ' #', text)
# 	text = re.sub(r'([^\s])#', r'\1 #', text)
# 	text = re.sub(r'\](\w)', r'] \1', text)
# 	# Remove spaces around dots in URLs/domains
# 	text = re.sub(r'(\w)\.\s+(\w)', r'\1.\2', text)

# 	# Remove spaces around slashes
# 	text = re.sub(r'\s*/\s*', '/', text)
# 	return text


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


def generate_tokenizer_lookup(vocab:Optional[dict]=None, text:Optional[str]=None) -> dict:
	# Returns tokens sorted by frequency, with the most common token at index 0
	if (text is None) and (vocab is None) :
		raise ValueError('Either vocab or text must be provided.')

	if text is not None:
		vocab = generate_vocabulary(text)
		# sorted_tokens = dict(sorted(vocab.items(), key=lambda x: x[1], reverse=True))
	
	return {token: idx for idx, token in enumerate(sorted(vocab, key=vocab.get, reverse=True))}
	

if __name__ == '__main__':
	text = """Release date: June 22, 2004 [eBook #3176]
                Most recently updated: September 13, 2025

Language: English

Other information and formats: www.gutenberg.org/ebooks/3176"""
	print("Original:", text)

	preprocessed = advanced_preprocess(text)
	print("Preprocessed:", preprocessed)

	postprocessed = advanced_postprocess(preprocessed)
	print("Postprocessed:", postprocessed)
