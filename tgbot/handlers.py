import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from tgbot.keyboards.inline import registration, tasks, what_change_task, status, status2, logout
from tgbot.states import Registration, Login, Tg_Id, Task, ChangeTask, ChangeTaskAll, \
    DeleteTask

API_URL = {'registration': "http://127.0.0.1:8000/registration/",
           'login': "http://127.0.0.1:8000/login/",
           'add_task': "http://127.0.0.1:8000/add_task/",
           'get_list': "http://127.0.0.1:8000/get_list/",
           'change_name': 'http://127.0.0.1:8000/change_name/',
           'change_description': 'http://127.0.0.1:8000/change_description/',
           'change_status': 'http://127.0.0.1:8000/change_status/',
           'change_all': 'http://127.0.0.1:8000/change_all/',
           'delete': 'http://127.0.0.1:8000/delete/'}

user = Router()


@user.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! 👋 Я бот‑органайзер. Помогу тебе записывать дела, управлять задачами и ничего не забывать",
        reply_markup=registration)


@user.callback_query(F.data == 'reg')
async def registration_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Пожалуйста, введите ваше имя 📝')
    await state.set_state(Registration.name)


@user.message(Registration.name)
async def registration_password(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите пароль 🔒 (он будет сохранён в базе):")
    await state.set_state(Registration.password)


@user.message(Registration.password)
async def process_registration(message: Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data['name']
    password = message.text
    tg_id = message.from_user.id

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL['registration'], json={
            'tg_id': tg_id,
            'name': name,
            'password': password,
        }) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res.get('success'):
                    user_id = res.get('user_id')
                    await message.answer("🎉 Вы успешно зарегистрировались! Ваши данные сохранены ✅", reply_markup=tasks)
                    await state.set_state(Tg_Id.authorized)
                    await state.update_data(tg_id=tg_id, authorized=True, user_id=user_id)
            else:
                await message.answer('⚠️ Произошла ошибка при регистрации. Пожалуйста, попробуйте ещё раз.')


@user.callback_query(F.data == 'login')
async def login_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите ваше имя для входа 👤')
    await state.clear()
    await state.set_state(Login.name)


@user.message(Login.name)
async def login_password(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите пароль 🔑:")
    await state.set_state(Login.password)


@user.message(Login.password)
async def process_login(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_name = user_data['name']
    password = message.text
    tg_id = message.from_user.id

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL['login'], json={
            'tg_id': tg_id,
            'name': user_name,
            'password': password
        }) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res.get('success'):
                    user_id = res.get('user_id')
                    await message.answer("🎉 Вы успешно вошли!", reply_markup=tasks)
                    await state.set_state(Tg_Id.authorized)
                    await state.update_data(tg_id=tg_id, authorized=True, user_id=user_id)
                    return
                else:
                    await message.answer("Неверное имя или пароль. Попробуйте снова.")
                    await message.answer('Введите имя ещё раз.')
            else:
                await message.answer("⚠️ Произошла ошибка при регистрации. Пожалуйста, попробуйте ещё раз.",
                                     reply_markup=registration)


@user.callback_query(F.data == 'add_task')
async def name_task(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get('authorized'):
        await callback.message.answer(
            "Пожалуйста, войдите в систему или зарегистрируйтесь, прежде чем добавлять задачи.",
            reply_markup=registration)
        return

    await callback.message.answer('📝 Введите название задачи, которую хотите добавить:')
    await state.set_state(Task.name)


@user.message(Task.name)
async def description_task(message: Message, state: FSMContext):
    await state.update_data(task_name=message.text)
    await message.answer('🖊️ Теперь введите описание задачи:')
    await state.set_state(Task.description)


@user.message(Task.description)
async def add_task(message: Message, state: FSMContext):
    data = await state.get_data()
    tg_id = message.from_user.id
    user_id = data.get('user_id')
    task_name = data.get('task_name')
    description = message.text

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL['add_task'], json={
            'name': task_name,
            'description': description,
            'user_id': user_id,
        }) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res.get('success'):
                    await message.answer('✅ Задача успешно добавлена! Отличная работа! 👍', reply_markup=tasks)

            else:
                await message.answer('⚠️ Произошла ошибка. Пожалуйста, попробуйте ещё раз.')
    await state.clear()
    await state.set_state(Tg_Id.authorized)
    await state.update_data(tg_id=tg_id, authorized=True, user_id=user_id)


@user.callback_query(F.data == 'show_list')
async def show_list(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tg_id = callback.from_user.id
    user_id = data.get('user_id')

    if user_id is None:
        await callback.message.answer("Пожалуйста, войдите или зарегистрируйтесь.")
        return

    if not data.get('authorized'):
        await callback.message.answer(
            "Пожалуйста, войдите в систему или зарегистрируйтесь, прежде чем добавлять задачи.",
            reply_markup=registration)
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL['get_list'], params={
            'user_id': user_id
        }) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res:
                    response_text = 'Ваши задачи \n'
                    for task in res:
                        if not task['is_completed']:
                            is_completed = 'Нет'
                        else:
                            is_completed = 'Да'
                        response_text += f"{task['task_number']}. {task['task_name']}: {task['description']}. Выполнено: {is_completed} \n"

                else:
                    response_text = 'У вас нет задач'
                await callback.message.answer(response_text, reply_markup=tasks)
            else:
                await callback.message.answer("⚠️ Ошибка при получении задач. Попробуйте ещё раз.")
    await state.clear()
    await state.set_state(Tg_Id.authorized)
    await state.update_data(tg_id=tg_id, authorized=True, user_id=user_id)


@user.callback_query(F.data == 'rewrite_task')
async def choose_task(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tg_id = callback.from_user.id
    user_id = data.get('user_id')
    if not data.get('authorized'):
        await callback.message.answer(
            "Пожалуйста, войдите в систему или зарегистрируйтесь, прежде чем добавлять задачи.",
            reply_markup=registration)
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL['get_list'], params={
            'user_id': user_id
        }) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res:
                    response_text = 'Ваши задачи \n'
                    for task in res:
                        if not task['is_completed']:
                            is_completed = 'Нет'
                        else:
                            is_completed = 'Да'
                        response_text += f"{task['task_number']}. {task['task_name']}: {task['description']}. Выполнено: {is_completed} \n"
                else:
                    response_text = 'У вас нет задач'
                await callback.message.answer(response_text)

            else:
                await callback.message.answer("Ошибка при получении задач. Попробуйте ещё раз.")

    await state.clear()
    await state.set_state(Tg_Id.authorized)
    await state.update_data(tg_id=tg_id, authorized=True, user_id=user_id)

    await callback.message.answer('📋 Напишите номер задачи, которую хотите изменить.')
    await state.set_state(ChangeTask.number)


@user.message(ChangeTask.number)
async def what_change(message: Message, state: FSMContext):
    await state.update_data(task_number=message.text)
    await message.answer('Что хотите изменить в задаче? 🔄', reply_markup=what_change_task)


@user.callback_query(F.data == 'change_name')
async def process_change_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('📝 Введите новое название задачи:')
    await state.set_state(ChangeTask.name)


@user.message(ChangeTask.name)
async def change_name(message: Message, state: FSMContext):
    data = await state.get_data()
    task_number = data.get('task_number')
    tg_id = message.from_user.id
    new_task_name = message.text
    user_id = data.get('user_id')

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL['change_name'], json={
            'tg_id': tg_id,
            'task_number': task_number,
            'new_task_name': new_task_name
        }) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res.get('success'):
                    await message.answer('✅ Название задачи успешно изменено!', reply_markup=tasks)

            else:
                await message.answer('❌ Вы не зарегистрированы или ввели неверный номер задачи!', reply_markup=tasks)

    await state.clear()
    await state.set_state(Tg_Id.authorized)
    await state.update_data(tg_id=tg_id, authorized=True, user_id=user_id)


@user.callback_query(F.data == 'change_description')
async def process_change_description(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('🖊️ Введите новое описание задачи:')
    await state.set_state(ChangeTask.description)


@user.message(ChangeTask.description)
async def change_description(message: Message, state: FSMContext):
    data = await state.get_data()
    task_number = data.get('task_number')
    tg_id = message.from_user.id
    new_task_description = message.text
    user_id = data.get('user_id')

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL['change_description'], json={
            'tg_id': tg_id,
            'task_number': task_number,
            'new_task_description': new_task_description
        }) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res.get('success'):
                    await message.answer('✅ Описание задачи успешно изменено!', reply_markup=tasks)

            else:
                await message.answer('Вы не зарегистрированы или ввели не верный номер задачи!', reply_markup=tasks)

    await state.clear()
    await state.set_state(Tg_Id.authorized)
    await state.update_data(tg_id=tg_id, authorized=True, user_id=user_id)


@user.callback_query(F.data == 'status')
async def process_change_is_completed(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('✅ Задание выполнено? Выберите:', reply_markup=status)


@user.callback_query(F.data == 'ready')
async def complete_or_not(callback: CallbackQuery, state: FSMContext):
    status = True
    data = await state.get_data()
    task_number = data.get('task_number')
    tg_id = callback.from_user.id
    user_id = data.get('user_id')

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL['change_status'], json={
            'tg_id': tg_id,
            'task_number': task_number,
            'status': status
        }) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res.get('success'):
                    await callback.message.answer('✅ Статус задачи успешно обновлён!', reply_markup=tasks)

            else:
                await callback.message.answer('❌ Вы не зарегистрированы или ввели неверный номер задачи!',
                                              reply_markup=tasks)

    await state.clear()
    await state.set_state(Tg_Id.authorized)
    await state.update_data(tg_id=tg_id, authorized=True, user_id=user_id)


@user.callback_query(F.data == 'not_ready')
async def complete_or_not(callback: CallbackQuery, state: FSMContext):
    status = False
    data = await state.get_data()
    task_number = data.get('task_number')
    tg_id = callback.from_user.id
    user_id = data.get('user_id')

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL['change_status'], json={
            'tg_id': tg_id,
            'task_number': task_number,
            'status': status
        }) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res.get('success'):
                    await callback.message.answer('✅ Статус задачи успешно обновлён!', reply_markup=tasks)

            else:
                await callback.message.answer('❌ Вы не зарегистрированы или ввели неверный номер задачи!',
                                              reply_markup=tasks)

    await state.clear()
    await state.set_state(Tg_Id.authorized)
    await state.update_data(tg_id=tg_id, authorized=True, user_id=user_id)


