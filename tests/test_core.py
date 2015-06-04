"""
Unittests for `gpsdio_filtersplit.core`.
"""


import tempfile

from click.testing import CliRunner
import gpsdio.cli
import os.path
import datetime
import random
import contextlib
import glob

def randdate():
    return datetime.datetime(
        2014, 1+int(12*random.random()),
        1+int(28*random.random()),
        int(24*random.random()),
        int(60*random.random()),
        int(60*random.random())
        )


@contextlib.contextmanager
def unittestfiles():
    try:
        with gpsdio.open('unittest.in.msg', "w") as f:
            f.writerows([
                    {"mmsi": "123", "name": "Rainbow warrior", "speed": 1.0},
                    {"name": "France", "speed": 1.1},
                    {"mmsi": "456", "name": "Rainbow warrior II", "speed": 2.0}
                    ])
        yield
    finally:
        # pass
        if os.path.exists('unittest.in.msg'):
            os.unlink('unittest.in.msg')
        for name in glob.glob("unittest.out.*"):
            os.unlink(name)

    
def test_split():
    with unittestfiles():
        CliRunner().invoke(gpsdio.cli.main.main_group, [
                'filtersplit',
                'unittest.in.msg',
                'unittest.out.%(split)s.msg'
                ])
        files = glob.glob('unittest.out.*')
        files.sort()
        assert files == ['unittest.out.mmsi=123.msg', 'unittest.out.mmsi=456.msg']
        with gpsdio.open('unittest.out.mmsi=123.msg') as f:
            assert [row['name'] for row in f] == ["Rainbow warrior", "France"]

def test_bucketsplit():
    with unittestfiles():
        CliRunner().invoke(gpsdio.cli.main.main_group, [
                'filtersplit',
                "--buckets=2",
                'unittest.in.msg',
                'unittest.out.%(split)s.msg'])
        files = glob.glob('unittest.out.*')
        files.sort()
        assert files == ['unittest.out.bucket=0.msg', 'unittest.out.bucket=1.msg', 'unittest.out.bucketlist.msg']
        with gpsdio.open('unittest.out.bucket=1.msg') as f:
            assert [row['name'] for row in f] == ["Rainbow warrior", "France"]

def test_filter():
    with unittestfiles():
        res = CliRunner().invoke(gpsdio.cli.main.main_group, [
                'filtersplit',
                "--split=",
                "--filter=speed < 1.9",
                'unittest.in.msg',
                'unittest.out.msg'])
        files = glob.glob('unittest.out.*')
        files.sort()
        assert files == ['unittest.out.msg']
        with gpsdio.open('unittest.out.msg') as f:
            assert [row['name'] for row in f] == ["Rainbow warrior", "France"]
