# Univercity

Задание для кандидата на должность Junior Python Developer

Целью этого задания является разработка структуры базы данных и реализация API для "Системы управления университетом". Это система, где учитываются студенты, преподаватели, курсы, группы, отделения университета, оценки и другие соответствующие данные.

## Часть 1: База данных

Сначала вам необходимо создать схему базы данных, состоящую из 15 сущностей:
 - Студент +
 - Преподаватель +
 - Курс +
 - Группа +
 - Отделение +
 - Оценка +
 - Расписание 
 - Здание +
 - Аудитория +
 - Семестр +
 - Факультет +
 - Экзамен +
 - Задание для самостоятельной работы +
 - Программа курса +
 - Учебный план
 
Ваша задача - создать ER-диаграмму (схему связей между сущностями) и определить свойства каждой из этих сущностей. Затем напишите SQL запросы для создания соответствующих таблиц, включающих все необходимые поля и связи между ними.
Мы ждём от вас:
 - ER-диаграмму, которая описывает все сущности и связи между ними.
 - SQL скрипт, который создаёт все таблицы с полями, их типами данных, ключами и связями.
 - Краткое описание каждой сущности и её свойств.

## Часть 2: SQL запросы
Пожалуйста, реализуйте следующие SQL запросы:
Выбрать всех студентов, обучающихся на курсе "Математика".
Обновить оценку студента по курсу.
Выбрать всех преподавателей, которые преподают в здании №3.
Удалить задание для самостоятельной работы, которое было создано более года назад.
Добавить новый семестр в учебный год.

## Часть 3: FastAPI
Мы бы хотели увидеть следующие точки входа API:
 - POST /students - создать нового студента.
 - GET /students/{student_id} - получить информацию о студенте по его id.
 - PUT /students/{student_id} - обновить информацию о студенте по его id.
 - DELETE /students/{student_id} - удалить студента по его id.
 - GET /teachers - получить список всех преподавателей.
 - POST /courses - создать новый курс.
 - GET /courses/{course_id} - получить информацию о курсе по его id.
 - GET /courses/{course_id}/students - получить список всех студентов на курсе.
 - POST /grades - создать новую оценку для студента по курсу.
 - PUT /grades/{grade_id} - обновить оценку студента по курсу.
Ожидается реализация этих точек входа API с использованием FastAPI, включая входные и выходные модели Pydantic для каждого маршрута.

## Часть 4: Публикация и документация
Загрузите свой код в публичный репозиторий на GitHub и предоставьте ссылку на него. Включите в README файл:
Описание проекта.
Инструкции по установке и запуску вашего приложения.
Инструкции по использованию API.

