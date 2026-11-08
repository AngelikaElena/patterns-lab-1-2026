from datetime import datetime

import pytest

from adapters.digital_clock_adapter import DigitalClockAdapter
from clocks import AnalogClock
from consts import DayNightDivision


@pytest.fixture
def adapter():
    """Фикстура, создающая адаптер с аналоговыми часами для тестов."""
    return DigitalClockAdapter(AnalogClock())


@pytest.mark.parametrize(
    "dt, expected_hour, expected_minute, expected_second, expected_dn",
    [
        # Полночь
        (datetime(2023, 10, 25, 0, 0, 0), 0.0, 0.0, 0.0, DayNightDivision.AM),
        # Полдень
        (datetime(2023, 10, 25, 12, 0, 0), 0.0, 0.0, 0.0, DayNightDivision.PM),
        # День (например, 15:30:15)
        (
            datetime(2023, 10, 25, 15, 30, 15),
            3 * 30.0 + 30 * 0.5 + 15 * (0.5 / 60.0),
            30 * 6.0 + 15 * 0.1,
            15 * 6.0,
            DayNightDivision.PM,
        ),
        # Ночь (например, 23:59:59)
        (
            datetime(2023, 10, 25, 23, 59, 59),
            11 * 30.0 + 59 * 0.5 + 59 * (0.5 / 60.0),
            59 * 6.0 + 59 * 0.1,
            59 * 6.0,
            DayNightDivision.PM,
        ),
    ],
)
def test_adapter_set_date_time(adapter, dt, expected_hour, expected_minute, expected_second, expected_dn):
    """Тест прямого преобразования (datetime -> углы)."""
    adapter.set_date_time(dt)
    
    clock = adapter._analog_clock
    assert clock.get_year() == dt.year
    assert clock.get_month() == dt.month
    assert clock.get_day() == dt.day
    assert pytest.approx(clock.get_hour_angle(), abs=1e-5) == expected_hour
    assert pytest.approx(clock.get_minute_angle(), abs=1e-5) == expected_minute
    assert pytest.approx(clock.get_second_angle(), abs=1e-5) == expected_second
    assert clock.get_day_night_division() == expected_dn


@pytest.mark.parametrize(
    "dt",
    [
        datetime(2023, 10, 25, 0, 0, 0),    # Полночь
        datetime(2023, 10, 25, 12, 0, 0),   # Полдень
        datetime(2023, 10, 25, 15, 30, 15), # День
        datetime(2023, 10, 25, 23, 59, 59), # Ночь
    ],
)
def test_adapter_get_date_time(adapter, dt):
    """Тест обратного преобразования (углы -> datetime)."""
    # Сначала устанавливаем время
    adapter.set_date_time(dt)
    # Теперь получаем его обратно
    result_dt = adapter.get_date_time()
    
    assert result_dt == dt