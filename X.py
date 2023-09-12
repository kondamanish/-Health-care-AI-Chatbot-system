
from flask import Flask, render_template, request, session, session
#from flask_session import session
import sqlite3
import aiml
from seminar2_progress import sntnce as s
import random
import re
from mappings import map_keys
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

botName = "AIML-Bot"

@app.route("/")
def home():
	global botName
	session['sid'] = random.randint(1,10000) #uuid.uuid4()
	k.learn("std-startup.xml")
	k.respond("load aiml b", session.get('sid'))
	botName = k.getBotPredicate("name")
	k.setPredicate('email', '', session.get('sid'))

	return render_template("index.html")

@app.route("/get")
def get_bot_response():
	userText = request.args.get('msg')
	return (start(userText))


sent_check = s.Sent_Similarity()

k = aiml.Kernel()
#k.learn("std-startup.xml")
#k.respond("load aiml b")
#botName = k.getBotPredicate("name")
userName = "Anonymous"
# a global id for authentication purpose
user_auth_id=0;
#k.setPredicate('email', '')
GREETING = ['Hello! My name is P8-bot. I will try my best to provide you information related ur Query!']

DEFAULT_RESPONSES = ["I did not get you! Pardon please!","I couldn't understand what you just said! Kindly rephrase"
					 " what you said :-)", "What you are saying is out of my understanding! You can ask me"
					 " queries regrading RCOEM, your attendance and grades" ]

EMPTY_RESPONSES = ["Say something! I would love to help you!","Don't hesitate. I'll answer your queries to the best"
				   " of my knowledge!","Say my friend!"]

ONE_WORD_RESPONSES = ["Please elaborate your query for me to understand!", "I could not understand your context, please say more!",
					  "Sorry, I could not get you! Please say something more for me to understand!"]

AUTH_KEYWORDS = ['login', 'cgpa', 'sgpa', 'grades', 'gpa']

AUTH_NOT_REQD = -1
AUTH_NOT_SUCC = 0
AUTH_SUCC = 1
UNAME_REQ = 0
PWD_REQ = 0

#conn = sqlite3.connect('C:/Users/Shiva/Desktop/chatbot/seminar2_progress/shrya/db/sqlite/db/pythonsqlite.db')

#c = conn.cursor()

INVALID_UNAME_RES = ['Invalid username! Would you like to retry or have changed your mood?',
					 'Username does not exist! Would you like to retry or have changed your mood?',
					 'I suppose you forgot your username! Would you like to retry or have changed your mood?']
INVALID_PWD_RES = ['Invalid password! Would you like to retry or have changed your mood?',
					 'I suppose you forgot your password! Would you like to retry or have changed your mood?']





def conv_mapping(inp):#C:\Users\Dwithi\Desktop\chatbot
	conn = sqlite3.connect('C:/Users/Dwithi/Desktop/chatbot/seminar2_progress/shrya/db/sqlite/db/pythonsqlite.db')

	c = conn.cursor()
	new_inp = ''
	keys = map_keys.keys()
	arr = inp.split()
	for a in arr:
		if(a in keys):
			new_inp = new_inp + str(map_keys[a])
		else:
			new_inp = new_inp + a
	c.close()
	conn.close() 
	return new_inp

def printBot(msg, lst=None):
	conn = sqlite3.connect('C:/Users/Dwithi/Desktop/chatbot/seminar2_progress/shrya/db/sqlite/db/pythonsqlite.db')

	c = conn.cursor()
	print(botName+": "+msg)
	if(lst!=None):
		print(botName+": ",lst)
	c.close()
	conn.close() 
	
def match(line, word):
	conn = sqlite3.connect('C:/Users/Dwithi/Desktop/chatbot/seminar2_progress/shrya/db/sqlite/db/pythonsqlite.db')

	c = conn.cursor()
	pattern = '\\b'+word+'\\b'
	if re.search(pattern, line, re.I)!=None:
		c.close()
		conn.close() 
		return True
	c.close()
	conn.close() 
	return False

def matchingSentence(inp):
	conn = sqlite3.connect('C:/Users/Dwithi/Desktop/chatbot/seminar2_progress/shrya/db/sqlite/db/pythonsqlite.db')

	c = conn.cursor()
	f = open('C:/Users/Dwithi/Desktop/chatbot/database/questions.txt')
	match = "";
	max_score=0;
	for line in f.readlines():
		score = sent_check.symmetric_sentence_similarity(inp, line)
		if score > max_score:
			max_score = score
			match = line
	f.close()
	c.close()
	conn.close() 
	return match, max_score

