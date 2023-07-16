from create_bot import dp, types, Dispatcher
from keyboards import get_start_keyboard
from handlers.registration_handlers import register_button_handler, process_password_handler, \
	RegistrationState, process_login
from handlers.course_handlers import create_course_handler, back_to_menu


async def set_default_commands(dp, chat_id: int):
	await dp.bot.set_my_commands([
		types.BotCommand('start', 'Начать сначала'),
		types.BotCommand('help', 'Справка о боте'),
	], scope=types.BotCommandScopeChat(chat_id), language_code='ru')


# @dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
	await set_default_commands(dp, message.chat.id)
	await message.answer("Здравствуй! Я бот для обучения. 🤖📚\n"
	                     "Чтобы продолжить, выберите действие, которое вас интересует: 🎯",
	                     reply_markup=get_start_keyboard())


# @dp.message_handler(commands='start')
async def catalog(message: types.Message):
	await message.answer("На данный момент",
	                     reply_markup=get_start_keyboard())


def register_start_handlers(dp: Dispatcher):
	dp.register_message_handler(catalog, commands='catalog')
	dp.register_message_handler(cmd_start, commands='start')
	dp.register_callback_query_handler(register_button_handler, text='register')
	dp.register_message_handler(process_password_handler, state=RegistrationState.Password)
	dp.register_callback_query_handler(process_login, text='login')
	dp.register_callback_query_handler(create_course_handler, text='create_course', state='*')
	dp.register_callback_query_handler(create_course_handler, text='create_course', state='*')
	dp.register_callback_query_handler(back_to_menu, text='back_to_menu', state='*')
