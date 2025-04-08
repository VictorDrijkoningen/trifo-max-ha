import json

CONFIG_FILE = "/data/app/config_mono_auto_tasks.json"
# CONFIG_FILE = "config_mono_auto_tasks.json.sample"


def import_config_file():
    global CONFIG_FILE
    with open(CONFIG_FILE, 'r') as f:
        config_data = json.load(f)
    return config_data


def export_config_file(tasks:list):
    cnt = 0
    export = dict()
    export['name'] = 'auto-work'
    data_list = list()

    for task in tasks:
        export_task = dict()
        export_task['id'] = str(cnt)
        export_task['status'] = task['status']
        export_task['mode'] = task['mode']
        export_task['time'] = task['time']
        export_task['repeat'] = task['repeat']
        export_task['mopping_mode'] = task['mopping_mode']
        export_task['invalid'] = task['invalid']
        export_task['clean_area'] = list()

        cnt += 1
        data_list.append(export_task)

    export['cnt'] = str(cnt)
    export['data'] = data_list

    with open(CONFIG_FILE+"compare", 'w') as f:
        json.dump(export, f, indent=4)

def run():
    tasks = [
        {
            "status": "true",
            "mode": "1",
            "time": "09:30",
            "repeat": "1000000",
            "mopping_mode": "2",
            "invalid": "false",
            "clean_area": [
                
            ]
        },
        {
            "status": "true",
            "mode": "1",
            "time": "09:30",
            "repeat": "0010000",
            "mopping_mode": "0",
            "invalid": "false",
            "clean_area": [
                
            ]
        },
        {
            "status": "true",
            "mode": "2",
            "time": "09:30",
            "repeat": "0000100",
            "mopping_mode": "0",
            "invalid": "false",
            "clean_area": [
                
            ]
        },
        {
            "status": "false",
            "mode": "0",
            "time": "15:49",
            "repeat": "0000000",
            "mopping_mode": "0",
            "invalid": "false",
            "clean_area": [
                
            ]
        }
    ]
    print(import_config_file())




run()

import helpers

print(helpers.test())

import asyncio
from microdot import Microdot

app = Microdot()

@app.route('/')
async def index(request):
    return 'Hello, world!'

async def main():
    # start the server in a background task
    server = asyncio.create_task(app.start_server())

    # ... do other asynchronous work here ...
    while True:
        await asyncio.sleep(1)
    # cleanup before ending the application
    await server

asyncio.gather(main())