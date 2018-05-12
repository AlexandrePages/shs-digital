# coding: utf8 
import wikipedia as wk
import io
import os

def get_article_content(a):
	wk.set_lang('fr')
	p=wk.page(a)
	return p.content
	
def print_article(a):
	wk.set_lang('fr')
	p=wk.page(a)
	print(p.content)

def write_article(a,path):
	try:
		b="".join(i for i in a if i.isalnum())
		filename=path + '/' + b + '.txt'
		if not os.path.isfile(filename):
			p = get_article_content(a)
			f=io.open(filename,'w',encoding='utf8')
			f.write(p)
			f.close()
	except wk.exceptions.DisambiguationError:
		print('Dis Err')

def get_related_articles(a,n,namebool):
	wk.set_lang('fr')
	l=wk.search(a,n)
	rl=[]
	a = a.split(' ')
	if len(a)>1 and bool(namebool):
		for i in l:
			if a[0] not in i and a[1] not in i:
				rl.append(i)
	else:
		for i in l:
			rl.append(i)
	return rl

def print_related_articles(a,n):
	print(get_related_articles(a,n))

def make_doc(a,n, namebool):
	if not os.path.exists(a):
		os.makedirs(a)
	rl=get_related_articles(a,n, namebool)
	for i in rl:
		write_article(i,a)
