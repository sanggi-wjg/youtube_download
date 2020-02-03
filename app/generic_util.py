from datetime import datetime


def ret_date_format(timeFormat: str = '%Y%m%d%H%M%S'):
    return str(datetime.today().strftime(timeFormat))
