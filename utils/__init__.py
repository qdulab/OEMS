from django.utils.timezone import get_current_timezone, make_naive

def get_naive_datetime(datetime):
    tzinfo = get_current_timezone()
    return make_naive(datetime, tzinfo)
