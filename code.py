
from classes import *
from random import randint
import datetime
from copy import deepcopy
from bs4 import BeautifulSoup
import requests
import info as info

#global variables
words = []
size = 30
wordnum = 20
sec = 20
loaded = 0

def main():
	global words,wordnum,sec,loaded
	loaded = 0
	words = []
	info.info_string = 'Connecting to server.....###%'
	print 'Loading words ...'
	'''
	#for debugging
	w = ['miniature','unsightly','male','pleasant','mature','plastic','funny','glamorous','maddening','voracious','precious','chubby','ratty','rambunctious','complex']
	for txt in w:
		wd = word(txt,'a','clue')
		words.append(wd)
	'''
	get_words(wordnum)
	a,b,c = find_best_crossword(sec)
	info.grid = a
	info.gridnum = b
	info.wordlist = c
	info.info_string = 'DONE'
	return

def get_words(no_of_words):
	global words

	num_adj = randint( no_of_words/10 , no_of_words/2 ) 
	words_left = no_of_words -  num_adj

	num_verb = randint( no_of_words/10 , words_left/2 )
	
	num_noun = no_of_words - num_adj - num_verb

	url_adj = "https://www.randomlists.com/random-adjectives?qty=" + str(num_adj)
	url_verb = "https://www.randomlists.com/random-verbs?qty=" + str(num_verb)
	url_noun = "https://www.randomlists.com/nouns?qty=" + str(num_noun)
	read_data(url_adj,'Adjective',num_adj,num_verb,num_noun)
	read_data(url_verb,'Verb',num_adj,num_verb,num_noun)
	read_data(url_noun,'Noun',num_adj,num_verb,num_noun)

	words = sort_words(words)

def read_data(url,typ,num_adj,num_verb,num_noun):
	global words,loaded
	try:
		request  = requests.get(url)
	except requests.exceptions.ConnectionError as e:
		info.info_string = 'Error : #'+ str(e.args[0].reason) + '##%'
		print '----ERROR---- : '
		print e.args[0].reason

	data = request.text
	soup = BeautifulSoup(data , "html.parser")

	tag_ol = soup.find_all(id='result')[0]

	for tag_li in tag_ol.children:
		t = tag_li.find_all(class_='crux')[0].text
		txt = ''
		for c in t:
			if c != '-':
				txt += c
		print txt + ' -  ' + typ + ' = ',
		clue = get_clue(txt,typ)
		loaded += 1
		info.info_string = 'Loading words ...#Random selection - Adjectives:' + str(num_adj) + ' Verbs:' + str(num_verb) + ' Nouns:' + str(num_noun)
		info.info_string += '#Loaded : (' + str(loaded) + '/' + str(wordnum) + ')#%'
		print clue + ';'
		wd = word(txt,typ,clue)
		words.append(wd)

def get_clue(wd,typ):
	#different types of clues:
	# 1. defination
	# 2. fill up

	rndm = randint(0,10000)
	f = True
	
	if rndm%5 == 0:
		
		url = 'http://sentence.yourdictionary.com/'+wd
		try:
			request  = requests.get(url)
		except requests.exceptions.ConnectionError as e:
			info.info_string = 'Error : #'+ str(e.args[0].reason) + '##%'
			return 'Error getting example from server'

		data = request.text
		soup = BeautifulSoup(data , "html.parser")
		
		error = soup.find_all('p',class_='error-msj')
		if len(error) > 0:
			f = True
		else:
			tag_ul = soup.find_all(id="examples-ul-content")[0]
			tag_li = tag_ul.find_all(class_='voting_li')[0]
			tag_div = tag_li.find_all(class_='li_content')[0]
			
			t =  tag_div.text
			ls = t.split()
			new = []
			txt = ''

			for l in ls:
				if l != wd:
					new.append(l)
				else:
					new.append('_'*len(l))
					f = False

			txt = ' '.join(new)
			if f == False:
				return txt + ' (' + typ + ')'	
	

	if f == True:
		url = 'http://wordnetweb.princeton.edu/perl/webwn?s='+wd+'+&sub=Search+WordNet&o2=&o0=&o8=1&o1=1&o7=&o5=&o9=&o6=&o3=&o4=&h=0000000000'
		
		try:
			request  = requests.get(url)
		except requests.exceptions.ConnectionError as e:
			info.info_string = 'Error : #'+ str(e.args[0].reason) + '##%'
			return 'Error getting definition from server'

		data = request.text
		soup = BeautifulSoup(data , "html.parser")

		try:
			tag = soup.find_all('h3',string=typ)
			d = tag[0].find_next_siblings('ul')[0].text
			return extract_def(d)
		except:
			info.info_string = 'Error : # no tag found ##%'
			return 'Error getting definition from server'

