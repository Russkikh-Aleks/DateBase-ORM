from sqlalchemy.orm import sessionmaker as ss
import functions as f


if __name__ == '__main__':

    # Создание движка
    module = 'postgresql'
    login = 'postgres'
    password = ''
    port = ''
    datebase = ''
    engine = f.create_engine(module, login, password, datebase)

    # Создание таблиц
    f.create_tables(engine)

    # Создание сессии
    Session = ss(bind=engine)
    session = Session()

    # Создание экземпляров моделей из JSON файла
    f.instantiation_from_json('tests_data.json', session)

    # Вывод фактов покупки книг по id или названия издателя
    f.printing_purchases(input('Введите имя или id издателя: '), session)

    session.close()

    f.del_tables(engine)
