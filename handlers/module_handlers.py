from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from course import Course
from module import Module


class CreateModuleState(StatesGroup):
	title = State()
	description = State()


async def start_create_module(message: types.Message):
	# Получаем ID существующего курса из аргументов команды
	course_id = int(message.get_args())

	# Проверяем, существует ли курс с указанным ID
	course = Course.get_course_by_id(course_id)
	if not course:
		await message.answer("Курс не найден")
		return

	# Устанавливаем состояние для создания модуля
	await CreateModuleState.title.set()
	await message.answer("Введите название модуля:")


async def process_module_title(message: types.Message, state: FSMContext):
	# Получаем название модуля из сообщения
	module_title = message.text

	# Сохраняем название модуля в контексте состояния
	await state.update_data(module_title=module_title)

	# Переходим к вводу описания модуля
	await CreateModuleState.description.set()
	await message.answer("Введите описание модуля:")


async def process_module_description(message: types.Message, state: FSMContext):
	# Получаем описание модуля из сообщения
	module_description = message.text

	# Получаем сохраненное название модуля из контекста состояния
	module_data = await state.get_data()
	module_title = module_data.get("module_title")

	# Получаем ID существующего курса из аргументов команды
	course_id = int(message.get_args())

	# Создаем модуль и связываем его с курсом
	module = Module.create(title=module_title, description=module_description, course_id=course_id)

	# Сбрасываем состояние
	await state.finish()

	await message.answer(f"Модуль '{module.title}' успешно создан!")
