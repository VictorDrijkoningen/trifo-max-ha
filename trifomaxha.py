import asyncio
from microdot import Microdot
from auth import BasicAuth
import helpers
from ws import with_websocket
import ssl
import os
import zmq

CONFIG_FILE = "/data/app/config_mono_auto_tasks.json"
ENV_FILE = "./trifomaxha_env.json"
SSL_FILES = ("./trifomaxha_cert.pem", "./trifomaxha_key.pem")
running = True
helpers.check_auto_start()
env = helpers.check_env_file(ENV_FILE)
helpers.check_ssl_pem_files(SSL_FILES, env, ENV_FILE)
simple_schema = helpers.get_simple_schema(CONFIG_FILE)

app = Microdot()
auth = BasicAuth(app)

@auth.authenticate
async def verify_user(request, username, password):
    if "password" in request.args.keys() and env['webserver_access_key'] == request.args['password']:
        print(f"successful login from {str(request.client_addr)} with args")
        return True
    elif password == env['webserver_access_key']:
        print(f"successful login from {str(request.client_addr)} with basicauth")
        return True
    else:
        print(f"wrong login from {str(request.client_addr)}")

@app.route('/')
async def index(request):
    return helpers.index_page(), {'Content-Type': 'text/html'}

@app.route('/configfile')
@auth
async def configfile(request):
    return helpers.import_config_file(CONFIG_FILE)

@app.route('/settings')
@auth
async def settings(request):
    return helpers.settings_page(CONFIG_FILE), {'Content-Type': 'text/html'}

@app.route('/stop')
@auth
async def stop(request):
    global running
    running = False
    request.app.shutdown()
    return 'Stopping server...'


@app.route('/websocket')
@with_websocket
@auth
async def websocket(request, ws):
    global simple_schema
    global env
    while True:
        message = await ws.receive()
        print("ws: "+message)
        helpers.change_setting(CONFIG_FILE, message, simple_schema, env)


async def main():
    global running
    # start the server in a background task
    sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslctx.load_cert_chain(*SSL_FILES)
    server = asyncio.create_task(app.start_server(port=443,ssl=sslctx))
    print("started webserver on port 443")
    print(f"running pid {os.getpid()}")

    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to hello world server…")
    socket = context.socket(zmq.REQ)
    socket.connect("/tmp/TrifoIPC_sensor_node-robot_control_REQ")

    #  Do 10 requests, waiting each time for a response
    for request in range(5):
        print("Sending request %s …" % request)
        socket.send(b"Hello")

        #  Get the reply.
        message = socket.recv()
        print("Received reply %s [ %s ]" % (request, message))

    while running:
        await asyncio.sleep(1)

    await server


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("exiting")