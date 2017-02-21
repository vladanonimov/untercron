# coding: utf-8
from datetime import datetime

import untercron


def callback(result):
    print datetime.now().isoformat(), result


def main():
    # каждую минуту вызываем функцию
    # каждую чётную минуту вызываем ls
    cron = untercron.UnterCron()
    cron.add_func_task(untercron.Interval(), lambda: 1, callback)
    cron.add_subprocess_task(
        untercron.Interval(minutes=range(0, 60, 2)),
        ['ls'],
        callback,
    )

    try:
        cron.start(blocking=True)
    finally:
        cron.stop()


if __name__ == '__main__':
    main()
