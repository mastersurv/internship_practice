import sqlite3
import bcrypt
from course import Course


class User:
    def __init__(self, db, id, name, username, password, role):
        self.db = db
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.role = role

    def register(self):
        """Логика регистрации пользователя"""
        query = 'INSERT INTO users (id, name, username, password, role) VALUES (?, ?, ?, ?, ?)'
        parameters = (self.id, self.name, self.username, self.password, self.role)
        self.db.execute_query(query, parameters)

    def login(self, user_id, password):
        query = 'SELECT * FROM users WHERE id = ?'
        parameters = (user_id,)
        result = self.db.execute_query(query, parameters)

        if result:
            id, name, username, hashed_password, role = result[0]

            # Проверяем совпадение паролей
            if bcrypt.checkpw(password.encode(), hashed_password):
                return User(self.db, id, name, username, hashed_password, role)
            else:
                return 1

        return None

    def view_available_courses(self):
        """Просмотр доступных курсов"""
        query = 'SELECT id, title, description FROM courses'
        result = self.db.execute_query(query)

        courses = []
        for row in result:
            course_id, title, description = row
            course = Course(self.db, course_id, title, description)
            courses.append(course)

        return courses

    def enroll_course(self, course_id):
        """Запись пользователя на курс"""
        # Проверяем, что пользователь не записан на данный курс
        query = 'SELECT id FROM course_enrollments WHERE user_id = ? AND course_id = ?'
        result = self.db.execute_query(query, (self.id, course_id))
        if result:
            # Пользователь уже записан на курс
            return False

        # Записываем пользователя на курс
        query = 'INSERT INTO course_enrollments (user_id, course_id) VALUES (?, ?)'
        self.db.execute_query(query, (self.id, course_id))

        # Сохраняем изменения
        self.db.commit()

        return True

    def view_course_details(self, course_id):
        """Просмотр подробной информации о курсе"""
        # Получаем информацию о курсе из базы данных
        query = 'SELECT id, title, description FROM courses WHERE id = ?'
        result = self.db.execute_query(query, (course_id,))
        if not result:
            # Курс с указанным ID не найден
            return None

        course_id, title, description = result[0]

        # Форматируем информацию о курсе для вывода
        course_info = f"Курс ID: {course_id}\nНазвание: {title}\nОписание: {description}"

        return course_info

    def view_course_statistics(self, course_id):
        """Просмотр статистики прохождения курса"""
        # Получаем информацию о курсе из базы данных
        query = 'SELECT id, title, students FROM courses WHERE id = ?'
        result = self.db.execute_query(query, (course_id,))
        if not result:
            # Курс с указанным ID не найден
            return None

        course_id, title, students = result[0]

        # Получаем количество студентов, успешно завершивших курс
        query = 'SELECT COUNT(*) FROM enrollments WHERE course_id = ? AND status = ?'
        result = self.db.execute_query(query, (course_id, 'completed'))
        completed_students = result[0][0]

        # Рассчитываем процент успешного завершения
        completion_rate = (completed_students / students) * 100

        # Форматируем информацию о статистике для вывода
        statistics_info = f"Статистика курса ID: {course_id}\nНазвание: {title}\n" \
                          f"Количество студентов: {students}\n" \
                          f"Успешное завершение: {completed_students}/{students} студентов " \
                          f"({completion_rate:.2f}% успешного завершения)"

        return statistics_info
