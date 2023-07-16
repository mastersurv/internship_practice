from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from database import DataBase
from course import Course
from module import Module
from states import CreateTaskStates


async def create_task_start(message: types.Message, state: FSMContext):
    # Получаем данные из сообщения
    module_id = message.text.split()[-1]  # Предполагается, что сообщение содержит идентификатор модуля
    module_id = int(module_id)

    # Проверяем, существует ли модуль с указанным идентификатором
    module = Module.get_by_id(module_id)
    if not module:
        await message.answer("Модуль не найден.")
        return

    # Устанавливаем состояние, чтобы ожидать названия и описания задания
    await CreateTaskStates.title.set()
    await state.update_data(module_id=module_id)

    await message.answer("Введите название задания:")


async def create_task_title(message: types.Message, state: FSMContext):
    # Получаем данные из состояния
    data = await state.get_data()
    module_id = data.get("module_id")

    # Получаем название задания из сообщения
    task_title = message.text

    # Устанавливаем состояние, чтобы ожидать описания задания
    await CreateTaskStates.description.set()
    await state.update_data(task_title=task_title)

    await message.answer("Введите описание задания:")


async def create_task_description(message: types.Message, state: FSMContext):
    # Получаем данные из состояния
    data = await state.get_data()
    module_id = data.get("module_id")
    task_title = data.get("task_title")

    # Получаем описание задания из сообщения
    task_description = message.text

    # Создаем объект задания
    task = Task(module_id=module_id, title=task_title, description=task_description)

    # Добавляем задание в базу данных
    database = Database("database.db")
    task.create(database)

    await message.answer("Задание успешно добавлено.")

    # Сбрасываем состояние
    await state.finish()


async def cancel_create_task(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Добавление задания отменено.")

    # Сбрасываем состояние
    await state.finish()
