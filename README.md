<br />
<div align="center">
  <a href="https://github.com/Rev-1b/MirGovoritTest">
  </a>

<h3 align="center">Тех-задание для 'O-Комплекс'</h3>

  <p align="center">
    Документация по установке и работе с приложением прогноза погоды
    <br />В самом низу README я подробно описал свои решения по проекту
</div>



## Особенности

- **Прогноз погоды:** Просматривайте прогноз погоды для любого города.
- **Автозаполнение**. Получайте предложения по названиям городов во время ввода.
- **Статистика.** Узнайте, сколько раз другие пользователи искали ваш любимый город.
- **История пользователя:** сохранение истории поиска для отдельных пользователей.
- **Docker:** контейнерное приложение для простого развертывания.
- **Тесты**: автоматические тесты для проверки функциональности приложения.

## Используемые технологии

- **Веб-фреймворк:** Джанго
- **API погоды:** OpenWeatherMap (https://openweathermap.org)
- **Автозаполнение:** Стороннее API DaData (https://dadata.ru)
- **База данных:** Django ORM с SQLite (по умолчанию) или PostgreSQL (для рабочей среды).
- **Docker:** контейнеризация для разработки и развертывания.
- **Тестирование:** встроенная среда тестирования Django.

## Установка и настройка

### Локальная разработка

1. **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/Rev-1b/WeatherTest.git
    ```

2. **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Примените миграции:**

    ```bash
    python manage.py migrate
    ```

4. **Запустите сервер:**

    ```bash
    python manage.py runserver
    ```

   Сайт будет доступен по адресу `http://localhost:8000`.

### Docker

1. **Запустите docker-compose:**

    ```bash
    docker-compose up --build
    ```

   Сайт будет доступен по адресу `http://localhost:8000`.

## Использование

Рабочая область главной страницы делится на 5 основных зон:
- **Поисковая строка:** Место для выбора города. При вводе появляются подсказки
- **Окно основной информации:** Показывает краткую сводку по выбранному городу.
- **Окно прогноза:** Показывает прогноз погоды для выбранного города на несколько часов вперед.
- **Окно Истории поиска:** Позволяет быстро отобразить информацию по уже найденному городу. Требует авторизации.
- **Навигационная полоса:** Позволяет войти/выйти из системы либо перейти на страницу статистики.

Страница статистики похожа на главную страницу, однако у нее отсутствуют окна информации, прогноза и истории поиска.
Вместо этого, при поиске города, вам будет показано, сколько всего раз его запрашивали для отображения.

## Тестирование

Для запуска тестов, выполните команду, находясь в одной директории с manage.py:

```bash
python manage.py test
```

Эту команду можно запустить как из IDE, так и из docker контейнера.

## Комментарии по проекту

- **База данных:** Для удобства проверки, сейчас проект работает на SQLite3. Однако, в docker-compose есть закомментированный участок, который запускает PostgreSQL. При необходимости, надо раскомментировать все строчки в docker-compose, и поменять DATABASES в файле settings.py
- **Секреты:** Вынес SECRET_KEY в .env файл, который подключается к контейнеру при запуске. При работе БЕЗ Docker, необходимо добавить DJANGO_SECRET_KEY в ENVIRONMENT VARIABLES вашей run configuration

К сожалению, я не до конца понял, что именно от меня требуется по заданию. Если бы у меня была возможность уточнить требования к работе, я бы предпочел работать с DRF и JS, а не стоковым Django. Это позволило бы повысить юзер экспириенс. Однако, вакансия открыта на позицию бекендера, поэтому было принято решение делать все фронтенд через Django Templates.

