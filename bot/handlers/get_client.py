import math
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from data import Text, ButtonText
from keyboards import cancel, menu
from loader import dp, logger
from shell_interface import get_clients_from_manager, get_config_qrcode, put_bytes_to_file, get_config_raw, \
    delete_client, raw_to_html
from states import GetClient


NUMBER_OF_CLIENTS_ON_PAGE = 6


def get_clients_with_offset_fill_blank_clients(clients, page: int):
    offset = NUMBER_OF_CLIENTS_ON_PAGE * page

    res = clients[offset:(NUMBER_OF_CLIENTS_ON_PAGE + offset)]

    for _ in range(NUMBER_OF_CLIENTS_ON_PAGE - len(res)):
        res.append(" "  * 20)
    return res


@dp.callback_query_handler(text_contains="cancel", state=GetClient)
async def cancel_order(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(Text.MENU, reply_markup=menu)
    await call.answer()
    await state.finish()


@dp.callback_query_handler(text_contains="cancel")
async def cancel_order2(call: CallbackQuery):
    await call.message.edit_text(Text.MENU, reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(text="_")
async def plug(call: CallbackQuery):
    await call.answer()


@dp.callback_query_handler(text_contains="clients")
async def get_client(call: CallbackQuery, state: FSMContext):
    page = int(call.data.split(":")[1])

    all_clients = get_clients_from_manager()

    total_pages = math.ceil(len(all_clients) / NUMBER_OF_CLIENTS_ON_PAGE)

    if page >= total_pages:
        page = 0

    if page < 0:
        page = total_pages - 1

    clients = get_clients_with_offset_fill_blank_clients(all_clients, page)

    clients_keyboard = InlineKeyboardMarkup()
    for client_name in clients:
        if client_name == " " * 20:
            clients_keyboard.insert(InlineKeyboardButton(text=client_name, callback_data=f'_'))
        else:
            clients_keyboard.insert(InlineKeyboardButton(text=client_name, callback_data=f'client_name:{client_name}:{page}'))

    prev_page_button = InlineKeyboardButton(text="<", callback_data=f"clients:{page - 1}")
    current_page_button = InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data="_")
    next_page_button = InlineKeyboardButton(text=">", callback_data=f"clients:{page + 1}")

    clients_keyboard.row(prev_page_button, current_page_button, next_page_button)
    clients_keyboard.row(cancel)

    await call.message.edit_text(Text.CLIENTS, reply_markup=clients_keyboard)
    await call.answer()


@dp.callback_query_handler(text_contains="client_name")
async def get_client_2(call: CallbackQuery, state: FSMContext):
    client_name = call.data.split(':')[1]
    page = call.data.split(':')[2]

    get_client_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=ButtonText.GET_QR, callback_data=f'get_client_get_name:get_qrcode:{client_name}'),
                InlineKeyboardButton(text=ButtonText.GET_FILE, callback_data=f'get_client_get_name:get_file:{client_name}'),
            ],
            [
                InlineKeyboardButton(text=ButtonText.GET_RAW, callback_data=f"get_client_get_name:get_raw:{client_name}"),
            ],
            [
                InlineKeyboardButton(text=ButtonText.DELETE, callback_data=f"get_client_get_name:delete:{client_name}"),
            ],
            [
                InlineKeyboardButton(text=ButtonText.BACK_MENU, callback_data=f"clients:{page}")
            ]
        ]
    )

    await call.message.edit_text(Text.CLIENT.format(client_name=client_name), reply_markup=get_client_menu)
    await call.answer()


@dp.callback_query_handler(text_contains="get_client_get_name")
async def get_client_3(call: CallbackQuery, state: FSMContext):
    _, command, client_name = call.data.split(":")

    if command == "get_qrcode":
        photo = put_bytes_to_file(get_config_qrcode(client_name))
        photo.name = client_name + ".png"
        await call.message.answer_photo(photo=photo)
        await call.answer()
        logger.info(f"get qrcode \"{client_name}\" from user {call.from_user.username}:{call.from_user.id}")
    elif command == "get_file":
        document = put_bytes_to_file(get_config_raw(client_name))
        document.name = client_name + ".conf"
        await call.message.answer_document(document=document)
        await call.answer()
        logger.info(f"get file \"{client_name}\" from user {call.from_user.username}:{call.from_user.id}")
    elif command == "get_raw":
        await call.message.answer(raw_to_html(get_config_raw(client_name).decode()), parse_mode="html")
        await call.answer()
        logger.info(f"get raw \"{client_name}\" from user {call.from_user.username}:{call.from_user.id}")
    elif command == "delete":
        conf_del = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=ButtonText.CONFIRM, callback_data=f"confirm:{client_name}")
                ],
                [
                    InlineKeyboardButton(text=ButtonText.BACK_MENU, callback_data="cancel:_")
                ],
            ]
        )
        await call.answer()
        await call.message.edit_text(Text.CLIENT_DELETE_CONFIRM.format(client_name=client_name), reply_markup=conf_del)
        await GetClient.name.set()


@dp.callback_query_handler(state=GetClient.name)
async def get_client_4(call: CallbackQuery, state: FSMContext):
    _, client_name = call.data.split(":")
    delete_client(client_name)
    await call.message.edit_text(Text.CLIENT_DELETED.format(client_name=client_name), reply_markup=menu)
    await call.answer()
    await state.finish()
    logger.info(f"deleted client \"{client_name}\" from user {call.from_user.username}:{call.from_user.id}")