def preprocess(inp):
	conn = sqlite3.connect('C:/Users/Dwithi/Desktop/chatbot/seminar2_progress/shrya/db/sqlite/db/pythonsqlite.db')

	c = conn.cursor()
	if(inp!=""):
		if inp[-1]=='.':
			inp = inp[:-1]
	# to remove . symbol between alphabets. Eg. E.G.C becomes EGC
	inp = re.sub('(?<=\\W)(?<=\\w)\\.(?=\\w)(?=\\W)','',inp) 
	# to remove - symbol between alphabet. Eg. E-G-C becomes EGC
	inp = re.sub('(?<=\\w)-(?=\\w)',' ',inp) 
	# to remove . symbol at word boundaries. Eg. .E.G.C. becomes E.G.C
	inp = re.sub('((?<=\\w)\\.(?=\\B))|((?<=\\B)\\.(?=\\w))','',inp)
	# to remove ' ' symbol in acronyms. Eg. E B C becomes EBC
	inp = re.sub('(?<=\\b\\w) (?=\\w\\b)','',inp)
	inp = inp.upper()
#    print(inp)
	c.close()
	conn.close() 
	return inp

def isKeyword(word):
	conn = sqlite3.connect('C:/Users/Dwithi/Desktop/chatbot/seminar2_progress/shrya/db/sqlite/db/pythonsqlite.db')

	c = conn.cursor()
	f = open('database/questions.txt','r')
	keywords = f.read().split()
#    print(keywords)
	if(word in keywords):
		c.close()
		conn.close() 
		return True
	else:
		c.close()
		conn.close() 
		return False

def start(inp):

	global userName,UNAME_REQ,PWD_REQ
	conn = sqlite3.connect('C:/Users/Dwithi/Desktop/chatbot/seminar2_progress/shrya/db/sqlite/db/pythonsqlite.db')

	c = conn.cursor()
	print(session.get('sid'))
	# tasks: remove punctuation from input or make it get parsed, do something when no match is found; removed last period to end sentence
	p_inp = preprocess(inp)
	# function for transfer to authentication module
	
	
	inp = p_inp
	response = k.respond(inp, session.get('sid'))
	if(response=='No match'):
		# to invalidate wrong one-word input
		if(len(inp.split(" "))==1):
			if(isKeyword(inp)==False):
				if(UNAME_REQ==1):
					k.setPredicate('email',inp, session.get('sid'))
					UNAME_REQ = 0
					PWD_REQ = 1
					c.close()
					conn.close() 
					return "Please provide me your password too!"
				if(PWD_REQ==1):
					k.setPredicate('pwd',inp, session.get('sid'))
					PWD_REQ = 0
					c.close()
					conn.close() 
					return "I'll now be able to answer your GEMS related queries if your credentials are valid! Otherwise you will have to provide your credentials again!"
				c.close()
				conn.close() 
				return(random.choice(ONE_WORD_RESPONSES))
				
		inp = matchingSentence(inp)
#        print(inp)
		response = k.respond(inp[0], session.get('sid'))
		confidence = inp[1]
		if(confidence < 0.5):
			log = open('database/invalidated_log.txt','a')
			log.write(p_inp+"\n")
			log.close()
			c.close()
			conn.close() 
			return(random.choice(DEFAULT_RESPONSES))
		else:
			response = re.sub('( )?(http:[%\-_/a-zA-z0-9\\.]*)','<a href="\\2">\\2</a>',response)
#            print(response)
			c.close()
			conn.close() 
			return(response)
	elif(response==""):
		c.close()
		conn.close() 
		return(random.choice(EMPTY_RESPONSES))
	else: 
		response = re.sub('( )?(http:[%\-_/a-zA-z0-9\\.]*)','<a href="\\2">\\2</a>',response)
		c.close()
		conn.close() 
		return (response)
	
	if(k.getPredicate('name', session.get('sid'))!=""):
		userName = k.getPredicate('name', session.get('sid'))
	else:
		k.setPredicate('name','Anonymous', session.get('sid'))
		userName = k.getPredicate('name', session.get('sid'))    

	c.close()
	conn.close() 



if __name__ == "__main__":
	app.run()
	
