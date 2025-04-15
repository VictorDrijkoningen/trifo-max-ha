import asyncio
from microdot import Microdot
from auth import BasicAuth
import helpers
from ws import with_websocket
import ssl

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
    print(request)
    if password == env['webserver_access_key']:
        print(f"successful login from {str(request.client_addr)}")
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

    while running:
        await asyncio.sleep(1)

    await server


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("exiting")