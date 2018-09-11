# This script is an example of use of EventBot class
# and its functions

# -*- coding: UTF-8 -*-

from EventBotClass import EventBot


def run():
    try:
        client = EventBot("email", "password") # add email and password
                                               # of your fb Messenger bot
        client.listen()
    finally:
        client.sched.shutdown()
        print("client.sched.shutdown() zbehol")


if __name__ == "__main__":
    run()