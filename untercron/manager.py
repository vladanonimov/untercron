# coding: utf-8
import threading
import time
from functools import partial

from untercron.runner import run_func, run_subprocess
from untercron.scheduler import Scheduler, Task

__all__ = ('UnterCron',)


class UnterCron(object):

    def __init__(self, sleep_interval=1):
        self._sleep_interval = sleep_interval

        self._scheduler = Scheduler()
        self._running = False
        self._thread = None

    def start(self, blocking=False, daemon_thread=True):
        if self._running:
            raise RuntimeError('Already started')

        self._running = True
        if blocking:
            self._worker()
        else:
            self._thread = threading.Thread(target=self._worker)
            self._thread.daemon = daemon_thread
            self._thread.start()

    def stop(self):
        self._running = False
        self._scheduler.clear()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join()
        self._thread = None

    def add_func_task(self, interval, func, callback=None, name=None):
        runner = partial(run_func, func, callback)
        return self._add_task(interval, runner, name)

    def add_subprocess_task(self, interval, args, callback=None,
                            popen_kwargs=None, name=None):
        runner = partial(run_subprocess, args, popen_kwargs or {}, callback)
        return self._add_task(interval, runner, name)

    def remove_task(self, task_id):
        self._scheduler.remove_task(task_id)

    def _add_task(self, interval, runner, name):
        task = Task(
            runner=runner,
            interval=interval,
            name=name
        )
        return self._scheduler.add_task(task)

    def _worker(self):
        while self._running:
            for task in self._scheduler.get_ready_to_run_tasks():
                task.run()
            time.sleep(self._sleep_interval)
