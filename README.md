pysensu
=======

This is a simple python package to interact with [Sensu](https://github.com/sensu/sensu)

Installing
----------

    pip install pysensu

Example Usage
-------------
Pysensu uses the hostname and port where your sensu-api is running.

    from pysensu import pysensu

    client = pysensu.Pysensu("sensu.organization.com", 4567)

    # Stashes
    client.create_stash('server1')
    client.delete_stash('server2')
    client.get_all_stashes()

    # Clients
    client.get_client('server1')
    client.get_client_history('server1')
    client.delete_client('server2')
    client.get_all_clients()

    # Checks
    client.get_check('check_dns')
    client.get_all_checks()
    client.request_check('check_api_process', ['api-servers'])

    # Events
    client.get_all_events()
    client.get_all_client_events('server1')
    client.get_event('server1', 'check_dns')
    client.delete_event('server1', 'check_dns')
    client.resolve_event('server1', 'check_dns')