@user.callback_query(F.data == 'change_all')
async def process_change_all_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('📝 Введите новое название задания:')
    await state.set_state(ChangeTaskAll.name)


@user.message(ChangeTaskAll.name)
async def process_change_all_description(message: Message, state: FSMContext):
    await state.update_data(all_new_name=message.text)
    await message.answer('🖊️ Теперь введите новое описание задания:')
    await state.set_state(ChangeTaskAll.description)


@user.message(ChangeTaskAll.description)
async def process_change_all_status(message: Message, state: FSMContext):
    await state.update_data(all_new_description=message.text)
    await message.answer('✅ Задание выполнено? Выберите:', reply_markup=status2)


@user.callback_query(F.data == 'ready2')
async def change_full_task(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tg_id = callback.from_user.id
    task_number = data.get('task_number')
    task_name_new = data.get('all_new_name')
    task_description_new = data.get('all_new_description')
    new_status = True
    user_id = data.get('user_id')

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL['change_all'], json={
            'tg_id': tg_id,
            'task_number': task_number,
            'new_task_name': task_name_new,
            'new_task_description': task_description_new,
            'status': new_status
        }) as resp:

            if resp.status == 200:
                res = await resp.json()
                if res.get('success'):
                    await callback.message.answer('🎉 Вы успешно изменили задачу!')

            else:
                await callback.message.answer('Вы не зарегистрированы или ввели не верный номер задачи!',
                                              reply_markup=tasks)

    await state.clear()
    await state.set_state(Tg_Id.authorized)
    await state.update_data(tg_id=tg_id, authorized=True, user_id=user_id)

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL['get_list'], params={
            'user_id': user_id
        }) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res:
                    response_text = 'Новый обновлённый список задач: \n'
                    for task in res:
                        if not task['is_completed']:
                            is_completed = 'Нет'
                        else:
                            is_completed = 'Да'
                        response_text += f"{task['task_number']}. {task['task_name']}: {task['description']}. Выполнено: {is_completed} \n"
                else:
                    response_text = 'У вас нет задач'
                await callback.message.answer(response_text, reply_markup=tasks)
            else:
                await callback.message.answer("Ошибка при получении задач. Попробуйте ещё раз.")


