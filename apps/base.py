# -*- encoding: UTF-8 -*-

import yaml
import toolset.utils.util as util

logger = logging.getLogger('app_base')


class Task:
    def __init__(self, common_config, task_config):
        self.common_config = common_config
        self.task_config = task_config

    def process(self):
        raise("Not Implemented")

class Workflow:
    def __init__(self, tasks):
        self.tasks = tasks

    def run(self):
        for task in self.tasks:
            task.process()

class App:
    CONFIG_FILE = 'common.yaml'

    def __init__(self):
        self.common_config = self.load_config()
        self.tasks = set()
        self.workflows = set()
        self.init_local_cache()

    def init_local_cache(self):
        self.root = cache_settings['root']
        util.create_if_not_exist(local_path)

    def load_config(self):
        with open(self.CONFIG_FILE, 'r') as f:
            return yaml.load(f)

    def run_task(self, task_name):
        if task_name in self.tasks:
            self.tasks.get(task_name).process()
        else:
            logging.error('Task {} not found.'.format(task_name))

    def run_workflow(self, workflow_name):
        if workflow_name in self.workflows:
            self.workflows.get(workflow_name).run()
        else:
            logging.error('Workflow {} not found.'.format(workflow_name))


