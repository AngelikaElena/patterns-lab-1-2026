from datetime import datetime

import pytest

from facades import ClockFacade
from services import ClockHistory


def test_facade_set_and_get_time():
    """Тест установки и получения времени через фасад."""
    facade = ClockFacade()
    dt = datetime(2023, 10, 25, 12, 30, 45)
    
    facade.set_date_time(dt)
    assert facade.get_date_time() == dt


def test_facade_formatting():
    """Тест получения форматированного времени."""
    facade = ClockFacade()
    dt = datetime(2023, 10, 25, 12, 30, 45)
    facade.set_date_time(dt)
    
    # Проверяем формат по умолчанию
    assert facade.get_formatted_time() == "25.10.2023 12:30:45"
    # Проверяем кастомный формат
    assert facade.get_formatted_time("%Y-%m-%d") == "2023-10-25"


def test_facade_history():
    """Тест сохранения истории через фасад."""
    facade = ClockFacade()
    dt1 = datetime(2023, 10, 25, 10, 0, 0)
    dt2 = datetime(2023, 10, 25, 11, 0, 0)
    
    facade.set_date_time(dt1)
    facade.set_date_time(dt2)
    
    history = facade.get_history()
    assert len(history) == 2
    assert history[0] == dt1
    assert history[1] == dt2


def test_history_directly():
    """Отдельный тест для истории (проверка работы класса ClockHistory)."""
    history = ClockHistory()
    dt = datetime(2023, 1, 1, 0, 0, 0)
    
    assert history.all() == ()  # Изначально пусто
    
    history.add(dt)
    
    assert history.all() == (dt,)
    assert isinstance(history.all(), tuple)  # Проверяем, что возвращается кортеж