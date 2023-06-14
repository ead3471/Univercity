
CREATE TABLE public.buildings (
	id serial4 NOT NULL,
	street varchar(50) NULL,
	house_number varchar(10) NULL,
	CONSTRAINT buildings_pkey PRIMARY KEY (id)
);

CREATE TABLE public.faculties (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT faculties_name_key UNIQUE (name),
	CONSTRAINT faculties_pkey PRIMARY KEY (id)
);


CREATE TABLE public.semesters (
	id serial4 NOT NULL,
	"start" timestamp NULL,
	"end" timestamp NULL,
	"number" int4 NULL,
	CONSTRAINT semesters_pkey PRIMARY KEY (id)
);

CREATE TABLE public.timeslots (
	id serial4 NOT NULL,
	"name" varchar(64) NULL,
	"start" time NULL,
	"end" time NULL,
	CONSTRAINT timeslots_name_key UNIQUE (name),
	CONSTRAINT timeslots_pkey PRIMARY KEY (id)
);


CREATE TABLE public.visitors (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	middle_name varchar NOT NULL,
	last_name varchar NOT NULL,
	birthdate date NOT NULL,
	passport_id varchar NOT NULL,
	CONSTRAINT visitors_passport_id_key UNIQUE (passport_id),
	CONSTRAINT visitors_pkey PRIMARY KEY (id)
);

CREATE TABLE public.auditories (
	id serial4 NOT NULL,
	room_number varchar(10) NULL,
	building_id int4 NULL,
	CONSTRAINT auditories_pkey PRIMARY KEY (id),
	CONSTRAINT uq_room_building UNIQUE (room_number, building_id),
	CONSTRAINT auditories_building_id_fkey FOREIGN KEY (building_id) REFERENCES public.buildings(id)
);

CREATE TABLE public.courses (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	faculty_id int4 NULL,
	CONSTRAINT courses_pkey PRIMARY KEY (id),
	CONSTRAINT courses_faculty_id_fkey FOREIGN KEY (faculty_id) REFERENCES public.faculties(id)
);


CREATE TABLE public.departments (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	faculty_id int4 NULL,
	CONSTRAINT departments_pkey PRIMARY KEY (id),
	CONSTRAINT uq_faculty_department UNIQUE (faculty_id, name),
	CONSTRAINT departments_faculty_id_fkey FOREIGN KEY (faculty_id) REFERENCES public.faculties(id)
);


CREATE TABLE public."groups" (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	department_id int4 NULL,
	CONSTRAINT groups_name_key UNIQUE (name),
	CONSTRAINT groups_pkey PRIMARY KEY (id),
	CONSTRAINT groups_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id)
);


CREATE TABLE public.homeworks (
	id serial4 NOT NULL,
	course_id int4 NULL,
	created timestamp NULL,
	"text" text NULL,
	CONSTRAINT homeworks_pkey PRIMARY KEY (id),
	CONSTRAINT homeworks_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id)
);


CREATE TABLE public.shedules (
	id serial4 NOT NULL,
	"date" date NULL,
	group_id int4 NULL,
	CONSTRAINT shedules_pkey PRIMARY KEY (id),
	CONSTRAINT uq_group_date UNIQUE (group_id, date),
	CONSTRAINT shedules_group_id_fkey FOREIGN KEY (group_id) REFERENCES public."groups"(id)
);



CREATE TABLE public.students (
	id int4 NOT NULL,
	group_id int4 NULL,
	CONSTRAINT students_pkey PRIMARY KEY (id),
	CONSTRAINT students_group_id_fkey FOREIGN KEY (group_id) REFERENCES public."groups"(id),
	CONSTRAINT students_id_fkey FOREIGN KEY (id) REFERENCES public.visitors(id)
);



CREATE TABLE public.students_courses (
	student_id int4 NULL,
	course_id int4 NULL,
	CONSTRAINT uq_student_course UNIQUE (student_id, course_id),
	CONSTRAINT students_courses_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id),
	CONSTRAINT students_courses_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id)
);



CREATE TABLE public.teachers (
	id int4 NOT NULL,
	department_id int4 NULL,
	CONSTRAINT teachers_pkey PRIMARY KEY (id),
	CONSTRAINT teachers_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id),
	CONSTRAINT teachers_id_fkey FOREIGN KEY (id) REFERENCES public.visitors(id)
);



