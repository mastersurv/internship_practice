from material import Material


class Module:
    def __init__(self, db, id, title):
        self.id = id
        self.title = title
        self.materials = []
        self.db = db
        self.load_materials()

    def add_material(self, material):
        self.materials.append(material)

        # Выполнение операции вставки материала в таблицу materials
        query = 'INSERT INTO materials (module_id, title) VALUES (?, ?)'
        parameters = (self.id, material.title)
        self.db.execute_query(query, parameters)

    def remove_material(self, material_id):
        for material in self.materials:
            if material.id == material_id:
                self.materials.remove(material)

                # Выполнение операции удаления материала из таблицы materials
                query = 'DELETE FROM materials WHERE id = ?'
                parameters = (material_id,)
                self.db.execute_query(query, parameters)
                break

    def load_materials(self):
        # Выполняем запрос для загрузки материалов данного модуля из базы данных
        query = 'SELECT id, title FROM materials WHERE module_id = ?'
        materials_data = self.db.execute_query(query, (self.id,))

        # Создаем объекты материалов и добавляем их в список self.materials
        for material_row in materials_data:
            material_id, material_title = material_row
            material = Material(material_id, material_title)
            self.materials.append(material)

    def create(self, database):
        query = "INSERT INTO modules (course_id, title, content) VALUES (?, ?, ?)"
        parameters = (self.course_id, self.title, self.content)
        result = database.execute_query(query, parameters)

        if result:
            self.module_id = database.lastrow_id
            return True

        return False