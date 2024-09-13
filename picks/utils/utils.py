from datetime import datetime


NFL_WEEK_END_DATES_2024 = {
    1: '2024-09-09',
    2: '2024-09-16',
    3: '2024-09-23',
    4: '2024-09-30',
    5: '2024-10-07',
    6: '2024-10-14',
    7: '2024-10-21',
    8: '2024-10-28',
    9: '2024-11-04',
    10: '2024-11-11',
    11: '2024-11-18',
    12: '2024-11-25',
    13: '2024-12-02',
    14: '2024-12-09',
    15: '2024-12-16',
    16: '2024-12-23',
    17: '2024-12-30',
    18: '2025-01-05',
}


def get_current_week():
    '''
    Returns the current week of the 2024 NFL season.
    '''

    # Get the current date
    today = datetime.now()

    # Figure out what week it is based on the end dates of each week
    # The current week should be the first week where the current date is less than the end date
    for week, end_date in NFL_WEEK_END_DATES_2024.items():
        if today < datetime.strptime(end_date, '%Y-%m-%d'):
            return week
