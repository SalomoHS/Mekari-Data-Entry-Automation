import get_date

# Mekari Account ------------------------------------

EMAIL = ''
PASS = ''

# Card Information ------------------------------------

card_name:str = "USD"
card_purpose:str = ""
card_holder_name:str = "Teta"
account:str = "Teta Project"

# Automation Configuration ------------------------------------

delay:int = 5 # Delay before the next input (seconds)
today_date:str = get_date.today() # Get today date ex. 2025-04-01
valid_thru:str = "2027-04-01" # 2027-04-01
limit:int = 50 # Input automation limit

# URL ------------------------------------

LOGIN_URL = "https://account.mekari.com"
DASHBOARD_URL = "https://expense.mekari.com/"
CARD_URL = "https://expense.mekari.com/card"

# Autentication Session ------------------------------------

AUTH = "auth.json"



