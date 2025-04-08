import json

def test():
    return 3
    


def export_config_file(CONFIG_FILE, tasks:list):
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
                        <div style="text-align: center;">
                            <p id="slider1value">90</p>
                            <input onchange="slider1()" type="range" min="0" max="180" value="90" id="slider1">
                        </div>
                    </td>
                    <td>
                        <h3>ESP Web Server</h3>
                        <div style="text-align: center;">
                            <p>
                                <button onclick="offfunc()" class="">OFF</button>
                                <button onclick="onfunc()" class="">ON</button>
                            </p>
                        </div>
                    </td>
                    <td>
                        <div style="text-align: center;">
                            <p id="slider2value">90</p>
                            <input onchange="slider2()" type="range" min="0" max="180" value="90" id="slider2">
                        </div>
                    </td>
                </tr>

                <tr>
                    <td>
                        <div style="background-color: grey; border-radius: 50px;">
                            <div id="joy1Div" style="margin: auto; width:300px;height:300px;"></div>
                        </div>
                    </td>
                    <td></td>
                    <td>
                        <div style="background-color: grey; border-radius: 50px;">
                            <div id="joy2Div" style="margin: auto; width:300px;height:300px;"></div>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>


        <script src="joy.js"></script>

        <script type="text/javascript">
            alert(window.location.host);
            var socket = new WebSocket("ws://"+window.location.host+"/data");
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
                        socket = new WebSocket("ws://"+window.location.host+"/data");
                        lastretry = window.performance.now();
                    }
                }
            }


            var lastsend = window.performance.now()
            // Create JoyStick object into the DIV 'joyDiv'
            var Joy1 = new JoyStick('joy1Div', {}, async function(stickData) {
                if (window.performance.now() > lastsend + 50 || (stickData.x == 0 && stickData.y == 0)){
                    send_data(JSON.stringify({
                        'joy1x': stickData.x,
                        'joy1y': stickData.y
                    }));
                    lastsend = window.performance.now();
                }
            });
            var Joy2 = new JoyStick('joy2Div', {}, async function(stickData) {
                if (window.performance.now() > lastsend + 50 || (stickData.x == 0 && stickData.y == 0)){
                    send_data(JSON.stringify({
                        'joy2x': stickData.x,
                        'joy2y': stickData.y
                    }));
                    lastsend = window.performance.now();
                }
            });

            function slider1() {
                var x = document.getElementById("slider1").value;
                document.getElementById("slider1value").innerHTML = x;

                send_data(JSON.stringify({
                    'slider1': x
                }));
            }

            function slider2() {
                var x = document.getElementById("slider2").value;
                document.getElementById("slider2value").innerHTML = x;

                send_data(JSON.stringify({
                    'slider2': x
                }));
            }


            function offfunc() {
                send_data(JSON.stringify({
                    'off': '_'
                }));
            }
            function onfunc() {
                send_data(JSON.stringify({
                    'on': '_'
                }));
            }
        </script>

    </body>
</html>
    """




    return out

