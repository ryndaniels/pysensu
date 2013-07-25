#!/usr/bin/env python


class Pysensu():
    def __init__(self, host, user=None, password=None, port=4567):
        if not host:
            raise ValueError("Cannot create Pysensu object without host")

        self.host = host
        self.user = user
        self.password = password
        self.port = port

        if self.user and self.port:
            self.api_url = "https://{}:{}@{}:{}".format(user, password, host, port)
        elif not self.user and not self.port:
            self.api_url = "http://{}:{}".format(host, port)
        else:
            raise ValueError("Must specify both user and password")
