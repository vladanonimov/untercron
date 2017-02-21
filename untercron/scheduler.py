# coding: utf-8
import heapq
import itertools
from datetime import datetime, timedelta


__all__ = ('Scheduler', 'Task')


class Task(object):
    def __init__(self, runner, interval, name=None):
        self.runner = runner
        self.interval = interval
        self.name = name

    def run(self):
        return self.runner()


class Scheduler(object):
    def __init__(self, check_delta=timedelta(hours=1)):
        self._tasks = {}
        self._heap = []
        self._id_generator = itertools.count()
        self._check_delta = check_delta

    def get_ready_to_run_tasks(self):
        tasks = []
        while self._heap and self._heap[0][0] <= datetime.now():
            _, task_id, ready_to_run = heapq.heappop(self._heap)
            task = self._tasks.get(task_id)
            if task is None:
                continue
            if ready_to_run:
                tasks.append(task)

            self._push_task(task, task_id)
        return tasks

    def add_task(self, task):
        task_id = self._id_generator.next()
        self._tasks[task_id] = task
        self._push_task(task, task_id)
        return task_id

    def remove_task(self, task_id):
        self._tasks.pop(task_id, None)

    def clear(self):
        self._tasks = {}
        self._heap = []

    def _push_task(self, task, task_id):
        next_time = task.interval.get_next_time()
        if next_time is not None:
            next_ready_to_run = True
        else:
            next_time = datetime.now() + self._check_delta
            next_ready_to_run = False
        heapq.heappush(self._heap, (next_time, task_id, next_ready_to_run))
