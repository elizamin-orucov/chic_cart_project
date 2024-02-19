# calculating how long ago the notification was sent
from datetime import datetime


def calculate_time_difference_from_now(date_):
    # get the current time
    current_time = datetime.now()
    # calculate time difference
    time_difference = current_time - date_
    # calculation of days, hours, minutes and seconds
    days = time_difference.days
    hours = time_difference.seconds // 3600
    minutes = (time_difference.seconds // 60) % 60
    seconds = time_difference.seconds % 60
    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }


