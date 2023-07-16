class Course:
	def __init__(self, db, id, title, description):
		self.id = id
		self.db = db
		self.title = title
		self.description = description
		self.students = []
		self.load_students()

	def add_student(self, student_id):
		self.students.append(student_id)
		self.db.execute_query('INSERT INTO course_enrollments (course_id, student_id) VALUES (?, ?)',
		                      (self.id, student_id))

	def remove_student(self, student_id):
		if student_id in self.students:
			self.students.remove(student_id)
			self.db.execute_query('DELETE FROM course_enrollments WHERE course_id = ? AND student_id = ?',
			                      (self.id, student_id))

	def load_students(self):
		query = 'SELECT student_id FROM course_enrollments WHERE course_id = ?'
		result = self.db.execute_query(query, (self.id,))
		self.students = [row[0] for row in result]

	def get_course_by_id(self, course_id):
		query = "SELECT * FROM courses WHERE course_id = ?"
		parameters = (course_id,)
		result = self.db.execute_query(query, parameters)

		if result:
			# Получаем значения столбцов из результата запроса
			course_id, title, description = result[0]
			course = Course(self.db, course_id, title, description)
			return course

		return None