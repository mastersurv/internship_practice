from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards.start_keyboards import get_main_menu_keyboard, get_back_to_main_menu_keyboard
from models.course_data import CourseData
from administrator import Administrator
from create_bot import dp, db


class CreationState(StatesGroup):
	Title = State()
	Description = State()


# @dp.callback_query_handler(text='create_course', state='*')
async def create_course_handler(callback_query: types.CallbackQuery, state: FSMContext):
	await callback_query.answer()
	# Отправляем сообщение с просьбой ввести название курса
	await callback_query.message.delete()
	await callback_query.message.answer("Вы приступили к созданию собственного курса!\n"
	                                    "Введите название нового курса:")
	# Устанавливаем состояние CreationState.Title для текущего пользователя
	await CreationState.Title.set()


@dp.message_handler(state=CreationState.Title)
async def process_course_title(message: types.Message, state: FSMContext):
	# Получаем введенное название курса
	course_title = message.text.strip()

	# Проверяем, что название курса не пустое
	if not course_title:
		await message.answer("Название курса не может быть пустым.")
		return

	# Сохраняем название курса в контексте состояния
	await state.update_data(course_title=course_title)

	# Отправляем сообщение с просьбой ввести описание курса
	await message.answer("Введите описание нового курса:")

	# Устанавливаем состояние CreationState.Description
	await CreationState.Description.set()


@dp.message_handler(state=CreationState.Description)
async def process_course_description(message: types.Message, state: FSMContext):
	# Получаем введенное описание курса
	course_description = message.text.strip()

	# Проверяем, что описание курса не пустое
	if not course_description:
		await message.answer("Описание курса не может быть пустым.")
		return

	# Получаем данные из контекста состояния
	data = await state.get_data()
	course_title = data['course_title']

	# Создаем объект CourseData с данными о курсе
	course_data = CourseData(title=course_title, description=course_description, db=db)

	# Создаем экземпляр класса Administrator
	admin = Administrator(db, id=message.from_user.id, name=message.from_user.full_name,
	                      username=message.from_user.username, password=None)

	# Создаем курс с использованием метода create_course
	course = admin.create_course(course_data)

	# Выводим информацию о созданном курсе
	await message.answer(f"Курс успешно создан!\n"
	                     f"Название: {course.title}\n"
	                     f"Описание: {course.description}\n"
	                     f"Чтобы вернуться в меню выбора - нажмите кнопку ниже",
	                     reply_markup=get_back_to_main_menu_keyboard())

	# Завершаем создание курса
	await state.finish()


# @dp.callback_query_handler(text='back_to_menu', state='*')
async def back_to_menu(callback_query: types.CallbackQuery, state: FSMContext):
	await callback_query.answer()
	await callback_query.message.edit_text("Вы уже зарегистрированы. Можете начать обучение.\n"
	                                       "Выберите действие:",
	                                       reply_markup=get_main_menu_keyboard())
