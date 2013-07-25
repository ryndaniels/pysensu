pysensu
=======

This is a simple python package to interact with [Sensu](https://github.com/sensu/sensu)

Installing
----------

    python setup.py install

Example Usage
-------------
Pysensu uses the hostname and port where your sensu-api is running.

    from pysensu import pysensu

    client = pysensu.Pysensu("sensu.organization.com", 4567)
    client.create_stash('server1')
    client.delete_stash('server2')
    client.delete_client('server2')
