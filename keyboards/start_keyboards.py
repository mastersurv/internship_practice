from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_keyboard():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(
		InlineKeyboardButton("Войти", callback_data="login"),
		InlineKeyboardButton("Зарегистрироваться", callback_data="register")
	)
	return keyboard


def get_main_menu_keyboard():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(
		InlineKeyboardButton("Каталог курсов", callback_data="course_catalog"),
		InlineKeyboardButton("Создание курса", callback_data="create_course")
	)
	return keyboard


def get_back_to_main_menu_keyboard():
	keyboard = InlineKeyboardMarkup(row_width=2)
	keyboard.add(
		InlineKeyboardButton("Вернуться в меню", callback_data="back_to_menu"),
	)
	return keyboard
