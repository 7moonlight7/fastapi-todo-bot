from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

registration = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📝 Регистрация', callback_data='reg'),
     InlineKeyboardButton(text='🔐 Вход', callback_data='login')]
])

tasks = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='➕ Добавить задачу', callback_data='add_task'),
     InlineKeyboardButton(text='✏️ Изменить задачу', callback_data='rewrite_task')],
    [InlineKeyboardButton(text='🗑️ Удалить задачу', callback_data='delete_task'),
     InlineKeyboardButton(text='📄 Просмотреть список', callback_data='show_list')]
])

what_change_task = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📝 Название', callback_data='change_name'),
     InlineKeyboardButton(text='🖊️ Описание', callback_data='change_description')],
    [InlineKeyboardButton(text='✅ Статус', callback_data='status'),
     InlineKeyboardButton(text='🔄 Всё сразу', callback_data='change_all')]
])

status = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✔️ Да', callback_data='ready'),
     InlineKeyboardButton(text='❌ Нет', callback_data='not_ready')]
])

status2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✔️ Да', callback_data='ready2'),
     InlineKeyboardButton(text='❌ Нет', callback_data='not_ready2')]
])

logout = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Да, выйти', callback_data='logout_yes'),
     InlineKeyboardButton(text='↩️ Нет, остаться', callback_data='logout_no')]
])
