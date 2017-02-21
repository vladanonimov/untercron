# coding: utf-8
from datetime import datetime

import freezegun
import pytest

from untercron.interval import Interval


class TestInterval(object):
    @pytest.mark.parametrize('kwargs', (
        {'months': (1, 20)},
        {'days': (1, 40)},
        {'hours': (1, 40)},
        {'minutes': (1, 70)},
        {'weekdays': (1, 70)},
    ))
    def test_invalid_values_raise_value_error(self, kwargs):
        with pytest.raises(ValueError):
            Interval(**kwargs)

    @freezegun.freeze_time('2001-01-01')  # это понедельник
    @pytest.mark.parametrize('kwargs, expected', (
        ({}, datetime(2001, 1, 1, 0, 1)),
        ({'minutes': (3,)}, datetime(2001, 1, 1, 0, 3)),
        ({'hours': (1,)}, datetime(2001, 1, 1, 1, 0)),
        ({'hours': (1,), 'minutes': (3,)}, datetime(2001, 1, 1, 1, 3)),
        ({'hours': (1,), 'weekdays': (1,)}, datetime(2001, 1, 1, 1, 0)),
        ({'hours': (1,), 'weekdays': (2,)}, None),
        ({'hours': (23,)}, None),
    ))
    def test_get_next_time_calculates_next_run_time(self, kwargs, expected):
        interval = Interval(**kwargs)
        assert interval.get_next_time() == expected
