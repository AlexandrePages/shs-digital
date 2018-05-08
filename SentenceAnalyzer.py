import pandas as pd

def load_dico():
	dico = pd.read_csv('lexique382.csv',dtype=None,low_memory=False)
	words = dico.set_index('1_ortho', drop = False)
	return words

class definition:
	def __init__(self,o,l,c,g,n,i,f):
		self.ortho=o
		self.lemme=l
		self.cgram=c
		self.genre=g
		self.nombre=n
		self.infover=i
		self.freqliv=f
class mot:
	def __init__(self,m):
		self.m = m
		self.d = []
	def add_definition(self,o,l,c,g,n,i,f):
		self.d.append(definition(o,l,c,g,n,i,f))
	def printmot(self):
		print('mot -- lemme -- cgram -- genre -- nombre -- infover -- freqliv')
		for i in self.d:
			print([i.ortho,i.lemme, i.cgram, i.genre, i.nombre, i.infover, i.freqliv])

def sen_format(a,words):
	a=a.replace('.','')
	a=a.split(' ')
	b=[];
	for i in range(0,len(a)):
		s = mot(a[i])
		b.append(s)
		s=None
		if a[i] in words.index:
			j = words.loc[a[i],:]
			if len(j.shape) > 1:
				it = j.shape[0]
			else:
				it=1
			for k in range(0,it):
				if len(j.shape) > 1:
					v=j.iloc[k,:]
				else:
					v=j.iloc[:]	
				o=v[0]
				l=v[2]
				c=v[3]
				g=v[4]
				n=v[5]
				ii=v[10]
				f=v[9]
				b[i].add_definition(o,l,c,g,n,ii,f)
				v=None
		else:
			b[i].add_definition('None','None','None','None','None','None','None')
	return b

'''
b = sen_format('a salut je kiffe la nucléaire',load_dico())
for i in b:
	i.printmot()
'''
