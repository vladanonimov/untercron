# coding: utf-8
from datetime import datetime

import freezegun

from untercron.scheduler import Scheduler, Task


class _FakeInterval(object):
    def __init__(self, next_time):
        self._next_time = next_time

    def get_next_time(self):
        return self._next_time


class _SmartFakeInterval(object):
    def __init__(self, next_time):
        self._next_time = next_time
        self._returned = False

    def get_next_time(self):
        if not self._returned:
            self._returned = True
            return self._next_time
        return None


class TestTask(object):
    def test_run_calls_runner(self):
        task = Task(runner=lambda: 1, interval=None, name='supername')

        assert task.name == 'supername'
        assert task.run() == 1


@freezegun.freeze_time('2001-01-01')
class TestScheduler(object):
    def test_add_task(self):
        task1 = Task(
            runner=None,
            interval=_FakeInterval(next_time=datetime(2020, 1, 1)),
            name='task1'
        )
        task2 = Task(
            runner=None,
            interval=_FakeInterval(next_time=None),
            name='task2'
        )
        scheduler = Scheduler()

        id1 = scheduler.add_task(task1)
        id2 = scheduler.add_task(task2)

        assert (id1, id2) == (0, 1)
        assert set(scheduler._tasks.keys()) == {0, 1}
        assert scheduler._tasks[0].name == 'task1'
        assert scheduler._tasks[1].name == 'task2'
        assert scheduler._heap == [
            (datetime(2001, 1, 1, 1, 0), 1, False),
            (datetime(2020, 1, 1), 0, True),
        ]

    def test_remove_task(self):
        task = Task(
            runner=None,
            interval=_FakeInterval(next_time=None),
        )
        scheduler = Scheduler()

        id1 = scheduler.add_task(task)
        assert len(scheduler._tasks) == 1

        scheduler.remove_task(id1)
        assert not scheduler._tasks

        scheduler.remove_task(-1)
        assert not scheduler._tasks

    def test_clear(self):
        task = Task(
            runner=None,
            interval=_FakeInterval(next_time=None),
        )
        scheduler = Scheduler()

        scheduler.add_task(task)
        assert len(scheduler._tasks) == 1
        assert len(scheduler._heap) == 1

        scheduler.clear()
        assert not scheduler._tasks
        assert not scheduler._heap

    def test_get_ready_to_run_tasks(self):
        task1 = Task(
            runner=None,
            interval=_SmartFakeInterval(next_time=datetime(1990, 1, 1)),
            name='task1'
        )
        task2 = Task(
            runner=None,
            interval=_FakeInterval(next_time=None),
            name='task2'
        )
        task3 = Task(
            runner=None,
            interval=_FakeInterval(next_time=datetime(1990, 1, 1)),
            name='task3'
        )
        scheduler = Scheduler()
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        id3 = scheduler.add_task(task3)
        scheduler.remove_task(id3)
        assert len(scheduler._heap) == 3

        ready_to_run_tasks = scheduler.get_ready_to_run_tasks()
        assert [task.name for task in ready_to_run_tasks] == ['task1']
        assert len(scheduler._heap) == 2
