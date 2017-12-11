from flask import Flask
from git import Repo
import os
import git
import shutil
import time

app = Flask(__name__)


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







if __name__ == '__main__':
    app.run()
