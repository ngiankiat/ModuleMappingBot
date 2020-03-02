import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread


class ListingMods:
    """
    1. Connects to Google Spreadsheets to get the data
    2. Converts the data obtained to a list which we can easily handle
    """
    def __init__(self, scope, credentials, key, spreadsheet="modulemapping"):
        print("I'm at listing mods function!")
        self.scope = scope
        self.key = key
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('ferrous-cursor-266716-ffd1b5e0a2f2.json', scope)
        self.table = []  # resulting data is in a list

    def auth(self):
        gc = gspread.authorize(self.credentials)
        book = gc.open_by_key(self.key)
        worksheet = book.worksheet("modulemapping")
        table = worksheet.get_all_values()
        return table


class MappingLogic:
    """
    Parses the data nicely into lists for ianbot.py to handle the logic
    Since each new chat is handled in a different instance,
    and we do not want to make too many requests to GSheets,
    we store the data in the main file and let it handle the logic instead of going here.
    """

    def __init__(self):
        print("I'm at mapping logic function!")
        self.modstomap = []  # the mods the user wants to map

        lm = ListingMods(scope=['https://spreadsheets.google.com/feeds'],
                         key=os.environ['spreadsheet_key'],
                         credentials=None)
        self.df = lm.auth()

        self.schoollist = None
        self.sgmodslist = None
        self.overseasmodslist = None

    def run(self):
        """
        Useless method lol
        """
        self.schoollist = self.list_of_schools()
        self.overseasmodslist = self.list_of_overseas_mods()
        self.sgmodslist = self.list_of_sg_mods()

    def return_df(self):
        return self.df

    # Converting stuff to lists  (helper functions)

    def list_of_schools(self):  # overseas unis
        school = list(self.df[x][3] for x in range(len(self.df)))
        schools = list(x for x in school if x)
        return schools

    def list_of_overseas_mods(self):  # overseas mods
        mod = list(self.df[x][2] for x in range(len(self.df)))
        mods = list(x for x in mod if x)
        return mods

    def list_of_sg_mods(self):  # nus mods
        mod = list(self.df[x][1] for x in range(len(self.df)))
        mods = list(x for x in mod if x)
        return mods


# Some helper functions lol


def map(fn, seq):
    res = ()

    for ele in seq:
        res = res + (fn(ele),)
    return res


def filter(pred, seq):
    res = ()

    for ele in seq:
        if pred(ele):
            res = res + (ele,)
    return res