import json



def log(message):
    print(message)

def create_config_mono_auto_tasks_json(file_path:str, tasks:list):
    cnt = 0
    export_data = dict()
    export_data['name'] = "auto-work"
    export_data['data'] = list()
    for task in tasks:
        task['id'] = cnt
        cnt += 1
        assert len(task.keys()) == 8
        export_data['data'].append(task)

    export_data['cnt'] = cnt


    with open(file_path, 'w') as f:
        json.dump(export_data, f)
    




