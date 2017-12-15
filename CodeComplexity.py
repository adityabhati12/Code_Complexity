from flask import Flask
from git import Repo
from flask import request
import subprocess
import os
import shutil
from dask.distributed import Client
import time
import json

"""
Program to develop Rest service and calculating Cyclomatic Complexity of a cloned repositor
using Radon  package

Dask Api was used to perform distributed computing in python
"""

app = Flask(__name__) #a REST Service using dask


@app.route('/codeComplexity')
def Get_repo(git_url, manual= False):
    list = []
    if manual:
        user_url = git_url
    else:
        user_url = request.args.get('user_url')
    user_name = (user_url.split('/')[-1]).split('.')[0]
    print user_name
    dest = "/adi_repo/" + user_name
    Repo.clone_from(user_url, dest)#cloning the user_url to the given path
    if os.path.isdir(user_url + "/.git"):
        shutil.rmtree(user_url + "/.git")#removing directory and subdirectories from the specified path
    dest = os.path.expanduser(dest)# used for expansion of path
    if os.path.isdir(dest):# true if path exists and is a directory
        os.path.walk(dest, create_blocks, list)#specificies visited directory and lists the files in the directory
    print len(list)
    return list, dest


def cyclomatic_c(dest): #function to perform analysis of cc

    cc = subprocess.Popen(["radon cc \"" + dest + "\" -s -j"], stdout=subprocess.PIPE, shell=True,
                                             executable='/bin/bash') #CC= codeComplexity
    (cc ,a2) = cc.communicate()#executing cyclomatic complexity, a2 = error
    return json.loads(cc)


def distributed_codecomplexity(list): #calculating codecomplexity of a distributed system
    t1 = time.time()

    mapper = s.map(cyclomatic_c, list ) # s is Client
    print s.gather(mapper)
    print("%s" % (time.time()-t1))
    return json.dumps(mapper)


def remove_files(dest):#function to remove directory tree
    if os.path.isdir(dest + "/.git"):
        shutil.rmtree(dest + "/.git")



def create_blocks(list, blocks , directory):
    size = len(blocks)
    for block in directory:
        if block.endswith('.py'):
            list.append(str(os.path.join(blocks, block).encode('ascii', 'ignore')))#adding path to the directory and converting a unicode string into ASCII









if __name__ == '__main__':
    s = Client('127.0.0.1:8786')

    app.run()
