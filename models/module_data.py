from module import Module


class ModuleData:
    def __init__(self, title):
        self.title = title

    def create_module(self, db):
        module = Module(db, None, self.title)
        # Дополнительные действия при создании модуля
        return module

    def edit_module(self, module):
        module.title = self.title
        # Дополнительные действия при редактировании модуля