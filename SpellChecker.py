import pandas as pd
import re
def load_dico_sc():
	dico = pd.read_csv('lexique382.csv',dtype=None,low_memory=False)
	words = dico.set_index('1_ortho', drop = False)
	return words

def get_words_as_vec(words):
	b = words.iloc[:,0]
	b = b.values
	return b

def is_line_gibb(text,words):
	for i in range(0,len(words)):
		ch = re.compile(r'\b({0})\b'.format(words[i]))
		
		if ch.search(text):
			return False
	return True

def check_text(text):
	new_text=[]
	if isinstance(text,list):
		words = get_words_as_vec(load_dico_sc())
		for i in range(0,len(text)):
			if is_line_gibb(text[i],words):
				new_text.append('')
			else:
				new_text.append(text[i])
	return new_text