def extract_def(d):
	first = True
	skip = True
	bracket = 0

	dictionary = ''
	for char in d:

		if char == '(' and first == True:
			continue
		elif char == ')' and first == True:
			first = False
			continue

		if char == '(' and first == False and bracket == 0:
			skip = False
			bracket += 1
			continue

		if char == '(' and first == False:
			bracket += 1
			if bracket > 1:
				dictionary = dictionary + char
			continue
		elif char == ')' and first == False:
			if bracket > 1:
				dictionary = dictionary + char
			bracket -= 1
			continue

		if bracket == 0 and dictionary != '':
			break

		if char == ';':
			skip = True

		if skip == False:
			dictionary = dictionary + char


	return dictionary


def sort_words(words):
	for i in range(1,len(words)):
		j=i-1
		key = words[i]

		while j > -1 and words[j].length < key.length:
			words[j+1] = words[j]
			j -= 1

		words[j + 1] = key

	return words

def firstword(crossword):
	global words,size

	w = deepcopy(words[0])
	rndm = randint(1,2000)
	if rndm%2 == 0:
			w.dir = 'across'
	else:
		w.dir = 'down'
	w.row = size/2 - (w.length/2)
	w.col = size/2 - (w.length/2)
	
	crossword.set_word(w)
	
def find_possible_pos(word,crossword):
	cross = False
	intersections = []
	possible_pos = []

	#first find any intersections
	for char_no in range(0,word.length):
		char = word.text[char_no]

		for row_no in range(0,crossword.rows):
			for col_no in range(0,crossword.cols):
				if char == crossword.get_cell(row_no,col_no):
					intersections.append({'row':row_no,'col':col_no,'pos':char_no})


	#now check if any of those intersections is good 
	#and score them
	
	#first horizontly/across
	for i in intersections:
		startr = i['row']
		startc = i['col'] - i['pos']
		endr = startr
		endc = startc + word.length - 1

		score = 1

		#check boundaries
		if startr < 0 or startr >= crossword.rows:
			continue
		if startc < 0 or startc >= crossword.cols:
			continue
		if endr < 0 or endr >= crossword.rows:
			continue
		if endc < 0 or endc >= crossword.cols:
			continue

		#check edge characters
		try:
			if crossword.get_cell(startr,startc-1) != '-':
				continue
			if crossword.get_cell(startr,endc+1) != '-':
				continue
		except:
			pass

		#check surroundings
		f = False
		for char_no in range(0,word.length):
			if char_no != i['pos']:
				#check cell
				if crossword.get_cell(startr,startc+char_no) != '-':
					if crossword.get_cell(startr,startc+char_no) == word.text[char_no]:
						score += 1
						continue
					else:
						f = True
						break
				#check cells above and below
				try: 
					if crossword.get_cell(startr-1,startc+char_no) != '-':
						f = True
						break
					if crossword.get_cell(startr+1,startc+char_no) != '-':
						f = True
						break
				except:
					pass
		if f == True:
			continue

		#if code reaches here => position is good
		cross = True
		possible_pos.append({'row':startr,'col':startc,'dir':'across','score':score})

	#now for vertical/down
	for i in intersections:
		startr = i['row'] - i['pos']
		startc = i['col']
		endr = startr + word.length - 1
		endc = startc

		score = 1
		
		#check boundaries
		if startr < 0 or startr >= crossword.rows:
			continue
		if startc < 0 or startc >= crossword.cols:
			continue
		if endr < 0 or endr >= crossword.rows:
			continue
		if endc < 0 or endc >= crossword.cols:
			continue
		
		#check edge characters
		try:
			if crossword.get_cell(startr-1,startc) != '-':
				continue
			if crossword.get_cell(endr+1,startc) != '-':
				continue
		except:
			pass

		#check surroundings
		f = False
		for char_no in range(0,word.length):
			if char_no != i['pos']:
				#check cell
				if crossword.get_cell(startr + char_no,startc) != '-':
					if crossword.get_cell(startr + char_no,startc) == word.text[char_no]:
						score += 1
						continue
					else:
						f = True
						break
				#check cells above and below
				try: 
					if crossword.get_cell(startr+char_no,startc-1) != '-':
						f = True
						break
					if crossword.get_cell(startr+char_no,startc+1) != '-':
						f = True
						break
				except:
					pass
		if f == True:
			continue

		#if code reaches here => position is good
		cross = True
		possible_pos.append({'row':startr,'col':startc,'dir':'down','score':score})

	#if no possible positon is found then find any random empty place on the board
	#no need to run this if cross is possible
	if cross == False:
		good = False

		while good == False:

			startr = randint(0,crossword.rows)
			startc = randint(0,crossword.cols)

			rndm = randint(1,2000)
			if rndm%2 == 0:
				random_dir = 'across'
			else: 
				random_dir = 'down'


			if random_dir == 'across':
				endr = startr
				endc = startc + word.length

				score = 0

				#check boundaries
				if startr < 0 or startr >= crossword.rows:
					continue
				if startc < 0 or startc >= crossword.cols:
					continue
				if endr < 0 or endr >= crossword.rows:
					continue
				if endc < 0 or endc >= crossword.cols:
					continue

				#check edge characters
				try:
					if crossword.get_cell(startr,startc-1) != '-':
						continue
					if crossword.get_cell(startr,endc+1) != '-':
						continue
				except:
					pass

				#check surroundings
				f = False
				for char_no in range(0,word.length):
					#check cell
					if crossword.get_cell(startr,startc+char_no) != '-':
						if crossword.get_cell(startr,startc+char_no) == word.text[char_no]:
							score += 1
							continue
						else:
							f = True
							break
					#check cells above and below
					try: 
						if crossword.get_cell(startr-1,startc+char_no) != '-':
							f = True
							break
						if crossword.get_cell(startr+1,startc+char_no) != '-':
							f = True
							break
					except:
						pass
				if f == True:
					continue

				#if code reaches here => position is good
				good = True
				possible_pos.append({'row':startr,'col':startc,'dir':'across','score':score})

			elif random_dir == 'down':
				endr = startr + word.length
				endc = startc 

				score = 0
				
				#check boundaries
				if startr < 0 or startr >= crossword.rows:
					continue
				if startc < 0 or startc >= crossword.cols:
					continue
				if endr < 0 or endr >= crossword.rows:
					continue
				if endc < 0 or endc >= crossword.cols:
					continue
				
				#check edge characters
				try:
					if crossword.get_cell(startr-1,startc) != '-':
						continue
					if crossword.get_cell(endr+1,startc) != '-':
						continue
				except:
					pass

				#check surroundings
				f = False
				for char_no in range(0,word.length):
					#check cell
					if crossword.get_cell(startr + char_no,startc) != '-':
						if crossword.get_cell(startr + char_no,startc) == word.text[char_no]:
							score += 1
							continue
						else:
							f = True
							break
					#check cells above and below
					try: 
						if crossword.get_cell(startr+char_no,startc-1) != '-':
							f = True
							break
						if crossword.get_cell(startr+char_no,startc+1) != '-':
							f = True
							break
					except:
						pass
				if f == True:
					continue

				#if code reaches here => position is good
				good = True
				possible_pos.append({'row':startr,'col':startc,'dir':'down','score':score})

		#reduce score if crossword is broken
		crossword.broken = True
	return possible_pos		


