"""
Здесь необходимо реализовать Adapter.

Класс должен реализовать interfaces.BaseDigitalClock и использовать
существующий clocks.AnalogClock через композицию.
"""

# TODO: реализуйте DigitalClockAdapter.

from datetime import datetime

from clocks import AnalogClock
from consts import DayNightDivision
from interfaces import BaseDigitalClock


class DigitalClockAdapter(BaseDigitalClock):
    """Адаптер, превращающий аналоговые часы в цифровые."""

    def __init__(self, analog_clock: AnalogClock) -> None:
        # Композиция: адаптер хранит внутри себя объект аналоговых часов
        self._analog_clock = analog_clock

    def set_date_time(self, date: datetime) -> None:
        """Преобразует datetime в углы и устанавливает их в AnalogClock."""
        # 1. Определяем AM или PM (12 часов дня и позже - это PM)
        day_night = DayNightDivision.PM if date.hour >= 12 else DayNightDivision.AM

        # 2. Переводим 24-часовой формат в 12-часовой для часовой стрелки
        hour_12 = date.hour % 12

        # 3. Считаем углы
        hour_angle = (hour_12 * 30.0) + (date.minute * 0.5) + (date.second * (0.5 / 60.0))
        minute_angle = (date.minute * 6.0) + (date.second * 0.1)
        second_angle = date.second * 6.0

        # 4. Передаем данные в аналоговые часы
        self._analog_clock.set_date_time(
            year=date.year,
            month=date.month,
            day=date.day,
            hour_angle=hour_angle,
            minute_angle=minute_angle,
            second_angle=second_angle,
            day_night_division=day_night,
        )

    def get_date_time(self) -> datetime:
        """Считывает углы из AnalogClock и собирает обратно в datetime."""
        # 1. Забираем дату (она хранится как есть)
        year = self._analog_clock.get_year()
        month = self._analog_clock.get_month()
        day = self._analog_clock.get_day()

        # 2. Вычисляем часы из угла (делим на 30 и берем целую часть)
        hour_12 = int(self._analog_clock.get_hour_angle() // 30.0)
        day_night = self._analog_clock.get_day_night_division()

        # 3. Восстанавливаем 24-часовой формат с учетом AM/PM
        if day_night == DayNightDivision.PM:
            hour = hour_12 + 12 if hour_12 != 0 else 12
        else:
            hour = hour_12

        # 4. Вычисляем минуты и секунды из углов
        minute = int(self._analog_clock.get_minute_angle() // 6.0)
        second = int(self._analog_clock.get_second_angle() // 6.0)

        return datetime(year, month, day, hour, minute, second)