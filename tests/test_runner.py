# coding: utf-8
from untercron.runner import run_func, run_subprocess


class TestRunFunc(object):
    def test_success(self):
        results = []
        thread = run_func(lambda: 1, lambda result: results.append(result))
        thread.join()

        assert len(results) == 1
        assert results[0].is_success
        assert results[0].return_value == 1
        assert results[0].exc_info is None

    def test_exception(self):
        results = []
        thread = run_func(lambda: 1/0, lambda result: results.append(result))
        thread.join()

        assert len(results) == 1
        assert not results[0].is_success
        assert results[0].return_value is None
        assert len(results[0].exc_info) == 3


class TestRunSubprocess(object):
    def test_success(self):
        results = []
        thread = run_subprocess(
            ['echo', 'aa'],
            {},
            lambda result: results.append(result)
        )
        thread.join()

        assert len(results) == 1
        assert results[0].is_success
        assert results[0].return_code == 0
        assert results[0].stdout == 'aa\n'
        assert results[0].stderr == ''
        assert results[0].exc_info is None

    def test_exception(self):
        results = []
        thread = run_subprocess(
            ['weirdnonexistentapp'],
            {},
            lambda result: results.append(result)
        )
        thread.join()

        assert len(results) == 1
        assert not results[0].is_success
        assert results[0].return_code is None
        assert results[0].stdout is None
        assert results[0].stderr is None
        assert len(results[0].exc_info) == 3
