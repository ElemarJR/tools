from datetime import timedelta, datetime


class Weeks:

    @staticmethod
    def get_week_dates(reference_date):
        if reference_date.weekday() == 6:
            start_of_week = reference_date
        else:
            start_of_week = reference_date - timedelta(days=reference_date.weekday() + 1)
        end_of_week = start_of_week + timedelta(days=6)
        return start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')

    @staticmethod
    def get_current():
        today = datetime.now()
        return Weeks.get_week_dates(today)

    @staticmethod
    def get_previous(n=1):
        today = datetime.now()
        last_week_date = today - timedelta(days=7 * n)
        return Weeks.get_week_dates(last_week_date)

    @staticmethod
    def get_week_string_from_date(reference_date):
        start, end = Weeks.get_week_dates(reference_date)
        return Weeks.get_week_string_from_interval(start, end)

    @staticmethod
    def get_week_string_from_interval(start, end):
        star_f = datetime.fromisoformat(start).strftime('%d/%m')
        end_f = datetime.fromisoformat(end).strftime('%d/%m')
        return f'{star_f} - {end_f}'
