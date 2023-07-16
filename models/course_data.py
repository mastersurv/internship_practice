from module import Module


class CourseData:
	def __init__(self, title, description, db):
		self.title = title
		self.description = description
		self.db = db
		self.modules = []
		self.load_modules(self.db, self.title)

	def add_module(self, module):
		"""Добавляет модуль в курс."""
		self.modules.append(module)

	def remove_module(self, title):
		# Удаляем модуль из базы данных
		query = 'DELETE FROM modules WHERE title = ?'
		self.db.execute_query(query, (title,))

		# Удаляем модуль из списка модулей курса
		for module in self.modules:
			if module.id == title:
				self.modules.remove(module)
				break

	def load_modules(self, db, title):
		query = 'SELECT id, title FROM modules WHERE title = ?'
		result = db.execute_query(query, (title,))
		for row in result:
			module_id, module_title = row
			module = Module(db, module_id, module_title)
			self.add_module(module)
