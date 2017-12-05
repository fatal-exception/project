DOIT_CONFIG = {'default_tasks': ['usage']}

def task_pysetup():
    return {
        'actions': ['python3 -m venv hansum.3venv',
            'source ./hansum.3venv/bin/activate && pip install -r requirements.txt',
            'echo type \\"source ./hansum.3venv/bin/activate\\" to use virtualenv'],
        'verbosity': 2
        }

def task_usage():
    return {
            'actions': ['echo type \\"doit list\\" to see tasks or \\"doit help\\" for help'],
            'verbosity': 2
            }
