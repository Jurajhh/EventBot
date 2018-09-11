# -*- coding: UTF-8 -*-

from fbchat import log, Client, ThreadType, models
from apscheduler.schedulers.background import BackgroundScheduler
import datetime as dt
from datetime import datetime
import time
from multiprocessing import Process


class EventBot(Client):
    # Subclasses fbchat.Client and override required methods
    def __init__(self, email, password):
        Client.__init__(self, email, password)
        self.sched = BackgroundScheduler()
        self.sched.start()

    THREAD_ID_EVENTBOT_TO_JURAJ = "100000489471600"
    THREAD_ID_EVENTBOT_TO_SAMUEL = "xx" # add contact to Samuel
    COMPANY_NAME = "the event"
    address_list = set()
    address_list.add(THREAD_ID_EVENTBOT_TO_JURAJ)
    #    address_list.add(THREAD_ID_ECHOBOT_TO_JURAJ)
    listening_list = set()
    listening_list.add(THREAD_ID_EVENTBOT_TO_JURAJ)

    #    listening_list.add(THREAD_ID_ECHOBOT_TO_JURAJ)

    def message_somebody(self, text=None, thread_id=THREAD_ID_EVENTBOT_TO_JURAJ):
        """
        send message
        :param text: 'str' text of your message
        :param thread_id: 'str' the person
        you are sending the message to
        :return:
        """
        message_object = models.Message(text=text)
        self.send(message_object, thread_id=thread_id,
                  thread_type=ThreadType.USER)

    def send_to_listeners(self, text=None):
        """
        Send message to all the listeners listed in
        address_list.

        :param str text: the text of the message
        """
        message_object = models.Message(text=text)
        for id in self.listening_list:
            self.send(message_object, thread_id=id,
                      thread_type=ThreadType.USER)


    def intro_message(self, thread_id=THREAD_ID_EVENTBOT_TO_JURAJ):
        """
        send the intro message
        :param thread_id: 'str' the ID of the addressee
        :return:
        """
        self.message_somebody(text="INTRO MESSAGE!", thread_id=thread_id)

    """
    def one_guy(self, thread_id=None):
        for i in ["un", "dos", "tres"]:
            time.sleep(3)
            self.message_somebody(text=i,
                                  thread_id=thread_id)
    """

    def onFriendRequest(self, from_id, msg):
        # log.info("{} from {} in {}".format(from_id, msg))
        print("Friend request")
        self.friendConnect(from_id)

    def log_off(self, author_id=None):
        self.listening_list.remove(author_id)
        self.message_somebody(
            text="If you would like to "
                 "receive notifications again,"
                 " send 'LOGON!'.",
            thread_id=author_id)

    def log_on(self, author_id=None):
        self.listening_list.add(author_id)
        self.message_somebody(
            text="You have subscribed to messages from the"
                 " Event Bot, so you will be receiving all "
                 "the interesting information about "
                + self.COMPANY_NAME +
                 " from the EventBot.",
            thread_id=author_id)
        self.message_somebody(
            text="If you do not want to receive the messages,"
                 " send 'LOGOFF!'.",
            thread_id=author_id)
        # chceme paralelny program, ktory po 3 minutach zavola:
        print("zacal scheduler")
        self.sched.add_job(func=self.log_off,
                           trigger="interval",
                           seconds=10,
                           end_date=datetime.now() + dt.timedelta(seconds=15),
                           args=[author_id])
        print("dostal sa na druhu stranu")

    def onMessage(self, author_id, message_object,
                  thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        log.info("{} from {} in {}".format(
            message_object, thread_id, thread_type.name))

        # If you're not the author, echo
        if author_id != self.uid:
            is_in = False
            for id in self.address_list:
                if id == author_id:
                    is_in = True
                    break  # break to stop the loop if the id was found
            if not is_in:
                self.address_list.add(author_id)
                self.listening_list.add(author_id)
                self.message_somebody(
                    text="Hello, this is Event Bot :-)",
                    thread_id=author_id)
                self.message_somebody(
                    text="Watch out for the video introducing the EventBot: "
                         "https://www.youtube.com/",
                         # add the green guy dancing
                    thread_id=author_id)
                self.intro_message(thread_id=author_id)
                self.log_on(author_id=author_id)

            """
            # allows those who have contacted the Bot to log off 
            # - needs improvement (pop up a question assuring that
            #   this is really what they want to do) 
            else:
                if message_object.text == "LOGON!":
                    self.log_on(author_id=author_id)
                if message_object.text == "LOGOFF!":
                    self.log_off(author_id=author_id)
            """
