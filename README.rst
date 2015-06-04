=====================
gpsdio sorting plugin
=====================


.. image:: https://travis-ci.org/SkyTruth/gpsdio-filtersplit.svg?branch=master
    :target: https://travis-ci.org/SkyTruth/gpsdio-filtersplit


.. image:: https://coveralls.io/repos/SkyTruth/gpsdio-filtersplit/badge.svg?branch=master
    :target: https://coveralls.io/r/SkyTruth/gpsdio-filtersplit


A CLI plugin for `gpsdio <https://github.com/skytruth/gpdsio/>`_ that sorts messages in arbitrarily large files according to an arbitrary set of columns.


Examples
--------

See ``gpsdio sort --help`` for info.

.. code-block:: console

    $ gpsdio sort input.msg output.msg \
        -c mmsi,timestamp


Installing
----------

Via pip:

.. code-block:: console

    $ pip install gpsdio-filtersplit

From master:

.. code-block:: console

    $ git clone https://github.com/SkyTruth/gpsdio-filtersplit
    $ cd gpsdio-filtersplit
    $ pip install .


Developing
----------

.. code-block::

    $ git clone https://github.com/SkyTruth/gpsdio-filtersplit
    $ cd gpsdio-filtersplit
    $ virtualenv venv && source venv/bin/activate
    $ pip install -e .[test]
    $ py.test tests --cov gpsdio_filtersplit --cov-report term-missing
