from hashlib import sha1
from random import random
import csv

class document:
	header = '<?xml version="1.0" encoding="UTF-8" ?> \n\n<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n        xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n        xmlns:rss="http://purl.org/rss/1.0/"\n        xmlns:foaf="http://xmlns.com/foaf/0.1/"\n        xmlns:dc="http://purl.org/dc/elements/1.1/"\n        xmlns:wot="http://xmlns.com/wot/0.1/"\n>\n\n\n\n<foaf:PersonalProfileDocument rdf:about="http://www.w3.org/">\n  <foaf:maker rdf:resource="#CVs_Alunos_2015" />\n  <foaf:primaryTopic rdf:resource="#CVs_Alunos_2015" />\n</foaf:PersonalProfileDocument>\n'
	footer = '\n\n<!-- Documents -->\n\n\n <!-- digital signature for this file -->\n <rdf:Description rdf:about="Assinatura">\n   <wot:assurance rdf:resource="webwho.xrdf.asc" />\n </rdf:Description>\n\n\n</rdf:RDF>'

	def __init__(self,listaGiven, listaFamily, listaEmail):
		listaKnow = []
		for i in range(len(listaGiven)):
			localGiven = listaGiven[:]
			localFamily = listaFamily[:]

			localGiven.pop(i)
			localFamily.pop(i)

			lista = []
			numKnows = int(len(localGiven)*random()) 
			for j in range(numKnows):
				k = int(len(localGiven)*random())
				given = localGiven.pop(k)
				family = localFamily.pop(k)

				lista.append((str.split(given, " ")[:1][0],given+" "+family))
			
			listaKnow.append(lista)
		
		self.listaPerson = []
		self.group = group(listaGiven)
		for i in range(len(listaGiven)):
			self.listaPerson.append(person(str.split(listaGiven[i], " ")[:1][0],listaGiven[i]+" "+listaFamily[i],listaFamily[i],listaGiven[i],listaEmail[i],listaKnow[i]))

	def getText(self):
		text = self.header
		text += self.group.getText()
		for person in self.listaPerson:
			text += person.getText()
		text += self.footer
		return text



class knows:
	text = '<foaf:knows>\n		  <foaf:Person rdf:ID="%s">\n			  <foaf:title>Aluno(a)</foaf:title>\n			  <foaf:name>%s</foaf:name>\n			</foaf:Person>\n		</foaf:knows>\n\n'
	def __init__(self, ID, name):
		self.text = self.text % (ID,name)
	def getText(self):
		return self.text

class group:
	header = '<!-- GROUP -->\n\n  <foaf:Group rdf:ID="Prof_Alunos_IME">\n    <foaf:name>Professores da Pos-Graduacao em Sistemas e Computacao do IME </foaf:name>\n    \n    <!-- Members -->\n'
	member = '        <foaf:member rdf:resource="#%s"/>\n'
	footer = '\n	\n</foaf:Group>\n\n\n'
	def __init__(self, listaGiven):
		self.text = self.header
		for given in listaGiven:
			self.text += self.member % (str.split(given, " ")[:1][0])
		self.text += self.footer

	def getText(self):
		return self.text


class person:
	header = '<foaf:Person rdf:ID="%s">\n'
	profile = '<foaf:name>%s</foaf:name>\n		  <foaf:title>Aluno(a)</foaf:title>\n		  <foaf:familyName>%s</foaf:familyName>\n		  <foaf:givenName>%s</foaf:givenName>\n		  <foaf:mbox_sha1sum>%s</foaf:mbox_sha1sum>\n		  <foaf:workplaceHomePage rdf:resource="http://www.ime.eb.br/" />\n\n'
	footer = '</foaf:Person>\n\n\n'
	def __init__(self, ID,name,familyName,givenName,mbox,knownPeople):
		m = sha1()
		m.update(mbox)
		self.profile = self.profile % (name, familyName, givenName, m.hexdigest())
		self.header = self.header % (ID)
		self.knowsList = []
		for (personID, personName) in knownPeople:
			self.knowsList.append(knows(personID, personName))

	def getText(self):
		text = self.header + self.profile
		for elem in self.knowsList:
			text += elem.getText()
		text += self.footer
		return text

f = open("info.csv", 'rb')
read = csv.reader(f,delimiter=",")
listaGiven = []
listaFamily = []
listaEmail = []
for row in read:
	listaGiven.append(row[0])
	listaFamily.append(row[1])
	listaEmail.append(row[2])
f.close()
doc = document(listaGiven,listaFamily,listaEmail)
doc = doc.getText()
f = open("seilah.rdf","w")
f.write(doc)
f.close()


