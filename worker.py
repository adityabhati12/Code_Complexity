import sys
import requests
import json
import os
import subprocess

import lizard

import CodeComplexity

if __name__ == '__main__':
    port = "8080"
    ip = "127.0.0.1"
    examined_files = 0
    reqURL = 'http://' + ip + ':' + port
    code_complex_url = reqURL + '/get_complexity_worker'
    assign_url = reqURL + '/worker_register'


    assign_response = requests.get(assign_url)
    print assign_response.text

    while True:
        working_d = requests.get(code_complex_url)
        j_data = json.loads(working_d.text)
        f_path = j_data['status']
        print ("getting from Master worker:" + str(f_path))
        if f_path == -2:
            print("ping from server")
        else:
            if f_path == -1:
                print("work done")
                break

        codecomplexity_radon = lizard.analyze_file(f_path).average_cyclomatic_complexity

        print("Code complexity of a cloned file:" + str(codecomplexity_radon))

        if codecomplexity_radon == "":
            print("No files present")
            master_response = requests.post(code_complex_url, json={'f_path': f_path, 'codecomplexity': -1})
        else:
            average_complexity = float(codecomplexity_radon)
            master_response = requests.post(code_complex_url,
                                            json={'f_path': f_path, 'codecomplexity': average_complexity})
            examined_files += 1
print("total files that are examined: ", examined_files)
