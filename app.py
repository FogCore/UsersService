#!/usr/bin/env python3

from UsersService import server

if __name__ == '__main__':
    server.start()
    server.wait_for_termination()
