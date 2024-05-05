from datetime import datetime, timedelta


today = datetime.now().date()
first_day_current_month = today.replace(day=1)

first_day_previous_month = first_day_current_month - timedelta(
    days=first_day_current_month.day
)

last_day_previous_month = first_day_current_month - timedelta(days=1)
