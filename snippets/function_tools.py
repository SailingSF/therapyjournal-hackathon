# functions to supply AI assistants with function tool outputs
from datetime import datetime
import pytz


# current time function

def current_time(timezone):
    # returns current time in a timezone in human readable format
    form = "%A %B %d, %Y at %H:%M Local Time (%Z)"
    
    tz = pytz.timezone(timezone)
    try:
        time_string = datetime.now(tz).strftime(form)
    except:
        time_string = datetime.now().strftime(form)
    
    return time_string