def add_best_pos(wd,possible_pos,crossword):
	good = []
	max_score = 0

	for l in possible_pos:
		if l['score'] > max_score:
			max_score = l['score']

	for l in possible_pos:
		if l['score'] == max_score:
			good.append(l)

	try:
		rndm = randint(0,len(good)-1)
		
		w = word(wd.text,wd.type,wd.clue)
		w.row = good[rndm]['row']
		w.col = good[rndm]['col']
		w.dir = good[rndm]['dir']

		crossword.set_word(w)
	except Exception as e:
		pass

def generate_crossword():
	global words,size
	crossword = grid(size,size)
	crossword.clear_grid()
	firstword(crossword)
	for i in range(1,len(words)):
		pos = find_possible_pos(deepcopy(words[i]),crossword)
		add_best_pos(deepcopy(words[i]),pos,crossword)
	crossword.calc_score()
	return crossword

def find_best_crossword(time):
	global words
	best_score = 0
	count = 0
	sec = 0
	#print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

	start_time = datetime.datetime.now()
	end_time = datetime.datetime.now()

	while (end_time - start_time).total_seconds() < time:
		end_time = datetime.datetime.now()
		temp = generate_crossword()
		count += 1
		sec = int(time - (end_time - start_time).total_seconds())
		if sec < 0:
			sec = 0
		info.info_string = 'Generating Crosswords.....#Total crosswords generated till now : ' + str(count) + '#Time remaining : ' + str(sec) + ' Seconds#%'
		print 'time remaining : ' + str(sec) + 'sec,  best score till now : ' + str(best_score)  + ', crosswords generated till now :' + str(count)
		if temp.score > best_score:
			best_score = temp.score
			best_crossword = deepcopy(temp)

	best_crossword.display()
	return best_crossword.grid , best_crossword.grid_num , best_crossword.wordlist














