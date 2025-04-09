import os
import json

def check_env_file(ENV_FILE: str) -> dict:
    try:
        with open(ENV_FILE, "r") as f:
            env = json.load(f)
    except:
        env = dict()

    if not "timezone" in env.keys():
        env['timezone'] = 0
        save_env_file(ENV_FILE, env)
    return env

def save_env_file(ENV_FILE: str, env: dict) -> None:
    with open(ENV_FILE, "w") as f:
        json.dump(env, f)
    

def wraps(wrapped):
    def _(wrapper):
        return wrapper
    return _

def check_auto_start() -> None:
    if not os.path.isfile('/etc/init.d/S90trifomaxha.sh'):
        with open("/etc/init.d/S90trifomaxha.sh", 'w') as f:
            f.write("""#! /bin/sh
cd /root
mv ./trifomaxha.py-aarch64 ./trifomaxha.py-aarch64.current
./trifomaxha.py-aarch64.current > trifomaxha.log &
""")
        print("installed autostart file")

def get_simple_schema(CONFIG_FILE):
    config_data = import_config_file(CONFIG_FILE)

    if len(config_data['data']) == 7:
        simple_schema = [
            {'status': config_data['data'][0]['status'], 'time': config_data['data'][0]['time']},
            {'status': config_data['data'][1]['status'], 'time': config_data['data'][1]['time']},
            {'status': config_data['data'][2]['status'], 'time': config_data['data'][2]['time']},
            {'status': config_data['data'][3]['status'], 'time': config_data['data'][3]['time']},
            {'status': config_data['data'][4]['status'], 'time': config_data['data'][4]['time']},
            {'status': config_data['data'][5]['status'], 'time': config_data['data'][5]['time']},
            {'status': config_data['data'][6]['status'], 'time': config_data['data'][6]['time']},

        ]
    else:
        simple_schema = [
            {'status': "false", 'time': '00:00'},
            {'status': "false", 'time': '00:00'},
            {'status': "false", 'time': '00:00'},
            {'status': "false", 'time': '00:00'},
            {'status': "false", 'time': '00:00'},
            {'status': "false", 'time': '00:00'},
            {'status': "false", 'time': '00:00'},

        ]
        export_config_file(CONFIG_FILE, simple_schema)
    return simple_schema

def export_config_file(CONFIG_FILE, simpledata:list):
    export = dict()
    export['name'] = 'auto-work'
    data_list = list()

    for num in range(7):
        export_task = dict()
        export_task['id'] = str(num)
        export_task['status'] = simpledata[num]['status']
        export_task['mode'] = str(1)
        export_task['time'] = simpledata[num]['time']
        export_task['repeat'] = num*"0" + "1" + (6-num)*"0"
        export_task['mopping_mode'] = str(0)
        export_task['invalid'] = 'false'
        export_task['clean_area'] = list()

        data_list.append(export_task)

    export['cnt'] = str(7)
    export['data'] = data_list

    with open(CONFIG_FILE, 'w') as f:
        json.dump(export, f, indent=4)


def export_config_file_old(CONFIG_FILE, tasks:list):
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


