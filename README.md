# Univercity

Целью этого  проекта является разработка структуры базы данных и реализация API для "Системы управления университетом". Это система, где учитываются студенты, преподаватели, курсы, группы, отделения университета, оценки и другие соответствующие данные.

## Часть 1: Доступные сущности

База данных содержит следующие сущности:
 - Посетитель - любой зарегистрированный человек, относящийся к структуре университета. Таблица 'visitors'
 - Студент - обучающиеся в университете студенты. Таблица 'students'. Связан с посетителем один к одному по полю id.
 - Преподаватель - преподаватели университета. Таблица 'teachers'. Связан с посетителем один к одному по полю id.
 - Курс - Курс обучения. Например курс Мат. Статистики. Таблица 'courses'. Связан с факультетами отношением один ко многим.
 - Группа - группа обучения, в нее входят студенты(связь один ко многим). Таблица  'groups'. Связана со студентами отношением один ко многим
 - Отделение -  кафедра факультета. Связана с преподавателями отношением один ко многим. Связана с Факультетом отношением один ко многим. Таблица 'departments'
 - Оценка - Оценка за курс. Таблица 'course_grades'. Связана со со студентами отношением один ко многим. Связана с курсами отношением один ко многим 
 - Расписание - Расписание группы на день. Таблица 'schedules'
 - Элемент расписани - Одно занятие определенного курса у группы. Таблица 'lessons'
 - Временной слот раcписания - представление временного интервала одного занятия. Таблица 'time_slots'
 - Здание - Здание, относящееся к университету. Таблица 'buildings'
 - Аудитория - Аудитория в здании. Таблица 'auditories'
 - Семестр - семестр обучения. Таблица 'semesters'
 - Факультет - Факультет университета. Связан с преподавателсями отношением один ко многим. Таблица 'courses'
 - Экзамен - Экзамен по определенному курсу. Таблица 'exams'
 - Задание для самостоятельной работы. Задание по определенному курсу. Таблица 'homeworks'
 - Программа курса - Программа курса, состоящая из разных тем. Таблица 'course_programms'
 - Элемент программы курса. Таблица 'course_programms_themes'
 - Учебный план - учебный план группы на семестр, включает разные курсы. Таблица 'education_plans'.
 

ER-диаграмма, которая описывает все сущности и связи между сущностями доступна по этой [ссылке.](https://www.yworks.com/yed-live/?file=https://gist.githubusercontent.com/ead3471/27bc4d7c0fcf181c6bbd10445fe19718/raw/af8c85120656bee42192219966503dfc34a11abc/fastapi%20-%20public)
 
SQL скрипт, который создаёт все таблицы с полями, их типами данных, ключами и связями доступен [здесь](https://github.com/ead3471/Univercity/blob/master/sql_tables_code_create.sql)


## Часть 2: SQL запросы к таблицам
1. Выбрать всех студентов, обучающихся на курсе "Математика".
    ```
    SELECT 
        visitors.id as student_id, 
        visitors.name as student_name, 
        visitors.last_name  as student_last_name
    FROM courses  
    JOIN students_courses on courses.id = students_courses.course_id 
    JOIN visitors on visitors.id = students_courses.student_id 
    WHERE courses.name  = 'Math';
    ```

2. Обновить оценку студента по курсу.
    ```
    UPDATE course_grades 
    SET score  = 3
    WHERE student_id =24 and course_id = 1;
    ```
3. Выбрать всех преподавателей, которые преподают в здании №3.
   ```
    select 
        visitors.id as teacher_id,
        visitors.name as teacher_name
    from buildings 
    join auditories on auditories.building_id = buildings.id 
    join lessons ON lessons.auditory_id  = auditories.id 
    join visitors on visitors.id = lessons.teacher_id 
    where buildings.house_number = '3';
    ```

4. Удалить задание для самостоятельной работы, которое было создано более года назад.
    ```
    DELETE FROM homeworks
    WHERE created < (current_date - interval '1 year');
    ```
5. Добавить новый семестр в учебный год.
    ```
    INSERT INTO semesters (number, start, "end") 
    VALUES
    (1,'2022-01-01', '2022-05-01');
    ```

## Часть 3: FastAPI
Реализованны следующие точки входа API:
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


## Часть 4. Запуск проекта
1. Установите Docker. При необходимости установите djcker-compose
2. Клонируйте проект с github.
    ```
    git clone git@github.com:ead3471/Univercity.git
    ```
3. В командной строке перейдите в дирректорию клонированного проекта. 
    ```
    cd univercity
    ```

4. Соберите и запустите контейнеры с помощью docker-compose:
    ```
    docker-compose up
    ```

Список доступных ендпоинтов станет доступен на локальном комппьютере по этому адресу:
[http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)

