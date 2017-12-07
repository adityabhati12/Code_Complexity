from flask import Flask
from git import Repo
import os
import git
import shutil

app = Flask(__name__)

@app.route('/')
def Get_repo():
    DIR_NAME = "C:/Users/user/PycharmProjects1"
    REMOTE_URL = "https://github.com/adityabhati12/SCALABLE-COMPUTING---CHAT-SERVER.git"
    Repo.clone_from(REMOTE_URL, DIR_NAME)
    return 'repository cloned'


if __name__ == '__main__':
    app.run()
