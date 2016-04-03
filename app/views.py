
from flask import request
from flask import jsonify
from flask import redirect
from app import app
from flask import render_template
import os,time
import subprocess

@app.route('/')
def index():
    return "Hi there"

@app.route('/start')
def start():
    remoteAddress = request.remote_addr
    cmd = ["bash","launcher.sh", remoteAddress]
    p = subprocess.Popen(cmd, preexec_fn=os.setpgrp, shell= False, stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    print "Mavproxy started"
   
    # cmdParams = " --master=" + remoteAddress + ":5760 --out=" + remoteAddress + ":14550 --out=" + remoteAddress + ":1244"
    # cmd = ["sudo","mavproxy.py",cmdParams]
    # p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    # out,err = p.communicate()
    # return out + "=" + cmdParams
    cmd1 = ["python", "/home/pi/copter/mdc.py"]
    p=subprocess.Popen(cmd1, preexec_fn=os.setpgrp, stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    print "mdc.py started"
    
    cmd2 = ["python", "/home/pi/copter/webUpdate.py"]
    p=subprocess.Popen(cmd2, preexec_fn=os.setpgrp, stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    print "webUpdate started"
    url = 'http://10.0.0.253/index.html'
    return redirect(url, code=307) 

@app.route('/simulator')
def simulator():
    remoteAddress = request.remote_addr
    cmd = ["bash","launcherSim.sh", remoteAddress]
    p = subprocess.Popen(cmd, preexec_fn=os.setpgrp, shell= False, stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    print "Mavproxy started"
    url = 'http://10.0.0.253/index.html'
    return redirect(url, code=307)  
    # cmdParams = " --master=" + remoteAddress + ":5760 --out=" + remoteAddress + ":14550 --out=" + remoteAddress + ":1244"
    # cmd = ["sudo","mavproxy.py",cmdParams]
    # p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    # out,err = p.communicate()
    # return out + "=" + cmdParams
    #cmd1 = ["python", "/home/pi/copter/mdc.py"]
    #p=subprocess.Popen(cmd1, preexec_fn=os.setpgrp, stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    #print "mdc.py started"
    
    #cmd2 = ["python", "/home/pi/copter/webUpdate.py"]
    p=subprocess.Popen(cmd2, preexec_fn=os.setpgrp, stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    #print "webUpdate started"
    #return "ready to fly !"
