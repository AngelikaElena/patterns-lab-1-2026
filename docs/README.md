# Диаграмма

Поместите сюда структурную диаграмму итоговой реализации Adapter и Facade.

# Структурная диаграмма

Ниже представлена UML-диаграмма классов, отображающая структуру решения с применением паттернов **Adapter** и **Facade**.

```mermaid
classDiagram
    direction TB

    %% Интерфейсы
    class BaseAnalogClock {
        <<interface>>
        +set_date_time()
        +get_hour_angle()
        +get_minute_angle()
        +get_second_angle()
        +get_year()
        +get_month()
        +get_day()
        +get_day_night_division()
    }

    class BaseDigitalClock {
        <<interface>>
        +set_date_time(date: datetime)
        +get_date_time() datetime
    }

    %% Существующий класс (Аналоговые часы)
    class AnalogClock {
        -year: int
        -month: int
        -day: int
        -hour_angle: float
        -minute_angle: float
        -second_angle: float
        -day_night_division: DayNightDivision
    }

    %% Адаптер
    class DigitalClockAdapter {
        -_analog_clock: AnalogClock
        +set_date_time(date: datetime)
        +get_date_time() datetime
    }

    %% Сервисы подсистемы
    class ClockFormatter {
        +format(value: datetime, fmt: str) str
    }

    class ClockHistory {
        -_items: list[datetime]
        +add(value: datetime)
        +all() tuple
    }

    %% Фасад
    class ClockFacade {
        -_adapter: DigitalClockAdapter
        -_formatter: ClockFormatter
        -_history: ClockHistory
        +set_date_time(date: datetime)
        +get_date_time() datetime
        +get_formatted_time(fmt: str) str
        +get_history() tuple
    }

    %% Связи
    BaseAnalogClock <|.. AnalogClock : implements
    BaseDigitalClock <|.. DigitalClockAdapter : implements
    
    DigitalClockAdapter o-- AnalogClock : holds >
    
    ClockFacade *-- DigitalClockAdapter : uses >
    ClockFacade *-- ClockFormatter : uses >
    ClockFacade *-- ClockHistory : uses >