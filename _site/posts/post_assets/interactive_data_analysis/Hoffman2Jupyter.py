#!/usr/bin/env python
from __future__ import print_function
"""In order to use the script you need to copy your SSH key to the target server
and also copy the server SSH public key (usually .ssh/id_rsa.pub) to .ssh/authorized_keys,
so that the computing node can ssh passwordless to the login node"""

from subprocess import Popen, PIPE, call
import sys
import webbrowser
from getopt import getopt
import time
import os
#import exceptions
import platform

import sys, getopt
import os
#import exceptions

username = ''
username = str(username)
timeinhours = 1
timeinhours = int(timeinhours)
memoryingb = 1
memoryingb = int(memoryingb)
numberofslots = 1
numberofslots = int(numberofslots)
port = 8789
port=int(port)
directory = ''
directory = str(directory)
opsys = platform.system()
opsys = str(opsys)
pythonver = '3.6.1'
pythonver = str(pythonver)


if sys.version_info<(2,6,0):
  sys.stderr.write("You need python 2.6 or later to run this script\n")
  exit(1)


if opsys == 'Windows':
    try:
        mytest = call(['where','plink'])
    except:
        print("It appears that the program plink is not installed")
        print("on your computer or not available in your path.")
        print("Install Plink, a command-line interface to the PuTTY back")
        print("ends. Availabe at: ")
        print("http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html")
        print("and add it to the system path via control panel")
        sys.exit(2)

else:
    myssh = 'ssh'


def main(argv):
    global  username, timeinhours, memoryingb, numberofslots, pythonver, port, directory
    try:
        opts, args = getopt.getopt(argv,"h:u:t:m:s:v:p:d:",["user=","time=","memory=","slots=","version=","port=","dir="])
    except getopt.GetoptError:
        print("Usage:")
        print("\n\t h2ipynb [-u <Hoffman2 user name>] [-t <time in hours>] [-m <memory in GB>] [-s <number of slots>] [-v <python-version>] [-p <port>] [-d <dir>] \n")
        print("If no arguments are given to this script it is assumed that:")
        print("\t your Hoffman2 user name is the same as on your client machine")
        print("\t the time duration for your session is of 2 hours")
        print("\t the memory per slot for your session is of 1GB")
        print("\t the number of slots for your session is of 1")
        print("\t the python version for your notebook is 2.7.3")
        print("\t the port on which the server is started is 8789")
        print("\t the starting directory on Hoffman2 is your $HOME")
        print("\n\t python versions currently available are 2.7.3 or 3.4 \n")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("h2ipynb -u <Hoffman2 user name> -t <time in hours> [-p <port> [-d <dir>]")
            sys.exit()
        elif opt in ("-u", "--user"):
            username = arg
            username = str(username)
        elif opt in ("-t", "--time"):
            timeinhours = arg
            try:
                timeinhours=int(timeinhours)
            except exceptions.KeyError:
                print("Setting the time to 2 hours...")
                timeinhours = 2
        elif opt in ("-m", "--memory"):
            memoryingb = arg
            try:
                memoryingb=int(memoryingb)
            except exceptions.KeyError:
                print("Setting the memory to 1GB...")
                memoryingb = 1
        elif opt in ("-s", "--slots"):
            numberofslots = arg
            try:
                numberofslots=int(numberofslots)
            except exceptions.KeyError:
                print("Setting the number of slots to 1...")
                numberofslots = 1
        elif opt in ("-v", "--version"):
            pythonver = arg
            pythonver = str(pythonver)
            if (not pythonver == '2.7.3') and (not pythonver == '3.4'):
                print("version ,pythonver, of python not available")
                print("setting python version to 2.7.3")
                pythonver = '2.7.3'
        elif opt in ("-p", "--port"):
            port = arg
            try:
                port=int(port)
            except exceptions.KeyError:
                print("Setting the port to 2 8789...")
                port = 8789
        elif opt in ("-d", "--dir"):
            directory = (arg,None)
            directory = str(directory)
        else:
            print("Usage:")
            print("\n\t h2jupyter [-u <Hoffman2 user name>] [-t <time in hours>] [-m <memory in GB>] [-s <number of slots>] [-v <python-version>] [-p <port>] [-d <dir>] \n")
            print("If no arguments are given to this script it is assumed that:")
            print("\t your Hoffman2 user name is the same as on your client machine")
            print("\t the time duration for your session is of 2 hours")
            print("\t the memory per slot for your session is of 1GB")
            print("\t the number of slots for your session is of 1")
            print("\t the python version for your notebook is 2.7.3")
            print("\t the port on which the server is started is 8789")
            print("\t the starting directory on Hoffman2 is your $HOME")
            sys.exit(2)

    if not username:
        username = str(os.environ["USER"])


    print("Your Hoffman2 user name is", username )
    print("The time in hours is", timeinhours )
    print("The memory in GB per slots is", memoryingb)
    print("The number of slots is", numberofslots)
    print("The version of python for the notebook is", pythonver)
    print("The port is" , port)
    if not directory:
        print("The directory on Hoffman2 is $HOME")
    else:
        print("The directory on Hoffman2 is", directory)

