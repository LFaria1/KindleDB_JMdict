# Variable names are the same as the element they represent in JMdict_e.xml
# 
# NAMING DEFINITIONS
# 
# entry = Entries consist of kanji elements, reading elements, 
# general information and sense elements.
# ----
# pos = part-of-speech.
# ----
# keb = This element will contain a word or short phrase in Japanese 
# 	which is written using at least one non-kana character (usually kanji,
# 	but can be other characters)
# ----
# sense = The sense element will record the translational equivalent
# 	of the Japanese word, plus other related information.
# ----
# kele = k_ele(kanji element)
# ----
# rele = r_ele(reading element, contains valid readings)
# -----------------------------------------------------------


import csv
import xml.etree.cElementTree as ET
import time
import sqlite3

db = sqlite3.connect(':memory:')
db = sqlite3.connect('vocab.db')
cursor =db.cursor()

cursor.execute('''SELECT usage,word_key,book_key FROM LOOKUPS''')
allrows=cursor.fetchall()
cursor.execute('''SELECT id,title FROM BOOK_INFO''')
books=cursor.fetchall()
#fetch como string 

#busca part-of-speech e definições
def definitions(entry):
	deftext=''	
	sense =entry.find('sense')
	poss = sense.findall('pos')
	deftext = deftext + '('
	apos = list()
	for pos in poss:
		aux =pos.text[:-1]
		apos.append(aux)
	deftext = deftext + ', '.join(apos)
	deftext = deftext + ')'
		
	glosses=sense.findall('gloss')
	for gloss in glosses:
		deftext = deftext+ ' ' + gloss.text +';'
	return deftext
#busca leituras	
def readings(entry):
	readtext=''
	readings =entry.findall('r_ele')
	aread = list()
	for reading in readings:
		aux = readtext + reading.find('reb').text
		aread.append(aux)
	readtext = readtext + '; '.join(aread)
	return readtext
#busca nome do livro
def searchbooks(bookkey):
	bookName=''
	for book in books:
		if(bookkey == book[0]):
			bookName =book[1]
	return bookName

#formatando para o formato de import do Anki
fnames=['word','phrase','reading','meaning','book']
#ffile= open('teste.csv','r+',encoding='utf-8-sig')
#reader =csv.DictReader(ffile)
sfile=open('export.csv','w',newline='',encoding='utf-8-sig')
writer = csv.DictWriter(sfile, delimiter='|', fieldnames=fnames)
writer.writeheader()
starttime= time.time()
tree = ET.parse('JMdict_e.xml');
root = tree.getroot()
entrys = root.findall('entry')
i=0
#

#
for word in allrows:
	found=False
	auxword = word[1]
	wordcheck = auxword[3: ]
	bookkey = word[2]
	for entry in entrys:
		keles=entry.findall('k_ele')
		for kele in keles:
			if(wordcheck == kele.find('keb').text and not found):
				writer.writerow({'word':wordcheck,'phrase' : word[0], 'reading' : readings(entry),'meaning':definitions(entry),'book':searchbooks(bookkey)})
				i+=1
				print (i)
				found=True
				
print(time.time()-starttime)

db.close()
#ffile.close()
sfile.close()