def import_config_file(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        config_data = json.load(f)
    return config_data

def change_setting(CONFIG_FILE, message, simple_schema):
    try:
        message = json.loads(message)
        if "mondaytime" in message.keys():
            simple_schema[0]['time'] = message['mondaytime']
        if "tuesdaytime" in message.keys():
            simple_schema[1]['time'] = message['tuesdaytime']
        if "wednesdaytime" in message.keys():
            simple_schema[2]['time'] = message['wednesdaytime']
        if "thursdaytime" in message.keys():
            simple_schema[3]['time'] = message['thursdaytime']
        if "fridaytime" in message.keys():
            simple_schema[4]['time'] = message['fridaytime']
        if "saturdaytime" in message.keys():
            simple_schema[5]['time'] = message['saturdaytime']
        if "sundaytime" in message.keys():
            simple_schema[6]['time'] = message['sundaytime']
        
        if "mondaystatus" in message.keys():
            if message['mondaystatus'] == True:
                simple_schema[0]['status'] = "true"
            else:
                simple_schema[0]['status'] = "false"
        if "tuesdaystatus" in message.keys():
            if message['tuesdaystatus'] == True:
                simple_schema[1]['status'] = True
            else:
                simple_schema[1]['status'] = "false"
        if "wednesdaystatus" in message.keys():
            if message['wednesdaystatus'] == True:
                simple_schema[2]['status'] = "true"
            else:
                simple_schema[2]['status'] = "false"
        if "thursdaystatus" in message.keys():
            if message['thursdaystatus'] == True:
                simple_schema[3]['status'] = "true"
            else:
                simple_schema[3]['status'] = "false"
        if "fridaystatus" in message.keys():
            if message['fridaystatus'] == True:
                simple_schema[4]['status'] = "true"
            else:
                simple_schema[4]['status'] = "false"
        if "saturdaystatus" in message.keys():
            if message['saturdaystatus'] == True:
                simple_schema[5]['status'] = "true"
            else:
                simple_schema[5]['status'] = "false"
        if "sundaystatus" in message.keys():
            if message['sundaystatus'] == True:
                simple_schema[6]['status'] = "true"
            else:
                simple_schema[6]['status'] = "false"
        if "SUBMIT" in message.keys():
            os.system("reboot")
        
        export_config_file(CONFIG_FILE, simple_schema)
    except Exception as e:
        print(f"Malformed json {e}")

def index_page():
    out = """
<!DOCTYPE html>
<html>
    <head> 
    </head>
    <body style="text-align: center;">     
        <table>
            <thead>
            </thead>
            <tbody>
                <tr>
                    <td></td>
                    <td>
                        <div style="text-align: center;">
                            <h3>MAX Web Server</h3>
                            <button onclick="location.href='/stop'"> STOP webserver </button>
                        </div>
                    </td>
                    <td></td>
                </tr>

                
                <tr>
                    <td>Enabled</td>
                    <td>Day</td>
                    <td>Time in UTC</td>
                </tr>



                <tr>
                    <td>
                        <div style="text-align: center;">
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <p>
                                <button onclick="location.href='/settings'">Change time schedule</button>
                            </p>
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                        </div>
                    </td>
                </tr>


                <tr>
                    <td>
                        <div style="text-align: center;">
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <p>
                                1
                            </p>
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                        </div>
                    </td>
                </tr>

                <tr>
                    <td>
                        <div style="text-align: center;">
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <p>
                                2
                            </p>
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>

        <script type="text/javascript">

        </script>

    </body>
</html>

"""

    return out
def settings_page(CONFIG_FILE):
    config_data = import_config_file(CONFIG_FILE)
    out = """
<!DOCTYPE html>
<html>
    <head> 
    </head>
    <body style="text-align: center;">     
        <table>
            <thead>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <button onclick="location.href='/'">Back</button>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <h3>MAX Web Server</h3>
                            <button onclick="location.href='/stop'"> STOP webserver </button>
                        </div>
                    </td>
                    <td></td>
                </tr>




                <tr>
                    <td>
                        <div style="text-align: center;">
                            <input onchange="mondaystatus()" type="checkbox"  id="mondaystatus" """+ str("checked" if config_data['data'][0]['status'] == "true" else "")+""">
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <p>
                                MONDAY
                            </p>
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <input type="time" onchange="mondaytime()" id="mondaytime" value='"""+ config_data['data'][0]['time']+"""'>
                        </div>
                    </td>
                </tr>


                <tr>
                    <td>
                        <div style="text-align: center;">
                            <input onchange="tuesdaystatus()" type="checkbox"  id="tuesdaystatus" """+ str("checked" if config_data['data'][1]['status'] == "true" else "")+""">
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <p>
                                TUESDAY
                            </p>
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <input type="time" onchange="tuesdaytime()" id="tuesdaytime" value='"""+ config_data['data'][1]['time']+"""'>
                        </div>
                    </td>
                </tr>

                <tr>
                    <td>
                        <div style="text-align: center;">
                            <input onchange="wednesdaystatus()" type="checkbox"  id="wednesdaystatus" """+ str("checked" if config_data['data'][2]['status'] == "true" else "")+""">
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <p>
                                WEDNESDAY
                            </p>
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <input type="time" onchange="wednesdaytime()" id="wednesdaytime" value='"""+ config_data['data'][2]['time']+"""'>
                        </div>
                    </td>
                </tr>

                <tr>
                    <td>
                        <div style="text-align: center;">
                            <input onchange="thursdaystatus()" type="checkbox"  id="thursdaystatus" """+ str("checked" if config_data['data'][3]['status'] == "true" else "")+""">
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <p>
                                THURSDAY
                            </p>
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <input type="time" onchange="thursdaytime()" id="thursdaytime" value='"""+ config_data['data'][3]['time']+"""'>
                        </div>
                    </td>
                </tr>

                <tr>
                    <td>
                        <div style="text-align: center;">
                            <input onchange="fridaystatus()" type="checkbox"  id="fridaystatus" """+ str("checked" if config_data['data'][4]['status'] == "true" else "")+""">
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <p>
                                FRIDAY
                            </p>
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <input type="time" onchange="fridaytime()" id="fridaytime" value='"""+ config_data['data'][4]['time']+"""'>
                        </div>
                    </td>
                </tr>

                <tr>
                    <td>
                        <div style="text-align: center;">
                            <input onchange="saturdaystatus()" type="checkbox"  id="saturdaystatus" """+ str("checked" if config_data['data'][5]['status'] == "true" else "")+""">
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <p>
                                SATURDAY
                            </p>
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <input type="time" onchange="saturdaytime()" id="saturdaytime" value='"""+ config_data['data'][5]['time']+"""'>
                        </div>
                    </td>
                </tr>

                <tr>
                    <td>
                        <div style="text-align: center;">
                            <input onchange="sundaystatus()" type="checkbox"  id="sundaystatus" """+ str("checked" if config_data['data'][6]['status'] == "true" else "")+""">
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <p>
                                SUNDAY
                            </p>
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <input type="time" onchange="sundaytime()" id="sundaytime" value='"""+ config_data['data'][6]['time']+"""'>
                        </div>
                    </td>
                </tr>

                <tr>
                    <td></td>
                    <td>
                        <div style="text-align: center;">
                            <button onclick="submit()">SUBMIT</button>
                        </div>
                    </td>
                    <td></td>
                </tr>
            </tbody>
        </table>

        


        <script type="text/javascript">
            var socket = new WebSocket("ws://"+window.location.host+"/websocket");
            var wsclosed = false;
            const retrytime = 3000;
            var lastretry = window.performance.now();

            // Listen for messages
            socket.addEventListener("message", (event) => {
                console.log("Message from server ", event.data);
            });


            function send_data(data){
                if (socket.readyState == 1){
                    socket.send(data);
                } else {
                    console.log("not ready!", socket.readyState);

                    if (window.performance.now()-lastretry > retrytime){
                        console.log("making new connection");
                        socket = new WebSocket("ws://"+window.location.host+"/websocket");
                        lastretry = window.performance.now();
                    }
                }
            }

            function mondaytime() {
                send_data(JSON.stringify({
                    'mondaytime': document.getElementById("mondaytime").value
                }));
                location.reload();
            }
            function tuesdaytime() {
                send_data(JSON.stringify({
                    'tuesdaytime': document.getElementById("tuesdaytime").value
                }));
                location.reload();
            }
            function wednesdaytime() {
                send_data(JSON.stringify({
                    'wednesdaytime': document.getElementById("wednesdaytime").value
                }));
                location.reload();
            }
            function thursdaytime() {
                send_data(JSON.stringify({
                    'thursdaytime': document.getElementById("thursdaytime").value
                }));
                location.reload();
            }

            function fridaytime() {
                send_data(JSON.stringify({
                    'fridaytime': document.getElementById("fridaytime").value
                }));
                location.reload();
            }

            function saturdaytime() {
                send_data(JSON.stringify({
                    'saturdaytime': document.getElementById("saturdaytime").value
                }));
                location.reload();
            }

            function sundaytime() {
                send_data(JSON.stringify({
                    'sundaytime': document.getElementById("sundaytime").value
                }));
                location.reload();
            }



            function mondaystatus() {
                send_data(JSON.stringify({
                    'mondaystatus': document.getElementById("mondaystatus").checked
                }));
                location.reload();
            }

            function tuesdaystatus() {
                send_data(JSON.stringify({
                    'tuesdaystatus': document.getElementById("tuesdaystatus").checked
                }));
                location.reload();
            }
            function wednesdaystatus() {
                send_data(JSON.stringify({
                    'wednesdaystatus': document.getElementById("wednesdaystatus").checked
                }));
                location.reload();
            }
            function thursdaystatus() {
                send_data(JSON.stringify({
                    'thursdaystatus': document.getElementById("thursdaystatus").checked
                }));
                location.reload();
            }
            function fridaystatus() {
                send_data(JSON.stringify({
                    'fridaystatus': document.getElementById("fridaystatus").checked
                }));
                location.reload();
            }
            function saturdaystatus() {
                send_data(JSON.stringify({
                    'saturdaystatus': document.getElementById("saturdaystatus").checked
                }));
                location.reload();
            }
            function sundaystatus() {
                send_data(JSON.stringify({
                    'sundaystatus': document.getElementById("sundaystatus").checked
                }));
                location.reload();
            }

            function submit() {
                send_data(JSON.stringify({
                    'SUBMIT': 'SUBMIT'
                }));
            }

        </script>

    </body>
</html>
    """




    return out

