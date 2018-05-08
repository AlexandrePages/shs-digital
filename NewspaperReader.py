from tkinter import *
import EventStructure as es
import PhraseFinder as pf
import numpy as np
import matplotlib.pyplot as mpl
import WikiArticleFinder as waf
import os
import io

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
	 if sen[i] == '.' and sen[i-1].islower():
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
	
	text = open_fichier(fichier)
	# text is an array of newspaper lines
	text = clean_text_pre(text)
	# text is now an array of sentences
	[firstname,lastname]=format_name(name)
	[wo,fo,lo] = find_name(name, firstname,lastname,text)
	if wo==[] and fo==[] and lo==[]:
		sen=[]
	else:
		[x,y,p] = name_occ_fit(wo,fo,lo,text)
		lr=make_article_bounds(wo,p)
		sen=[]
		for i in lr:
			#print(i)
			ll=min(i[0],0)
			rr=min(len(text)-1,i[-1])
			sen+=text[ll:rr]
		sen = clean_text_post(sen)
	
	return sen

		
#sen = make_sentences('JDG19101101.txt','Henri Dunant')
#print(sen)
#'JDG19101101.txt'
#'Henri Dunant'

class base_gui():
	def __init__(self):
		
		self.app = Tk()
		self.frame = Frame(self.app)
		
		self.frame.grid()
		self.title = Label(self.frame, fg='RED', text="ENTRYMAKER BOT v0.1 alphatest")
		self.title.grid(row=0)
		
		self.file_label = Label(self.frame, text="Fichier")
		self.file_label.grid(row=3)
		
		self.name_label = Label(self.frame, text="Nom à checher")
		self.name_label.grid(row=1)
		
		self.arn_label = Label(self.frame, text="Nombre d'Articles")
		self.arn_label.grid(row=2)
		
		self.name_entry = Entry(self.frame)
		self.name_entry.grid(row=1,column=1)

		self.name_entry.delete(0, END)
		self.name_entry.insert(0, "Henri Dunant")
		
		self.arn_entry = Entry(self.frame)
		self.arn_entry.grid(row=2,column=1)

		self.arn_entry.delete(0, END)
		self.arn_entry.insert(0, 100)
		
		self.file_entry = Entry(self.frame)
		self.file_entry.grid(row=3,column=1)

		self.file_entry.delete(0, END)
		self.file_entry.insert(0, "Don't Use")
		
		
		self.button = Button(self.frame, text="RUN", fg="blue", command=self.run_search)
		self.button.grid(row=4,column=0)
        
		self.button = Button(self.frame, text="PLOT", fg="red", command=self.plot_fit_gui)
		self.button.grid(row=4,column=1)
        
		self.app.mainloop()
		
	def make_new_text_window(self,text):
		h=600
		w=500
		new_tl=Toplevel(self.app,height=h,width=w)
		new_tl.geometry("%dx%d%+d%+d" % (w, h, 100, 10))
		scrollbar=Scrollbar(new_tl,orient=VERTICAL)
		scrollbar.pack(fill=Y,side=LEFT)
		new_cv=Canvas(new_tl,width=w,height=h)
		new_cv.pack(fill=BOTH)
		
		line = Text(new_cv,height=h,yscrollcommand=scrollbar.set)
		line.pack(fill=BOTH,side=LEFT)
		for i in range(0,len(text)):
			line.insert('1.0',text[len(text)-1-i])
			#line.insert('1.0','\n')
			#line.insert('1.0','-----------')
			#line.insert('1.0','\n')
			
		scrollbar.config(command=line.yview)
	def run_search(self):
		name = self.name_entry.get()
		arn = self.arn_entry.get()
		#waf.make_doc(name, arn, 1)
		prof = es.fiche(name)
		for filename in enumerate(os.listdir(name + '/')):
			nom_fichier= name + '/' + filename[1]
			text = open_fichier(nom_fichier)
			sen = get_text_for_name(nom_fichier,name)
			evs = pf.find_evenement(sen,text)
			for e in range(len(evs)):
				ev = es.evenement(evs[e][0],evs[e][1],evs[e][2])
				prof.add_evenement(ev)
				#prof.get_evenement(e)
			
		t2p=prof.str_fiche()
		self.make_new_text_window(t2p)
			
		#self.make_new_text_window(sen)
	def plot_fit_gui(self):
		name = self.name_entry.get()
		fichier = self.file_entry.get()
		text = open_fichier(fichier)
		[firstname,lastname]=format_name(name)
		[wo,fo,lo] = find_name(name, firstname,lastname,text)
		[x,y,p] = name_occ_fit(wo,fo,lo,text)
		plot_fit(x,y,p)
u = base_gui()
