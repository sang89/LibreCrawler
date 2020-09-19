from datetime import datetime, timedelta

def convert_to_datetime_obj(date_time_str):
    try:
        result = datetime.strptime(date_time_str, '%m/%d/%Y')
        return result
    except:
        print('Cannot convert string to date: ', date_time_str)
        return ''