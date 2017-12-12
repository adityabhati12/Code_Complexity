from flask import Flask
from git import Repo
from flask import request
import subprocess
import os
import shutil
from dask.distributed import Client
import time


app = Flask(__name__)
s = Client('127.0.0.1:8786')


@app.route('/CODECOMPLEXITY')
def Get_repo():
    list = []
    user = request.args.get('user')
    user_name = (user.split('/')[-1]).split('.')[0]
    print user_name
    method = "C:/Users/user/Documents/Storage1/" + user_name
    Repo.clone_from(user, method)
    if os.path.isdir(user + "/.git"):
        shutil.rmtree(user + "/.git")
    method = os.path.expanduser(method)
    if os.path.isdir(method):
        os.path.walk(method, create_blocks, list)
    print len(list)

    distributed_codecomplexity(list)
    # if os.path.isdir(method):
    #     shutil.rmtree(method)
    return 'repository cloned'

def create_blocks(list, blocks , directory):
    size = len(blocks)
    for block in blocks:
        if blocks.endswith('.py'):
            list.append(str(os.path.join(directory, blocks).encode('ascii', 'ignore')))



def cyclomatic_c(method):
    r_cc = subprocess.Popen(["radon raw \"" + method + "\" -s -j"], stdout=subprocess.PIPE, shell=True,
                                      executable='/bin/bash')
    cc = subprocess.Popen(["radon cc \"" + method + "\" -s -j"], stdout=subprocess.PIPE, shell=True,
                                             executable='/bin/bash')
    (r_cc_output, a1) = r_cc.communicate()
    (cc ,a2) = cc.communicate()
    return cc + r_cc_output
    print (cc + r_cc_output)



def distributed_codecomplexity(list):
    t1 = time.time()
    mapper = s.map(cyclomatic_c, list )
    print s.gather(mapper)
    print("%s" % (time.time()-t1))


if __name__ == '__main__':
    app.run()
