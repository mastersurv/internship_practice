class Material:
	def __init__(self, db, id, module_id, title, description):
		self.id = id
		self.db = db
		self.module_id = module_id
		self.title = title
		self.description = description

	def get_tasks_by_module_id(self, module_id):
		query = "SELECT * FROM tasks WHERE module_id = ?"
		parameters = (module_id,)
		result = self.db.execute_query(query, parameters)
		tasks = []

		for row in result:
			task_id, module_id, title, description = row
			task = Task(self.db, task_id, module_id, title, description)
			tasks.append(task)

		return tasks

	def get_task_by_id(self, task_id):
		query = "SELECT * FROM tasks WHERE id = ?"
		parameters = (task_id,)
		result = self.db.execute_query(query, parameters)

		if result:
			task_id, module_id, title, description = result[0]
			task = Task(self.db, task_id, module_id, title, description)
			return task

		return None

	def create_task(self, module_id, title, description):
		query = "INSERT INTO tasks (module_id, title, description) VALUES (?, ?, ?)"
		parameters = (module_id, title, description)
		self.db.execute_query(query, parameters)
		task_id = self.db.lastrow_id
		task = Task(self.db, task_id, module_id, title, description)
		return task

	def update_task(self, task_id, title, description):
		query = "UPDATE tasks SET title = ?, description = ? WHERE id = ?"
		parameters = (title, description, task_id)
		self.db.execute_query(query, parameters)

	def delete_task(self, task_id):
		query = "DELETE FROM tasks WHERE id = ?"
		parameters = (task_id,)
		self.db.execute_query(query, parameters)
