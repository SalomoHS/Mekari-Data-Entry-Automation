from datetime import datetime

# Get today date
def today() -> str:
    today = datetime.now()\
                .strftime("%Y-%m-%d")
    return today