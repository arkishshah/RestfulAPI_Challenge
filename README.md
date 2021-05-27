# TODO list collection application.

Help User to store a TODO-list in their terminal and content of the TODO-list persist on system reboot.

## Features

- CRUD operations can be performed on users/tasks
- TODO-list can be operated/accessible from both CLI and API
- TODO-list is saved in JSON file so it can remains after system reboot.

### File Structure

| File Name       | Desc                                                     |
| --------------- | -------------------------------------------------------- |
| app.py          | Main code file. Contains all functionality.              |
| Readme.md       | Documentation on how to use/run this application.        |
| swagger.yml     | Documentation on API endpoints and parameters            |
| Makefile        | To create Virtual environment and setup all things       |
| data.json       | Data storage file contains users and tasks               |
| Requirement.txt | List of python libraries to required by this application |

### Instruction

For Creation of environments.

```sh
pip3 install make
make develop
make test
```

For Run service.

```sh
source ./venv/bin/activate
```

CLI arguments

```
python3 app.py --mode=CLI
```

```
Usage: app.py [options]
       app.py -h | --help

Options:
  -h, --help            Help message
  --mode=<args>         CLI/API
  --operation=<args>    create/delete/read/update
  --target=<args>       user/task
  --user=<args>         all/user_name
  --olduser=<args>      old user name
  --task=<args>         Comma separated list of numbers eg. ["walk","run"]

 Response:
    {"Text":status of operation performed}
```

```
 Example1: python3 app.py --mode=CLI --operation=create --target=user --user=sam --task="walk"
 Example2: python3 app.py --mode=CLI --operation=read --target=user --user=sam
 Example3: python3 app.py --mode=CLI --operation=delete --target=user --user=sam
 Example4: python3 app.py --mode=CLI --operation=create --target=task --user=sam --task="walk","run"
 Example5: python3 app.py --mode=CLI --operation=read --target=task --user=sam
 Example6: python3 app.py --mode=CLI --operation=delete --target=task --user=sam --task="run"
 Example7: python3 app.py --mode=CLI --operation=update --target=user --user=alex --olduser=bob
 Example8: python3 app.py --mode=CLI --operation=update --target=task --user=alex --task=walk,run

```

API arguments

```sh
python3 app.py --mode=API
```

```
Endpoint = http://127.0.0.1:8791/apidocs
Method = POST
Body =  {
        operation = string      Which operation of CRUD to perform. eg = create/update/update/delete
        target = string         On whom operation has to perform. eg = users/task
        task =	string          Take user's task list OR "all" to read/delete all tasks
        user = string          Take user's name OR "all" to read/delete all users
        }
Response = {"Text":status of operation performed}
```

```
Example1: Body = {
                  "operation": "update",
                  "target": "task",
                  "task": ["swim"],
                  "user": "sam"
                }
```
