class evenement:
	def __init__(self,d,l,a,s):
		self.date=d
		self.lieu=l
		self.action=a
		self.score=s
class fiche:
	def __init__(self, n):
		self.name=n
		self.evts=[]
	def add_evenement(self, e):
		self.evts.append(e)
	def get_evenement(self,i):
		if i < len(self.evts):
			print(self.evts[i])
	def sort_evenements_by_score(self):
		self.evts.sort(key=lambda x: x.score, reverse=False)
	def remove_score_0(self):
		self.evts = list(filter(lambda x : x.score != 0, self.evts))
	def remove_dup(self):
		d = []
		for i in range(len(self.evts)-1):
			for j in range(i+1,len(self.evts)):
				if self.evts[i].action==self.evts[j].action:
					d.append(i)
					
		for i in reversed(d):
			self.evts.pop(i)
	def str_fiche(self):
		s = [self.name]
		s.append('\n')
		rang=0
		if len(self.evts)>0:
			for i in self.evts:
				s.append(i.date)
				s.append(' / ')
				s.append(i.lieu)
				s.append('. ')
				s.append(i.action)
				s.append('\n')
				s.append('RANG:')
				s.append('\n')
				s.append(str(rang))
				s.append('\n')
				s.append('SCORE:')
				s.append('\n')
				s.append(str(i.score))
				s.append(' \n')
				s.append(' \n')
				rang+=1
		return s
