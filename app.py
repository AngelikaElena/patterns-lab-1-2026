from datetime import datetime

from facades import ClockFacade


def main() -> None:
    # Создаем фасад. Клиент больше не знает про AnalogClock или Adapter
    facade = ClockFacade()
    print("Фасад создан. Работаем через ClockFacade.")

    # Установим какое-нибудь время
    now = datetime(2023, 10, 25, 15, 30, 15)
    facade.set_date_time(now)

    # Проверим, что все работает
    print(f"Текущее время: {facade.get_date_time()}")
    print(f"Форматированное время: {facade.get_formatted_time()}")
    
    # Установим еще одно время, чтобы проверить историю
    facade.set_date_time(datetime(2024, 1, 1, 0, 0, 0))
    
    print("\nИстория изменений:")
    for dt in facade.get_history():
        print(f" - {dt}")


if __name__ == "__main__":
    main()