CREATE TABLE public.course_grades (
	id serial4 NOT NULL,
	score int4 NULL,
	student_id int4 NULL,
	course_id int4 NULL,
	CONSTRAINT course_grades_pkey PRIMARY KEY (id),
	CONSTRAINT course_grades_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id),
	CONSTRAINT course_grades_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id)
);



CREATE TABLE public.course_programms (
	id serial4 NOT NULL,
	"name" varchar(50) NULL,
	description text NULL,
	course_id int4 NULL,
	CONSTRAINT course_programms_course_id_key UNIQUE (course_id),
	CONSTRAINT course_programms_pkey PRIMARY KEY (id),
	CONSTRAINT course_programms_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id)
);



CREATE TABLE public.course_programms_themes (
	id serial4 NOT NULL,
	"name" varchar(50) NULL,
	description text NULL,
	duration int4 NULL,
	course_programm_id int4 NULL,
	CONSTRAINT course_programms_themes_pkey PRIMARY KEY (id),
	CONSTRAINT course_programms_themes_course_programm_id_fkey FOREIGN KEY (course_programm_id) REFERENCES public.course_programms(id)
);



CREATE TABLE public.education_plans (
	id serial4 NOT NULL,
	semester_id int4 NULL,
	group_id int4 NULL,
	CONSTRAINT education_plans_pkey PRIMARY KEY (id),
	CONSTRAINT education_plans_group_id_fkey FOREIGN KEY (group_id) REFERENCES public."groups"(id),
	CONSTRAINT education_plans_semester_id_fkey FOREIGN KEY (semester_id) REFERENCES public.semesters(id)
);


CREATE TABLE public.exams (
	id serial4 NOT NULL,
	course_id int4 NULL,
	"start" timestamp NULL,
	"end" timestamp NULL,
	teacher_id int4 NULL,
	CONSTRAINT exams_pkey PRIMARY KEY (id),
	CONSTRAINT exams_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id),
	CONSTRAINT exams_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES public.teachers(id)
);



CREATE TABLE public.lessons (
	id serial4 NOT NULL,
	schedule_id int4 NULL,
	course_id int4 NULL,
	teacher_id int4 NULL,
	timeslot_id int4 NULL,
	auditory_id int4 NULL,
	CONSTRAINT lessons_pkey PRIMARY KEY (id),
	CONSTRAINT uq_time_auditory_date UNIQUE (timeslot_id, auditory_id, schedule_id),
	CONSTRAINT lessons_auditory_id_fkey FOREIGN KEY (auditory_id) REFERENCES public.auditories(id),
	CONSTRAINT lessons_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id),
	CONSTRAINT lessons_schedule_id_fkey FOREIGN KEY (schedule_id) REFERENCES public.shedules(id),
	CONSTRAINT lessons_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES public.teachers(id),
	CONSTRAINT lessons_timeslot_id_fkey FOREIGN KEY (timeslot_id) REFERENCES public.timeslots(id)
);



CREATE TABLE public.plans_courses (
	course_id int4 NULL,
	plan_id int4 NULL,
	CONSTRAINT uq_course_plan UNIQUE (course_id, plan_id),
	CONSTRAINT plans_courses_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id),
	CONSTRAINT plans_courses_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.education_plans(id)
);


CREATE TABLE public.students_exams (
	student_id int4 NULL,
	exam_id int4 NULL,
	CONSTRAINT uq_student_exam UNIQUE (student_id, exam_id),
	CONSTRAINT students_exams_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id),
	CONSTRAINT students_exams_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id)
);



CREATE TABLE public.teacher_course (
	teacher_id int4 NULL,
	course_id int4 NULL,
	CONSTRAINT uq_teacher_course UNIQUE (teacher_id, course_id),
	CONSTRAINT teacher_course_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id),
	CONSTRAINT teacher_course_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES public.teachers(id)
);



CREATE TABLE public.exam_grades (
	id serial4 NOT NULL,
	exam_id int4 NULL,
	score int4 NULL,
	student_id int4 NULL,
	CONSTRAINT exam_grades_pkey PRIMARY KEY (id),
	CONSTRAINT exam_grades_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id),
	CONSTRAINT exam_grades_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id)
);