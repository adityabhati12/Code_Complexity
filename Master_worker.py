from flask import Flask
import time
import CodeComplexity
from flask import request
from flask import jsonify
import os
import shutil

app = Flask(__name__)

#this functions is used register worker
@app.route('/worker_register', methods=['GET'])
def worker_register():
    print " Assigning worker to the master "
    Manager.curr_slave += 1
    if Manager.curr_slave == Manager.count_slv:
        Manager.begin = time.time()
    return "worker assigned"

#this is used to assign work to the worker
@app.route('/get_complexity_worker', methods=['GET'])
def calling_worker():
    if Manager.curr_slave < Manager.count_slv:
        time.sleep(0.1)
        return jsonify({'status': -2})
    if len(Manager.f_list ) == 0:
        return jsonify({'status': -1})
    f_path = Manager.f_list [0]
    del Manager.f_list [0]
    print "giving work to the worker :"+f_path
    return jsonify({'status': f_path})

#to get the complexity of each worker
@app.route('/get_complexity_worker', methods=['POST'])
def get_complexity_worker():
    f_path = request.args.get('f_path')
    code_complexity_req = request.json
    f_path= code_complexity_req['f_path']
    code_complexity= code_complexity_req['codecomplexity']
    print code_complexity
    Manager.cc_list.append({'f_path': f_path, 'codecomplexity': code_complexity})
    if len(Manager.cc_list) == Manager.total_file:
        end_t = time.time() - Manager.begin
        print("Time taken for execution: ", end_t)
        print("Number of Files that are analysed"+ str(len(Manager.cc_list)))
        print Manager.cc_list
        average_complexity = 0
        for i in Manager.cc_list:
            if i['codecomplexity'] > 0:
                average_complexity += i['codecomplexity']
            else:
                print("No files to be analyzed")
        average_complexity = average_complexity / len(Manager.cc_list)
        print("Average cyclomatic complexity Repository: ", average_complexity)
        if os.path.isdir(Manager.path):
            shutil.rmtree(Manager.path)

    return jsonify({'Working!!!!': True})


#class Manager for handling workers
class Manager:

    def __init__(self):
        self.cc_list = []
        self.curr_slave = 0
        self.count_slv = 1
        self.begin  = 0.0
        f_list , path = CodeComplexity.Get_repo("https://github.com/adityabhati12/SCALABLE-COMPUTING---CHAT-SERVER.git", True)
        self.path = path
        self.f_list  = f_list
        self.total_file = len(self.f_list )
        print("Number of commits: {}".format(self.total_file))

if __name__ == '__main__':
    Manager = Manager()
    app.run(port =8080)