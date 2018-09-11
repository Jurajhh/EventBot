# EventBot
**Facebook Messenger bot** to enhance the flow of your event.

*EventBotInAction.py* allows you to setup the behaviour of your bot.

After having created a profile of your bot on facebook,
just enter the login details, i.e. email and password into the file *EventBotInAction.py*:

    try:
        client = EventBot("email", "password") # add email and password
                                               # of your fb Messenger bot
