import calendar
from datetime import date, timedelta

from apps.habits.models import Calendar


def generate_calendar_data(request):
    """Генерирует данные календаря для пользователя"""

    def is_date_in_streak(check_date):
        """Проверяет, входит ли дата в период стрика"""
        return user_cal.first_date <= check_date <= user_cal.last_date

    # Имена месяцев
    month_names = {
        1: "Январь",
        2: "Февраль",
        3: "Март",
        4: "Апрель",
        5: "Май",
        6: "Июнь",
        7: "Июль",
        8: "Август",
        9: "Сентябрь",
        10: "Октябрь",
        11: "Ноябрь",
        12: "Декабрь",
    }

    if not request.user.is_authenticated:
        return None
    today = date.today()
    current_month = today.month
    current_year = today.year

    # Создаём календарь, если пользователь впервые заходит в приложение
    if not Calendar.objects.filter(user=request.user).exists():
        Calendar.objects.create(user=request.user, first_date=today, last_date=today)
    user_cal = Calendar.objects.get(user=request.user)

    calendar_data = {
        "weekdays": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
        "weeks": [],
        "month_name": month_names[current_month],
        "year": current_year,
    }

    # Получаем сетку календаря
    cal = calendar.monthcalendar(current_year, current_month)

    # Определяем даты для навигации
    prev_month, prev_year = (
        (12, current_year - 1)
        if current_month == 1
        else (current_month - 1, current_year)
    )
    next_month, next_year = (
        (1, current_year + 1)
        if current_month == 12
        else (current_month + 1, current_year)
    )

    # Получаем количество дней в месяцах
    prev_month_days = calendar.monthrange(prev_year, prev_month)[1]

    first_day_of_month = calendar.weekday(current_year, current_month, 1)

    # Заполняем календарь
    next_month_day = 1
    prev_month_start = prev_month_days - first_day_of_month + 1

    for week in cal:
        week_dates = []
        for day in week:
            if day == 0:
                if len(calendar_data["weeks"]) == 0:
                    # Дни предыдущего месяца
                    prev_date = date(prev_year, prev_month, prev_month_start)
                    day_class = (
                        "bg-success bg-opacity-50 text-white-50"
                        if is_date_in_streak(prev_date)
                        else "bg-secondary bg-opacity-10 text-white-50"
                    )

                    week_dates.append(
                        {
                            "day": prev_month_start,
                            "class": day_class,
                        },
                    )
                    prev_month_start += 1
                else:
                    # Дни следующего месяца
                    week_dates.append(
                        {
                            "day": next_month_day,
                            "class": "bg-secondary bg-opacity-10 text-white-50",
                        },
                    )
                    next_month_day += 1
            else:
                current_date = date(current_year, current_month, day)
                is_today = current_date == user_cal.last_date

                # Определяем class для дня
                if is_today:
                    day_class = (
                        "bg-success"
                        if user_cal.is_streak
                        else "bg-secondary bg-opacity-75"
                    )
                else:
                    day_class = (
                        "bg-success"
                        if is_date_in_streak(current_date)
                        else "bg-secondary bg-opacity-25 text-white-75"
                    )

                week_dates.append({"day": day, "class": day_class, "today": is_today})
        calendar_data["weeks"].append(week_dates)
      

    return calendar_data


def current_streak(request):
    """Возвращает текущую серию стриков"""

    calendar = Calendar.objects.filter(user=request.user).order_by("-last_date").first()
    if calendar.is_streak:
        return (calendar.last_date - calendar.first_date + timedelta(days=1)).days
    else:
        return (calendar.last_date - calendar.first_date).days


def get_day_word(number):
    """Возвращает правильное склонение слова 'день' в зависимости от числа"""

    last_digit = number % 10
    last_two_digits = number % 100

    if 11 <= last_two_digits <= 19:
        return "дней"
    elif last_digit == 1:
        return "день"
    elif 2 <= last_digit <= 4:
        return "дня"
    else:
        return "дней"
