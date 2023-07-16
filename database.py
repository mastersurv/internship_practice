import sqlite3

class DataBase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.lastrow_id = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query, parameters=None):
        self.connect()
        cursor = self.conn.cursor()

        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)

        self.lastrow_id = cursor.lastrowid
        result = cursor.fetchall()

        self.conn.commit()
        cursor.close()

        return result

    def create_tables(self):
        self.connect()

        cursor = self.conn.cursor()

        # Создание таблицы users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                username TEXT,
                password TEXT,
                role TEXT
            )
        ''')

        # Создание таблицы courses
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                students INTEGER
            )
        ''')

        # Создание таблицы course_enrollments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS course_enrollments (
                course_id INTEGER,
                student_id INTEGER,
                PRIMARY KEY (course_id, student_id),
                FOREIGN KEY (course_id) REFERENCES courses (id),
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        ''')

        # Создание таблицы enrollments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY,
                course_id INTEGER,
                student_id INTEGER,
                status TEXT,
                FOREIGN KEY (course_id) REFERENCES courses (id),
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        ''')

        # Создание таблицы modules
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS modules (
                        id INTEGER PRIMARY KEY,
                        course_id INTEGER,
                        title TEXT,
                        FOREIGN KEY (course_id) REFERENCES courses (id)
                    )
                ''')

        # Создание таблицы materials
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS materials (
                    id INTEGER PRIMARY KEY,
                    module_id INTEGER,
                    title TEXT,
                    FOREIGN KEY (module_id) REFERENCES modules (id)
                )
            ''')

        self.conn.commit()
        self.disconnect()
