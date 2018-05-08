class evenement:
	def __init__(self,d,l,a):
		self.date=d
		self.lieu=l
		self.action=a
class fiche:
	def __init__(self, n):
		self.name=n
		self.evts=[]
	def add_evenement(self, e):
		self.evts.append(e)
	def get_evenement(self,i):
		if i < len(self.evts):
			print(self.evts[i])
	def str_fiche(self):
		s = [self.name]
		s.append('\n')
		rang=0
		if len(self.evts)>0:
			for i in self.evts:
				s.append('\n')
				s.append('DATE:')
				s.append('\n')
				s.append(i.date)
				s.append('\n')
				s.append('LIEU:')
				s.append('\n')
				s.append(i.lieu)
				s.append('\n')
				s.append('ACTION:')
				s.append('\n')
				s.append(i.action)
				s.append('\n')
				s.append('RANG:')
				s.append('\n')
				s.append(str(rang))
				rang+=1
		return s
