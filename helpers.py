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