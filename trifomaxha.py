import asyncio
from microdot import Microdot
import helpers
from ws import with_websocket
import json
import os

CONFIG_FILE = "/data/app/config_mono_auto_tasks.json"
running = True
helpers.check_auto_start()

simple_schema = helpers.get_simple_schema(CONFIG_FILE)

app = Microdot()

@app.route('/')
async def index(request):
    return helpers.index_page(), {'Content-Type': 'text/html'}

@app.route('/configfile')
async def configfile(request):
    return helpers.import_config_file(CONFIG_FILE)

@app.route('/settings')
async def settings(request):
    return helpers.settings_page(CONFIG_FILE), {'Content-Type': 'text/html'}

@app.route('/stop')
async def stop(request):
    global running
    running = False
    request.app.shutdown()
    return 'Stopping server...'


@app.route('/websocket')
@with_websocket
async def websocket(request, ws):
    global simple_schema
    while True:
        message = await ws.receive()
        print("ws: "+message)
        helpers.change_setting(CONFIG_FILE, message, simple_schema)



@app.route('/config_file')
async def see(request):
    return str(helpers.import_config_file(CONFIG_FILE=CONFIG_FILE))

async def main():
    global running
    # start the server in a background task
    server = asyncio.create_task(app.start_server())

    while running:
        await asyncio.sleep(1)

    await server


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("exiting")