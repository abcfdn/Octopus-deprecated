# -*- encoding: UTF-8 -*-

import os
import argparse
import logging

import toolset.utils.util as util
from base import Resource
from constants import CONFIG_ROOT_PATH
from tasks.whitepaper_journal_poster import WhitepaperJournalPoster


FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('app')

TASKS = [
    WhitepaperJournalPoster
]


def add_task_arguments(task_parser):
    subparsers = task_parser.add_subparsers(
            title='task',
            dest='task',
            help='task to run')

    topic_poster_parser = subparsers.add_parser(
            'WhitepaperJournalPoster',
            help='run WhitepaperJournalPoster task')
    group = topic_poster_parser.add_mutually_exclusive_group()
    group.add_argument('--topics', help='create topic poster, comma separated')
    group.add_argument(
        '--session_name',
        help='create event poster based on session name prefix')
    group.add_argument(
        '--date', help='create event poster based on date, format 02/15/2019')


def add_flow_argument(flow_parser):
    subparsers = flow_parser.add_subparsers(
            title='flow',
            dest='flow',
            help='flow to run')
    # TODO: add workflow related args


def init_parser():
    parser = argparse.ArgumentParser(prog='wpj', add_help=False)
    subparsers = parser.add_subparsers(
            title='work_type',
            dest='work_type',
            help='type of work to do')

    task_parser = subparsers.add_parser('task', help='run a task')
    add_task_arguments(task_parser)

    flow_parser = subparsers.add_parser('flow', help='run a workflow')
    add_flow_argument(flow_parser)
    return parser



class App(Resource):
    def __init__(self, tasks):
        self.config = self.load_config()
        super().__init__(self.config['google'], self.config['data'])
        self._tasks = {task.__name__ : task for task in tasks}

    def load_config(self):
        common_config_file = os.path.join(CONFIG_ROOT_PATH, 'common.yaml')
        return util.load_yaml(common_config_file)

    def get_task(self, task_name):
        if task_name in self._tasks:
            return self._tasks[task_name](self.config)
        return None

    def run_task(self, task_name, args):
        task = self.get_task(task_name)
        if task:
            task.process(args)
        else:
            logging.error('Task {} not found.'.format(task_name))

    def run_flow(self, flow_name):
        if workflow_name in self.workflows:
            self.workflows.get(workflow_name).run()
        else:
            logging.error('Workflow {} not found.'.format(workflow_name))


def main():
    parser = init_parser()
    args = parser.parse_args()

    app = App(TASKS)
    if args.work_type == 'task':
        app.run_task(args.task, args)
    elif args.work_type == 'flow':
        app.run_flow(args.flow, args)


if __name__ == '__main__':
    main()
