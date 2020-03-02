import os

print("Hello we're starting now")

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from mapping import MappingLogic
from scoring import Scorer
from inspector import Inspect


class IanBot:
    """
    This Module functions as a Manager to combine all the other Python files
    """
    """
    1. Connects to telegram
    2. Runs Python script which handles the logic
    3. Runs Telegram handlers alongside with Python logic i.e. checking if modules exist in the data
    4.
    """

    def __init__(self, token, name):
        print("I'm at main function!")
        self.token = token
        self.name = name

        self.module_list = {}
        self.regions = {}

        # We need to store data in this module so that we don't have to call the google API again
        self.df = None
        self.schoollist = None
        self.overseasmodslist = None
        self.sgmodslist = None

        self.topx = 10  # going to hard core for now!!!
        # self.topx_unis = None  # for this version, this is a string but todo: parse string into buttons

        self.inspect_uni = None

        # Scoring-related tasks
        self.schoolscore = {}

    def run(self):
        # initialise lists
        ml = MappingLogic()
        self.df = ml.return_df()
        self.schoollist = ml.list_of_schools()
        self.overseasmodslist = ml.list_of_overseas_mods()
        self.sgmodslist = ml.list_of_sg_mods()

        updater = Updater(self.token, use_context=True)

        # dispatcher to register handlers
        dp = updater.dispatcher

        # add command functionality
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CommandHandler('add', self.add))  # add new modules
        dp.add_handler(CommandHandler('view', self.view))
        dp.add_handler(CommandHandler('done', self.done))  # once user is done, return top x unis
        dp.add_handler(CommandHandler('inspect', self.inspect))
        dp.add_handler(CommandHandler('stop', self.stop))

        # start the bot
        updater.start_polling()
        print("I have started polling!")
        updater.idle()
        print("I have started idling!")

    def start(self, update, context):
        user = update.message.from_user
        chatid = update.message.chat.id

        log_text = "User " + str(user.id) + " has started using bot."
        print(log_text)  # To keep track of log

        self.module_list['user_id'] = []
        print(self.module_list['user_id'])

        self.regions['user_id'] = []
        print(self.regions['user_id'])

        reply_text = "Hello! Welcome to the Biz Exchange Module Mapping Bot! Send /add Module Code in this format to start!"
        reply_text += "\n\nExample: /add ACC1002"
        reply_text += "\n\nYou can view the current module selection with /view"
        reply_text += "\n\nOnce you are done, type /done and we will return you your top 10 exchange universities."
        reply_text += "\n\nTo exit, type /stop"
        reply_text += "\n\nThis bot is created by Nelson. Feel free to contact me at @Exopulse on Telegram."

        context.bot.send_message(text=reply_text,
                                 chat_id=chatid,
                                 parse_mode=ParseMode.HTML)

    def add(self, update, context):
        user = update.message.from_user
        chatid = update.message.chat.id

        log_text = "User " + str(user.id) + " has added a new module"
        print(log_text)  # To keep track of log

        new_module_text = ' '.join(context.args)
        new_module_text = new_module_text.upper()

        # handling spaces
        if new_module_text == ' ':
            reply_text = "Please type a valid module code."
            context.bot.send_message(text=reply_text,
                                     chat_id=chatid,
                                     parse_mode=ParseMode.HTML)

        # check if module is currently in selection
        if new_module_text in self.module_list['user_id'] and new_mdoule_text != ' ':
            reply_text = "Sorry. You have already added {} to the module list".format(new_module_text)
            context.bot.send_message(text=reply_text,
                                     chat_id=chatid,
                                     parse_mode=ParseMode.HTML)

        # check if the module actually exists
        if self.check_mod(new_module_text) and new_module_text not in self.module_list['user_id'] and new_module_text != ' ':
            self.module_list['user_id'].append(new_module_text)

            reply_text = "Okay you have added " + new_module_text + " as Module " + str(len(self.module_list['user_id']))
            reply_text += "\n\nAdd another module? Send in the format of /add Module Code:"
            reply_text += "\n\nExample: /add MKT1003"
            reply_text += "\n\nOnce you are done, type /done"
            reply_text += "\n\nTo exit, type /stop"

            context.bot.send_message(text=reply_text,
                                     chat_id=chatid,
                                     parse_mode=ParseMode.HTML)
        else:
            reply_text = "Sorry, but " + new_module_text + " does not exist in our system. Please try again"
            reply_text += "\n\nSend in the format of /add Module Code:"
            reply_text += "\n\nExample: /add MKT1003"
            reply_text += "\n\nOnce you are done, type /done"
            reply_text += "\n\nTo exit, type /stop"

            context.bot.send_message(text=reply_text,
                                     chat_id=chatid,
                                     parse_mode=ParseMode.HTML)

    def view(self, update, context):
        user = update.message.from_user
        chatid = update.message.chat.id

        log_text = "User " + str(user.id) + " is going to view the current module selection"
        print(log_text)  # To keep track of log

        reply_text = "## You have selected {} modules ##".format(len(self.module_list['user_id']))
        
        for idx, module in enumerate(self.module_list['user_id']):
            reply_text += "\n\n" + str(idx+1) + ". " + module
        
        context.bot.send_message(text=reply_text,
                                 chat_id=chatid,
                                 parse_mode=ParseMode.HTML)

    def filter_country(self, update, context):
        """
        Allow the user to filter by country
        """
        
        pass

    def done(self, update, context):
        """
        Handler which asks the user to input their top x universities to select from
        """

        def check_positive_int(inp):
            if type(inp) == int:
                if inp > 0:
                    return True
            return False

        user = update.message.from_user
        chatid = update.message.chat.id

        user_input = ' '.join(context.args)

        log_text = "User " + str(user.id) + " has entered the top x universities section."
        print(log_text)  # To keep track of log

        # reply_text = "How many schools do you want to see? (enter a positive-integer number): "
        # context.bot.send_message(text=reply_text,
        #                         chat_id=chatid,
        #                         parse_mode=ParseMode.HTML)

        user_input = 10
        if user_input:  # await user reply... going to hardcode for now
            if check_positive_int(user_input):
                pass
            else:
                reply_text = "Sorry, but you need to enter a positive integer to continue"
                context.bot.send_message(text=reply_text,
                                         chat_id=chatid,
                                         parse_mode=ParseMode.HTML)

        result = self.run_logic()  # should be a list

        reply_text = "## Top " + str(10) + " Candidate Schools ## "
        for score in result:
            reply_text += "\n\n%s: %d" % (score[0], score[1])
        reply_text += "\n\n###################"
        reply_text += "\n\nPlease chose a university to you're interested in to check the modules you can take."
        reply_text += "\n\nType /inspect University Code"
        reply_text += "\n\nExample: /inspect UCLA"
        reply_text += "\n\nIf the university doesn't have a shortform you probably have to type in the full name"
        reply_text += "\n\nPress /stop when you are done."

        context.bot.send_message(text=reply_text,
                                 chat_id=chatid,
                                 parse_mode=ParseMode.HTML)

    def topx_unis(self, update, context):
        """
        Message Handler which parses the number that the user gives and returns the unis
        I'm also not sure how this works... need to check out ConversationHandler
        """
        pass

    def run_logic(self):
        """
        scoring.py
        Returns a list of exchange unis from most matched to least matched!
        """
        sc = Scorer(
            df=self.df,
            module_list=self.module_list['user_id'],
            sgmods=self.sgmodslist,
            schoollist=self.schoollist,
            topx=self.topx
        )
        result = sc.run()
        return result

    def inspect(self, update, context):
        """
        Now we'll just let the user type in the university code. (Todo: create buttons for user to select)
        """
        user = update.message.from_user
        chatid = update.message.chat.id

        log_text = "User " + str(user.id) + " is going to inspect the selected universities"
        print(log_text)  # To keep track of log

        self.inspect_uni = ' '.join(context.args)

        # inspect logic here from inspect.py
        # returns the required information to the user

        insp = Inspect(
            df=self.df,
            uni=self.inspect_uni,  # user input gets passed to the Inspect logic
            module_list=self.module_list['user_id']
        )

        reply_text = insp.run()

        context.bot.send_message(text=reply_text,
                                 chat_id=chatid,
                                 parse_mode=ParseMode.HTML)

    def stop(self, update, context):
        user = update.message.from_user
        chatid = update.message.chat.id

        log_text = "User " + str(user.id) + " has pressed done which will end the conversation"
        print(log_text)  # To keep track of log

        self.module_list['user_id'] = []  # reset module_list for the user

        reply_text = "Thanks for using the Biz Exchange Module Mapping Bot (BEMbot)!"

        context.bot.send_message(text=reply_text,
                                 chat_id=chatid,
                                 parse_mode=ParseMode.HTML)

    # Helper functions
    def check_mod(self, mod):
        """
        Check mod availability for mapping in NUS
        """
        inside = False
        for x in range(len(self.sgmodslist)):
            if mod not in self.sgmodslist[x]:
                continue
            elif mod in self.sgmodslist[x]:
                inside = True
                break
        return inside

def main():
    tele = IanBot(
        token=os.environ['TELEGRAM_TOKEN'],
        name="ian-bot")
    tele.run()


if __name__ == '__main__':
    main()