@user.callback_query(F.data == 'not_ready2')
async def change_full_task(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tg_id = callback.from_user.id
    task_number = data.get('task_number')
    task_name_new = data.get('all_new_name')
    task_description_new = data.get('all_new_description')
    new_status = False
    user_id = data.get('user_id')

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL['change_all'], json={
            'tg_id': tg_id,
            'task_number': task_number,
            'new_task_name': task_name_new,
            'new_task_description': task_description_new,
            'status': new_status
        }) as resp:

            if resp.status == 200:
                res = await resp.json()
                if res.get('success'):
                    await callback.message.answer('🎉 Вы успешно изменили задачу!')

            else:
                await callback.message.answer('Вы не зарегистрированы или ввели не верный номер задачи!',
                                              reply_markup=tasks)

    await state.clear()
    await state.set_state(Tg_Id.authorized)
    await state.update_data(tg_id=tg_id, authorized=True, user_id=user_id)

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL['get_list'], params={
            'user_id': user_id
        }) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res:
                    response_text = 'Новый обновлённый список задач: \n'
                    for task in res:
                        if not task['is_completed']:
                            is_completed = 'Нет'
                        else:
                            is_completed = 'Да'
                        response_text += f"{task['task_number']}. {task['task_name']}: {task['description']}. Выполнено: {is_completed} \n"
                else:
                    response_text = 'У вас нет задач'
                await callback.message.answer(response_text, reply_markup=tasks)
            else:
                await callback.message.answer("Ошибка при получении задач. Попробуйте ещё раз.")


