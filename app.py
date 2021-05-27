"""
Usage:
 app.py [options]
 app.py -h | --help

Options:
 -h, --help            how this help message and exit
 --mode=<args>         CLI/API
 --operation=<args>    create/delete/read/update
 --target=<args>       user/task
 --user=<args>         all/user name/ new user name
 --olduser=<args>      old user name
 --task=<args>         Comma separated list of numbers
"""

import os 
from docopt import docopt
import json
from flask import Flask, request, jsonify
from flasgger import Swagger


app = Flask(__name__)
swagger = Swagger(app)

DATA_FILE = os.getcwd()+"/data.json"

def read_json():

    try:
        with open(DATA_FILE) as json_file:
            data = json.load(json_file)
    except:
        data = {}
    return data

def write_json(data):
    with open(DATA_FILE, 'w+') as json_file:
        json.dump(data, json_file)
    

# Create user 
def createUser(args):
    
    if args["--user"] != None:
        userName = args["--user"]
    else:
        return {"Text": "--user is not given."}

    if args["--task"] != None:
        task = [x for x in args["--task"].split(',')]
    else:
        task = []
    
    data = read_json()

    data[userName] = task
    
    write_json(data)

    return {"Text": "User " +userName+" created."}

# Delete user(s) 
def delUser(args):
    
    if args["--user"] != None:
        userName = args["--user"]
    else:
        return {"Text": "--user is not given."}

    data = read_json()

    if userName == "all":
        data = {}
        write_json(data)
        return {"Text": "All users are deleted."}

    if userName in data.keys():
        data.pop(userName)
        write_json(data)
        return {"Text": "User " +userName+" deleted."}
    else:
        return {"Text": "User " +userName+" not found."}

# Read user(s) 
def readUser(args):
    
    data = read_json()

    if args["--user"] != None:
        userName = args["--user"]
    else:
        return {"Text": "--user is not given."}

    if userName == "all":
        return {"Users": list(data.keys())}
    
    if userName in data.keys():
        return {"Tasks":data[userName]}
    else: 
        return {"Text": "User " +userName+" not found."}

# Update user
def updateUser(args):

    if args["--user"] != None:
        userName = args["--user"]
    else:
        return {"Text": "--user is not given."}
    
    if args["--olduser"] != None:
        oldUserName = args["--olduser"]
    else:
        return {"Text": "--olduser is not given."}

    data = read_json()

    if oldUserName in data.keys():
        
        data[userName] = data[oldUserName] 
    
        data.pop(oldUserName)
        
        write_json(data)
        
        return {"Text": "User " +userName+" updated."}

    return {"Text": userName+" not found."}

# create task 
def createTask(args):
    data = read_json()

    if args["--user"] != None:
        userName = args["--user"]
    else:
        return {"Text": "--user is not given."}

    if args["--task"] != None:
        task = [x for x in args["--task"].split(',')]
    else:
        return {"Text": "--task is not given."}
    
    if userName in data.keys():
        
        data[userName].extend(task)
        write_json(data)
        
        return {"Text": "Task [" + ', '.join(task) + "] added to " + userName +"."}
    else: 
        return {"Text": "User " +userName+" not found."}
    

# Delete task(s) 
def delTask(args):

    data = read_json()
    
    if args["--user"] != None:
        userName = args["--user"]
    else:
        return {"Text": "--user is not given."}

    if args["--task"] != None:
        task = [x for x in args["--task"].split(',')]
    else:
        return {"Text": "--task is not given."}
    
    if userName in data.keys():
        if task[0] == "all":
            data[userName] = []
            write_json(data)
            return {"Text": "All tasks of "+ userName +" are deleted."}
        
        if task[0] in data[userName]:
            data[userName].remove(task[0])
            write_json(data)
            return {"Text": "Task "+str(task)+" deleted."}
        else:
            return {"Text": "Task "+str(task)+" not found."}
    else: 
        return {"Text": "User " +userName+" not found."}
    

# Read task(s) 
def readTask(args):

    data = read_json()

    if args["--user"] != None:
        userName = args["--user"]
    else:
        return {"Text": "--user is not given."}
    
    if userName in data.keys():
        return {"Tasks":data[userName]}
    else: 
        return {"Text": userName+" not found."}

# Update task
def updateTask(args):
    
    data = read_json()

    if args["--user"] != None:
        userName = args["--user"]
    else:
        return {"Text": "--user is not given."}
    
    if args["--task"] != None:
        task = [x for x in args["--task"].split(',')]
    else:
        return {"Text": "--task is not given."}
    
    if userName in data.keys():
        data[userName] = task
        write_json(data)
        return {"Text": userName + "'s task has been updated to " + ', '.join(task)}
    else: 
        return {"Text": userName+" not found."}


def create(args):
    
    if args["--target"] != None:
        if args['--target'] == "user":
            res = createUser(args)

        if args['--target'] == "task":
            res = createTask(args)
        return res
    else:
        return {"Text": "--target is not given."}

def read(args):
    
    if args["--target"] != None:
        if args['--target'] == "user":
            res = readUser(args)

        if args['--target'] == "task":
            res = readTask(args)
        
        return res
    else:
        return {"Text": "--target is not given."}


def delete(args):
    print("heredel")
    if args["--target"] != None:
        if args['--target'] == "user":
            res = delUser(args)

        if args['--target'] == "task":
            res = delTask(args)
        
        return res
    else:
        return {"Text": "--target is not given."}


def update(args):
    
    if args["--target"] != None:
        if args['--target'] == "user":
            res = updateUser(args)

        if args['--target'] == "task":
            res = updateTask(args)
        
        return res
    else:
        return {"Text": "--target is not given."}

def main(args):   
    if args['--operation'] == "create":
        res = create(args)
    
    elif args['--operation'] == "read":
       res = read(args)
      
    elif args['--operation'] == "delete":
       res = delete(args)
      
    elif args['--operation'] == "update":
        res = update(args)
    else:
        res = {"Text":"Command not found."}
    
    print(res)
    res = json.dumps(res)
    return json.loads(res)

@app.route("/todoList", methods=["POST"])
def main_API():
    """
        file: ./swagger.yml
    """
    commands = [
                "--operation",
                "--target",
                "--user",
                "--task"
    ]
    api_args = request.json
    args = { "--"+k: v for k, v in api_args.items() }
    
    for x in commands:
        if x not in args.keys():
            args[x] = None
    
    print(args)

    res = main(args)
    print("here",res)
    return res

if __name__ == "__main__":
    args = docopt(__doc__)
    if args["--mode"]=="CLI":
        res = main(args)
        print(res)
    elif args["--mode"]=="API":
       app.run(debug=True, port=8791)
    else:
        print({"Test":"See help, -h"})
