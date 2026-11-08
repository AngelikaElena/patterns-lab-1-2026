from datetime import datetime

from adapters import DigitalClockAdapter
from clocks import AnalogClock
from services import ClockFormatter, ClockHistory


class ClockFacade:
    """Фасад, предоставляющий удобный интерфейс для работы с часами."""

    def __init__(self, analog_clock: AnalogClock | None = None) -> None:
        # Внутри фасада живут все нужные компоненты подсистемы
        clock = analog_clock if analog_clock else AnalogClock()
        self._adapter = DigitalClockAdapter(clock)
        self._formatter = ClockFormatter()
        self._history = ClockHistory()

    def set_date_time(self, date: datetime) -> None:
        """Устанавливает время через адаптер и сохраняет в историю."""
        self._adapter.set_date_time(date)
        self._history.add(date)

    def get_date_time(self) -> datetime:
        """Возвращает текущее время из адаптера."""
        return self._adapter.get_date_time()

    def get_formatted_time(self, fmt: str = "%d.%m.%Y %H:%M:%S") -> str:
        """Возвращает отформатированную строку времени."""
        return self._formatter.format(self.get_date_time(), fmt)

    def get_history(self) -> tuple[datetime, ...]:
        """Возвращает историю изменений."""
        return self._history.all()