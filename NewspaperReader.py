from tkinter import *
from tkinter.ttk import *
import EventStructure as es
import PhraseFinder as pf
import numpy as np
import matplotlib.pyplot as mpl
import WikiArticleFinder as waf
import os
import io
import TextParser as tp

class base_gui():
	def __init__(self):
		self.app = Tk()
		Style().theme_use('classic')
		self.frame = Frame(self.app)
		
		self.app.title('EntryMaker Bot')
		self.frame.grid()
		self.title = Label(self.frame, text="EntryMaker Bot Beta")
		self.title.grid(row=0,columnspan=2)
		self.title.config(font=('Times',15,'bold'))
		
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
		self.file_entry.insert(0, "Fichier...")
		
		
		self.button1 = Button(self.frame, text="RUN", command=self.run)
		self.button1.grid(row=4,column=0)
		
		self.button1.config(width=30)
		
		self.button2 = Button(self.frame, text="PLOT", command=self.plot_fit_gui)
		self.button2.grid(row=4,column=1)
		
		self.button2.config(width=30)
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
		waf.make_doc(name, arn, 1)
		prof = es.fiche(name)
		for filename in enumerate(os.listdir(name + '/')):
			nom_fichier= name + '/' + filename[1]
			text = tp.open_fichier(nom_fichier)
			sen = tp.get_text_for_name(nom_fichier,name)
			evs = pf.find_evenement(sen,text,name)
			for e in range(len(evs)):
				ev = es.evenement(evs[e][0],evs[e][1],evs[e][2],evs[e][3])
				prof.add_evenement(ev)
				#prof.get_evenement(e)
		prof.sort_evenements_by_score()
		prof.remove_score_0()
		prof.remove_dup()
		t2p=prof.str_fiche()
		self.make_new_text_window(t2p)
			
		#self.make_new_text_window(sen)
	def plot_fit_gui(self):
		name = self.name_entry.get()
		fichier = self.file_entry.get()
		text = tp.open_fichier(fichier)
		[firstname,lastname]=tp.format_name(name)
		[wo,fo,lo] = tp.find_name(name, firstname,lastname,text)
		[x,y,p,fit] = tp.name_occ_fit_gauss(wo,fo,lo,text)
		tp.plot_fit(x,y,fit)
	def run(self):	
		self.app.update()
		self.run_search()
u = base_gui()
