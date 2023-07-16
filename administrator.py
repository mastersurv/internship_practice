from user import User
from course import Course
from models import CourseData


class Administrator(User):
    def __init__(self, db, id, name, username, password):
        super().__init__(db, id, name, username, password, role='administrator')
        self.role = 'admin'
        self.db = db

    def create_course(self, course_data: CourseData) -> Course:
        """Создает новый учебный курс"""
        # Вставляем новый курс в таблицу courses
        query = 'INSERT INTO courses (title, description) VALUES (?, ?)'
        self.db.execute_query(query, (course_data.title, course_data.description))

        # Получаем ID созданного курса
        course_id = self.db.lastrow_id

        # Создаем и возвращаем объект класса Course
        return Course(self.db, course_id, course_data.title, course_data.description)

    def edit_course(self, course_id: int, course_data: CourseData) -> bool:
        """Редактирует существующий учебный курс"""
        # Обновляем информацию о курсе в таблице courses
        query = 'UPDATE courses SET title = ?, description = ? WHERE id = ?'
        self.db.execute_query(query, (course_data.title, course_data.description, course_id))

        # Проверяем, было ли изменено хотя бы одно значение в базе данных
        if self.db.rowcount > 0:
            return True
        else:
            return False

    def delete_course(self, course_id: int) -> bool:
        """Удаляет учебный курс"""
        # Удаляем курс из таблицы courses
        query = 'DELETE FROM courses WHERE id = ?'
        self.db.execute_query(query, (course_id,))

        # Проверяем, было ли удалено хотя бы одно значение из базы данных
        if self.db.rowcount > 0:
            return True
        else:
            return False

    def manage_user_accounts(self):
        """Управление учетными записями пользователей"""
        # Получаем список всех пользователей из таблицы users
        query = 'SELECT id, name, username, role FROM users'
        users = self.db.execute_query(query)

        # Выводим информацию о каждом пользователе
        for user in users:
            user_id, name, username, role = user
            print(f"ID: {user_id}\nName: {name}\nUsername: {username}\nRole: {role}\n")