@user.callback_query(F.data == 'delete_task')
async def show_delete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tg_id = callback.from_user.id
    user_id = data.get('user_id')
    if not data.get('authorized'):
        await callback.message.answer(
            "Пожалуйста, войдите в систему или зарегистрируйтесь, прежде чем добавлять задачи.",
            reply_markup=registration)
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL['get_list'], params={
            'user_id': user_id
        }) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res:
                    response_text = 'Ваш список задач: \n'
                    for task in res:
                        if not task['is_completed']:
                            is_completed = 'Нет'
                        else:
                            is_completed = 'Да'
                        response_text += f"{task['task_number']}. {task['task_name']}: {task['description']}. Выполнено: {is_completed} \n"
                else:
                    response_text = 'У вас нет задач'
                await callback.message.answer(response_text)
            else:
                await callback.message.answer("Ошибка при получении задач. Попробуйте ещё раз.")

    await callback.message.answer('📋 Введите номер задачи, которую хотите удалить:')
    await state.set_state(DeleteTask.number)


@user.message(DeleteTask.number)
async def delete_start(message: Message, state: FSMContext):
    data = await state.get_data()
    tg_id = message.from_user.id
    task_number = message.text
    user_id = data.get('user_id')

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL['delete'], json={
            'tg_id': tg_id,
            'task_number': task_number
        }) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res.get('success'):
                    await message.answer('✅ Задача успешно удалена!', reply_markup=tasks)
                else:
                    await message.answer('❌ Задача с таким номером не найдена!')
            else:
                await message.answer('⚠️ Произошла ошибка при удалении. Пожалуйста, попробуйте ещё раз.')
    await state.clear()
    await state.set_state(Tg_Id.authorized)
    await state.update_data(tg_id=tg_id, authorized=True, user_id=user_id)


@user.message(Command("menu"))
async def show_menu(message: Message):
    await message.answer("📋 Выберите действие:", reply_markup=tasks)


@user.message(Command("logout"))
async def process_logout(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Вы действительно хотите выйти из профиля? 🚪", reply_markup=logout)


@user.callback_query(F.data == 'logout_yes')
async def logout_true(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Вы вышли из профиля. Для входа используйте /start 👋")


@user.callback_query(F.data == 'logout_no')
async def logout_true(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Вы остались в профиле 😊", reply_markup=tasks)
