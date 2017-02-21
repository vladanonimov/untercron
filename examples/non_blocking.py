# coding: utf-8
import time
from datetime import datetime

import untercron


def callback(result):
    print datetime.now().isoformat(), result


def main():
    # первые три минуты вызываем две функции
    # затем ещё три минуты вызываем только вторую функцию
    cron = untercron.UnterCron()
    task_id = cron.add_func_task(untercron.Interval(), lambda: 1, callback)
    cron.add_func_task(untercron.Interval(), lambda: 2, callback)

    cron.start(daemon_thread=False)
    time.sleep(3 * 60)

    cron.remove_task(task_id)
    time.sleep(3 * 60)

    cron.stop()


if __name__ == '__main__':
    main()
