from datetime import datetime, timedelta

def convert_to_datetime_obj(date_time_str):
    try:
        result = datetime.strptime(date_time_str, '%m/%d/%Y')
        return result
    except:
        print('Cannot convert string to date: ', date_time_str)
        return ''

def look_up_data(date, data_arr):
    # presumable param date is of format MM/DD/YYYY
    # need to get the form July 2020 and the date, e.g 20
    try:
        date_obj = convert_to_datetime_obj(date)
        month_year = date_obj.strftime('%B %Y')
        day = date_obj.strftime('%d')

        # Now loop through the data array

    except:
        return ''
