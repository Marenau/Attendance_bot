import sqlite3

conn_db = sqlite3.connect('db.sql')
cur_db = conn_db.cursor()

cur_db.execute('''
  CREATE TABLE IF NOT EXISTS discipline (
    id INTEGER PRIMARY KEY,
    title TEXT
  )
''')

cur_db.execute('''INSERT INTO discipline (title) VALUES ('МАД'), ('БД'), ('VR')''')

cur_db.execute('''
  CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY, 
    last_name TEXT,
    first_name TEXT,  
    second_name TEXT
  )  
''')

cur_db.execute('''INSERT INTO student (last_name, first_name, second_name)
                VALUES 
                ('Алифанов', 'Даниил', 'Алексеевич'),
                ('Анастасиади', 'Дмитрий', 'Евстафьевич'),
                ('Барш', 'Галина', 'Константиновна'), 
                ('Бондарчук', 'Даниил', 'Олегович'),
                ('Воробьёва', 'Дарья', 'Дмитриевна'),
                ('Герасимова', 'Полина', 'Дмитриевна'),
                ('Гурджи', 'Ольга', 'Дмитриевна'),
                ('Доброхвалов', 'Иван', 'Александрович'),
                ('Домбровская', 'Мария', 'Анатольевна'),
                ('Жаркова', 'Светлана', 'Михайловна'),
                ('Иванова', 'Надежда', 'Антоновна'), 
                ('Карюхина', 'Арина', 'Александровна'),
                ('Кузнецов', 'Алексей', 'Сергеевич'),
                ('Мазурова', 'Варвара', 'Дмитриевна'),
                ('Малин', 'Вадим', 'Александрович'),
                ('Модина', 'Елизавета', 'Николаевна'),
                ('Мустафаева', 'Арина', 'Ринатовна'),
                ('Новичков', 'Никита', 'Денисович'),
                ('Пальянов', 'Максим', 'Евгеньевич'),
                ('Петрунин', 'Максим', 'Александрович'), 
                ('Пятаков', 'Максим', 'Алексеевич'),
                ('Ситников', 'Иван', 'Игоревич'),
                ('Скитёва', 'Анастасия', 'Романовна'),  
                ('Соколова', 'Мария', 'Дмитриевна'),
                ('Тотмянин', 'Никита', 'Романович'),
                ('Третьякова', 'Софья', 'Владимировна'),
                ('Трифонов', 'Артём', 'Сергеевич'), 
                ('Чуйко', 'Максим', 'Константинович'),
                ('Шаповалова', 'Эвелина', 'Вадимовна')''')

cur_db.execute('''
  CREATE TABLE IF NOT EXISTS date_and_discipline (
    id INTEGER PRIMARY KEY,
    discipline_id INTEGER NOT NULL,
    date TEXT,  
    FOREIGN KEY (discipline_id) 
      REFERENCES discipline(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  )
''')

cur_db.execute('''
  CREATE TABLE IF NOT EXISTS enroll (
    date_and_discipline_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    PRIMARY KEY (date_and_discipline_id, student_id),
    FOREIGN KEY (date_and_discipline_id) 
      REFERENCES date_and_discipline(id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (student_id)
      REFERENCES student(id)
        ON DELETE CASCADE  
        ON UPDATE CASCADE
  )  
''')

cur_db.execute('''INSERT INTO date_and_discipline (discipline_id, date) VALUES
                ('1', '21-11'),
                ('1', '28-11'),
                ('1', '05-12'),
                ('1', '12-12'),
                ('1', '19-12'),
                ('2', '15-11'),
                ('2', '18-11'),
                ('2', '22-11'),
                ('2', '25-11'),
                ('2', '28-11'),
                ('2', '02-12'),
                ('2', '05-12'),
                ('2', '09-12'),
                ('2', '12-12'),
                ('2', '16-12'),
                ('3', '20-11'),
                ('3', '21-11'),
                ('3', '27-11'),
                ('3', '04-12'),
                ('3', '05-12'),
                ('3', '11-12'),
                ('3', '12-12'),
                ('3', '18-12'),
                ('3', '19-12')''')

conn_db.commit()

cur_db.close()
conn_db.close()
