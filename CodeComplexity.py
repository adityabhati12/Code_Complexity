from flask import Flask
from git import Repo
import subprocess
import os
import git
import shutil
from dask.distributed import Client
import time


app = Flask(__name__)
client = Client('127.0.0.1:8786')


@app.route('/CODECOMPLEXITY')
def Get_repo():
    DIR_NAME = "C:/Users/user/PycharmProjects1"
    REMOTE_URL = "https://github.com/adityabhati12/SCALABLE-COMPUTING---CHAT-SERVER.git"
    Repo.clone_from(REMOTE_URL, DIR_NAME)
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
    (r_output, a1) = r_cc.communicate()
    (cc ,a2) = cc.communicate()
    return cc + r_output


def distributed_codecomplexity(blocks):
    t1 = time.time()
    mapper = client.map(cyclomatic_c, blocks )
    print client.gather(mapper)
    print("%s" % (time.time()-t1))




if __name__ == '__main__':
    app.run()
