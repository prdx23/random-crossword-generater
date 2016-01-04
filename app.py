
from classes import *
import code as code
import info as info

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import threading
import os

#from werkzeug.contrib.fixers import ProxyFix
#app.wsgi_app = ProxyFix(app.wsgi_app)

class Thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        code.main()
        self.exit()



app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('step1.html')

@app.route('/step1/', methods=["GET","POST"])
def step1():
	return render_template('step1.html')

@app.route('/home/', methods=["GET","POST"])
def home():
	return render_template('step1.html')

@app.route('/loading/', methods=["GET","POST"])
def loading():
	try:
		if request.method == "POST":
			b,w,s = int(request.form['boardsize']),int(request.form['wordno']),int(request.form['sec'])
			code.size = b
			code.wordnum = w
			code.sec = s
			thread_main = Thread()
			thread_main.start()
			return render_template('loading.html')

	except Exception as e:
		print e.message
		return e.message   

@app.route('/_info_/')
def display_info():
	try:
		return  info.info_string
	except Exception as e:
		return e.message

@app.route('/_output_/', methods=["GET","POST"])
def output():
	return render_template('output.html', grid = info.grid, gridnum = info.gridnum , wordlist = info.wordlist)

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(threaded=True,port=port)