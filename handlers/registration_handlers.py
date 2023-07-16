from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram import types
from create_bot import db
import bcrypt
from user import User
from keyboards import start_keyboards


class RegistrationState(StatesGroup):
	Password = State()


# @dp.callback_query_handlers(text='register')
async def register_button_handler(callback_query: types.CallbackQuery, state: FSMContext):
	await callback_query.answer()
	# Отправляем сообщение с приветствием и инструкцией
	await callback_query.message.edit_text("Добро пожаловать в регистрацию!")

	# Сбрасываем состояние регистрации, если оно уже было начато
	await state.finish()

	# Переходим в состояние пароля
	await RegistrationState.Password.set()
	await callback_query.message.answer("Введите пароль для регистрации:")


# @dp.message_handler(state=RegistrationState.Password)
async def process_password_handler(message: types.Message, state: FSMContext):
	# Получаем введенный пользователем пароль
	password = message.text.strip()

	# Проверяем валидность пароля и сохраняем его в контексте состояния
	if len(password) < 6:
		await message.answer("Пароль должен содержать не менее 6 символов.")
		return

	# Хэшируем пароль
	hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

	# Создаем объект пользователя
	user = User(db, id=message.from_user.id, name=message.from_user.full_name,
	            username=message.from_user.username, password=hashed_password, role='user')

	# Проверяем, есть ли пользователь с таким ID в базе данных
	existing_user = user.login(message.from_user.id, password)
	if isinstance(existing_user, User):
		await message.answer("Вы уже зарегистрированы. Можете начать обучение.\n"
		                     "Выберите действие:", reply_markup=start_keyboards.get_main_menu_keyboard())
		await state.finish()
		return
	elif existing_user == 1:
		await message.answer("Неверный пароль, пожалуйста, введите ещё раз: ")
		return


	# Регистрируем пользователя
	user.register()

	# Завершаем регистрацию
	await state.finish()
	await message.answer("Регистрация завершена. Спасибо!")


# @dp.callback_query_handler(text='login')
async def process_login(callback_query: types.CallbackQuery):
	await callback_query.answer()

	# Отправляем сообщение с запросом ввода пароля
	await callback_query.message.edit_text("Введите пароль:")

	# Устанавливаем состояние "Ожидание пароля"
	await RegistrationState.Password.set()
