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