if __name__ == "__main__":
   main(sys.argv[1:])

QSUB_TEMPLATE = os.environ.get("IPYNB_QSUB_TEMPLATE", "qrsh -l i,h_rt=%d:00:00,h_data=%dg -pe shared %d")
MODULE_LOAD_TEMP = "module load python/%s"

def readwhile(stream,func):
    while True:
        line = stream.readline()
        if line!='':
            print(line[:-1])
            if func(line): break
        else:
            raise Exception("Disconnected unexpectedly.")

if opsys == 'Windows':
    pqsub=Popen(['plink','-t','-t','-4','%s@hoffman2.idre.ucla.edu' % username],stdin=PIPE,stdout=PIPE,stderr=PIPE,universal_newlines=True)
else:
    pqsub=Popen(['ssh','-t','-t','-4','%s@hoffman2.idre.ucla.edu' % username],stdin=PIPE,stdout=PIPE,stderr=PIPE,universal_newlines=True)

#pqsub.stdin.write(bytearray((QSUB_TEMPLATE % (timeinhours,memoryingb,numberofslots))+"\n","ascii"))
pqsub.stdin.write((QSUB_TEMPLATE % (timeinhours,memoryingb,numberofslots))+"\n")
##pqsub.stdin.write(('module load python/2.7.3')+"\n")
# pqsub.stdin.write(MODULE_LOAD_TEMP % (pythonver)+"\n","ascii"))
# pqsub.stdin.write(bytearray('echo HOSTNAME=`hostname`\n',"ascii"))
pqsub.stdin.write(MODULE_LOAD_TEMP % (pythonver)+"\n")
pqsub.stdin.write('echo HOSTNAME=`hostname`\n')
pqsub.stdin.flush()

def gethostname(line):
    global hostname
    if line.startswith('HOSTNAME'):
        hostname = line.split('=')[1].strip()
        return True

readwhile(pqsub.stdout, gethostname)

if directory:
    pqsub.stdin.write('cd %s\n'%directory)
    pqsub.stdin.write('echo CD\n')
    #readwhile(pqsub.stdout, lambda line: line.startswith('CD'))


pqsub.stdin.write('jupyter notebook --port=%s\n'%port)
pqsub.stdin.flush()
readwhile(pqsub.stdout, lambda line: line.find('NotebookApp')>0)

if myssh == 'ssh':
    tunnel = ['ssh','-4', '-t', '-Y', '%s@hoffman2.idre.ucla.edu' % username, '-L', '%s:localhost:%s'%(port,port), 'ssh', '-t', '-Y', hostname, '-L', '%s:localhost:%s'%(port,port)]
elif myssh == 'plink':
    tunnel = ['plink','-4', '-t', '-X', '%s@hoffman2.idre.ucla.edu' % username, '-L', '%s:localhost:%s'%(port,port), 'ssh', '-t', '-X', hostname, '-L', '%s:localhost:%s'%(port,port)]

print(' '.join(tunnel))
print(tunnel)

ptunnel = Popen(tunnel,stdout=PIPE,stdin=PIPE,universal_newlines=True)
ptunnel.stdin.write('echo TUNNEL\n')
ptunnel.stdin.flush()

readwhile(ptunnel.stdout,lambda line: line.startswith('TUNNEL'))

webbrowser.open('http://localhost:%s'%(port))

print("Succesfully opened notebook!")
print("Kill this process to end your notebook connection.")

time.sleep(timeinhours*3600)

pqsub.kill()
ptunnel.kill()


print("Succesfully cleaned up connections.")
