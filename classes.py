
class word:

	def __init__(self,text,typ,clue):
		self.text = text
		self.type = typ
		self.length = len(text)
		self.clue = clue
		self.startnum = 0

		#position
		self.row = -1
		self.col = -1
		self.dir = 'none'

		

class grid:

	def __init__(self,rows,cols):
		self.grid =  [['-' for x in range(cols)] for x in range(rows)]
		self.grid_num =  [['-' for x in range(cols)] for x in range(rows)]
		self.rows = rows
		self.cols = cols
		self.score = 0
		self.wordlist = []
		self.broken = False

		self.maxr = 0
		self.minr = rows
		self.maxc = 0
		self.minc = cols

		self.height = 0
		self.width = 0

	def clear_grid(self):
		self.grid =  [['-' for x in range(self.cols)] for x in range(self.rows)]

	def set_cell(self,char,row,col):
		self.grid[row][col] = char

	def get_cell(self,row,col):
		return self.grid[row][col]

	def set_word(self,word):
		self.wordlist.append(word)
		if word.dir == 'across':
			pos = word.col
			for char in word.text:
				self.set_cell(char,word.row,pos)
				if word.row < self.minr:
					self.minr = word.row
				if word.row > self.maxr:
					self.maxr = word.row
				if pos < self.minc:
					self.minc = pos
				if pos > self.maxc:
					self.maxc = pos
				pos += 1
		
		elif word.dir == 'down':
			pos = word.row
			for char in word.text:
				self.set_cell(char,pos,word.col)
				if pos < self.minr:
					self.minr = pos
				if pos > self.maxr:
					self.maxr = pos
				if word.col < self.minc:
					self.minc = word.col
				if word.col > self.maxc:
					self.maxc = word.col
				pos += 1

	def display(self):
		for i in range(0,self.rows):
			for j in range(0,self.cols):
				print self.grid_num[i][j],
			print ''

		for w in self.wordlist:
			print str(w.startnum)  + ' , ' + w.dir + ' , ' + w.clue

		for i in range(0,self.rows):
			for j in range(0,self.cols):
				print self.grid[i][j],
			print ''

		print 'crossword score : ' + str(self.score) 
		if self.broken == True:
			print 'reduced'
		

	def calc_score(self):
		self.score = 0
		count = 1
		for w in self.wordlist:

			if self.grid_num[w.row][w.col] == '-':
				self.grid_num[w.row][w.col] = count
				w.startnum = count
				count += 1
			else:
				w.startnum = self.grid_num[w.row][w.col]


			if w.dir == 'across':
				a = 0
				for char_no in range(0,w.length):
					try:
						if self.get_cell(w.row - 1,w.col + char_no) != '-' and self.get_cell(w.row + 1,w.col + char_no) != '-':
							a += 1
							self.score += a
					except:
						pass

			elif w.dir == 'down':
				a = 0
				for char_no in range(0,w.length):
					try:
						if self.get_cell(w.row + char_no, w.col -1) != '-' and self.get_cell(w.row + char_no,w.col + 1) != '-':
							a += 1
							self.score += a
					except:
						pass

		self.height = float(self.maxr - self.minr + 1)
		self.width = float(self.maxc - self.minc + 1)
		ratio = self.height / self.width

		ratio_factor = abs(ratio - 1)
		self.score -= ratio_factor
		if self.broken == True:
			self.score = self.score / 2
			
