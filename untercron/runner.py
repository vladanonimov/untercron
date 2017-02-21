# coding: utf-8
import subprocess
import sys
import threading

from collections import namedtuple
from functools import wraps


__all__ = ('run_func', 'run_subprocess')


FuncResult = namedtuple('FuncResult', (
    'is_success',
    'return_value',
    'exc_info',
))
SubprocessResult = namedtuple('SubprocessResult', (
    'is_success',
    'return_code',
    'stdout',
    'stderr',
    'exc_info',
))


def _run_in_thread(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread

    return wrapper


@_run_in_thread
def run_func(func, callback):
    try:
        return_value = func()
    except Exception:
        exc_info = sys.exc_info()
        result = FuncResult(
            is_success=False,
            return_value=None,
            exc_info=exc_info,
        )
    else:
        result = FuncResult(
            is_success=True,
            return_value=return_value,
            exc_info=None,
        )
    if callable(callback):
        callback(result)


@_run_in_thread
def run_subprocess(args, popen_kwargs, callback):
    popen_kwargs.setdefault('stdout', subprocess.PIPE)
    popen_kwargs.setdefault('stderr', subprocess.PIPE)
    process = None
    try:
        process = subprocess.Popen(args, **popen_kwargs)
        stdout, stderr = process.communicate()
    except Exception:
        exc_info = sys.exc_info()
        result = SubprocessResult(
            is_success=False,
            return_code=process.returncode if process is not None else None,
            stdout=None,
            stderr=None,
            exc_info=exc_info,
        )
    else:
        result = SubprocessResult(
            is_success=True,
            return_code=process.returncode,
            stdout=stdout,
            stderr=stderr,
            exc_info=None,
        )
    if callable(callback):
        callback(result)
