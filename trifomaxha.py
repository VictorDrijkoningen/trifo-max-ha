import asyncio
from microdot import Microdot
import helpers


CONFIG_FILE = "/data/app/config_mono_auto_tasks.json"
# CONFIG_FILE = "config_mono_auto_tasks.json.sample"
running = True
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
    }
]



app = Microdot()

@app.route('/')
async def index(request):
    return 'Hello, world!'

@app.route('/config')
async def config(request):
    return helpers.import_config_file(CONFIG_FILE)

@app.route('/stop')
async def stop(request):
    global running
    running = False
    request.app.shutdown()
    return 'Stopping, world!'

@app.route('/config_file')
async def see(request):
    return str(helpers.import_config_file(CONFIG_FILE=CONFIG_FILE))

async def main():
    global running
    # start the server in a background task
    server = asyncio.create_task(app.start_server())

    while running:
        await asyncio.sleep(1)
        # print("running")

    await server



asyncio.run(main())