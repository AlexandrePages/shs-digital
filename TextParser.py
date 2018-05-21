import io
import numpy as np
import matplotlib.pyplot as mpl
def open_fichier(nom_fichier):
	fichier=io.open(nom_fichier,'r',encoding='utf8')
	text=fichier.read()
	text = text.split('\n')
	fichier.close()
	return text;

def close_words(text):
	#print(len(text))
	for i in range(0,len(text)-1):
		#print(text[i][len(text[i])-1])
		#print(text[i])
		if len(text[i]) > 0 and text[i][len(text[i])-1]=='-':
			if ' ' in text[i+1]:
				a = text[i+1].split(' ')
				text[i] = text[i][:len(text[i])-1]+a[0]
				text[i+1] = text[i+1][len(a[0])+1:len(text[i+1])-1]
			else:
				a = text[i+1]
				text[i] = text[i][:len(text[i])-1]+a
				text[i+1]=''
		#print(text[i])		
	return text

def find_name(n,f,l, text):
	wo = []
	fo = []
	lo = []
	for i in range(0,len(text)):
		if n in text[i]:
			wo.append(i)
		elif f in text[i]:
			fo.append(i)
		elif l in text[i]:
			lo.append(i)
	return [wo,fo,lo]

def define_sentence(i,j,text):
	sen = ''
	for i in range(i,j):
		sen += text[i]
	new_sen = []
	z=0
	for i in range(1,len(sen)):
	 if sen[i] == '.' and not sen[i-1].isupper():
		 new_sen.append(sen[z+1:i])
		 z=i
	return new_sen

def clean_text_pre(text):
	text = close_words(text)
	for i in range(len(text)):
		text[i]+=' '
	text=define_sentence(0,len(text)-1,text)
	return text
def clean_text_post(text):
	#text = sc.check_text(text)
	text = list(filter(lambda x : x != '', text))		
	return text

def check_name(name):
	name = name.split(' ')
	if len(name) > 1:
		return True
	return False

def split_name(name):
	return name.split(' ');

def get_closest_lr(r,m,lts):
	if r == [] or m == []:
		return [0,0]
	else:
		rl = list(filter(lambda x: x<m,r))
		rr = list(filter(lambda x: x>m,r))
		rl=np.array(rl)
		rr=np.array(rr)
		if rl.size == 0:
			fl=m-lts
		else:
			l=np.abs(rl-m).argmin()
			fl=int(abs(rl[l]))
		if rr.size == 0:
			fr=m+lts
		else:
			r=np.abs(rr-m).argmin()
			fr=int(abs(rr[r]))
		return [fl,fr]
	
def plot_fit(x,y,p):
	xx=np.linspace(0,x[-1],300)
	plot = mpl.plot(x,y,'.',xx,p(xx),'-')
	mpl.show()
	
def name_occ_fit(wo,fo,lo,text):
	#print([wo, fo, lo])
	
	a=[0]*len(text)
	x=range(len(text))
	we=[0]*len(text)
	for i in x:
		if i in wo:
			a[i]+=1
		if i in fo:
			a[i]+=.5
		if i in lo:
			a[i]+=.8
		we[i] = a[i] + len(text[i])/1000
	b=[.3]*len(lo)
	c=[1]*len(wo)
	y = np.array(a+b+c)
	z = np.polyfit(x,a,10,w=we)
	p=np.poly1d(z)
	
	return [x,a,p]

def name_occ_fit_gauss(wo,fo,lo,text):
	a=np.array([0]*len(text))
	xx=range(len(text))
	we=[0]*len(text)
	for i in xx:
		if i in wo:
			a[i]+=1
		if i in fo:
			a[i]+=.5
		if i in lo:
			a[i]+=.8
	w=a*100+[0.1]*len(text)
	X = np.arange(a.size)
	x = np.sum(X*a)/np.sum(a)
	width = np.sqrt(np.abs((np.sum((X-x)**2*a)+len(wo)/10)/np.sum(a)))
	print(X-x)
	print(np.sum(a))
	print(width)
	max = a.max()
	fit = lambda t : max*np.exp(-(t-x)**2/(2*width**2))
	return [xx,a,width,fit]

def make_article_bounds_gauss(wo,g):
	var = g
	nlr=[]
	for i in enumerate(wo):
		nlr.append([int(round(i[1]-var)),int(round(i[1]+var))])
	print(nlr)	
	return nlr

def make_article_bounds(wo,p):
	r=np.round(np.roots(p))
	lr=[]
	for i in wo:
		lr.append(get_closest_lr(r,i,10))
	nlr=[]
	for i in lr:
		if i not in nlr:
			nlr.append(i)
	return nlr

def format_name(name):
	if check_name(name):
		[firstname,lastname] = split_name(name)
	else:
		[firstname,lastname] = ['_None_','_None_']
	return [firstname,lastname]

def get_text_for_name(fichier, name):
	print(fichier)
	text = open_fichier(fichier)
	# text is an array of newspaper lines
	text = clean_text_pre(text)
	# text is now an array of sentences
	[firstname,lastname]=format_name(name)
	[wo,fo,lo] = find_name(name, firstname,lastname,text)
	print([wo,fo,lo])
	if wo==[] and fo==[] and lo==[]:
		sen=[]
	else:
		[x,y,p,fit] = name_occ_fit_gauss(wo,fo,lo,text)
		lr=make_article_bounds_gauss(wo,p)
		sen=[]
		for i in lr:
			#print(i)
			ll=max(i[0],0)
			rr=min(len(text)-1,i[-1])
			sen+=text[ll:rr]
		sen = clean_text_post(sen)
	
	return sen

	
