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
	text = re.sub(r'(\d{1})', r'\1 ', text)                                   # Add spaces after digits
	text = re.sub(r'\n', '<newline>', text)                                   # Replace newlines with a token
	text = re.sub(r'[A-Z]', '<caps> \1', text)                                # Add a token before capital letters

	return text.lower()


def advanced_postprocess(text:str) -> str:
	text = re.sub(r'\s<newline>\s', '\n', text)                               # Replace newline tokens with actual newlines
	text = re.sub(r'\s<caps>\s([a-z])', r' \1', text)                         # Remove caps tokens and restore original capitalization
	text = re.sub(r'\s([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~])', r'\1', text) # Remove spaces around punctuation
	text = re.sub(r'\s(\d{1})', r'\1', text)                                  # Remove spaces after digits

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
	

if __name__ == '__main__':
	text = "Hello, world! It's a test. 100$"
	print("Original:", text)

	preprocessed = advanced_preprocess(text)
	print("Preprocessed:", preprocessed)

	postprocessed = advanced_postprocess(preprocessed)
	print("Postprocessed:", postprocessed)
