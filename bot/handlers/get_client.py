from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from data import Text, ButtonText
from keyboards import cancel, menu
from loader import dp, logger
from shell_interface import get_clients_from_manager, get_config_qrcode, put_bytes_to_file, get_config_raw, \
    delete_client, raw_to_html
from states import GetClient


def gen_pages(lst):
    res = []
    page = 0
    while 1:
        res.append([])
        for i in range(4):
            try:
                res[page].append(lst[i + page * 4])
            except IndexError:
                if not res[-1]:
                    res.pop(-1)
                return res
        page += 1


@dp.callback_query_handler(text="cancel", state=GetClient)
async def cancel_order(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(Text.MENU, reply_markup=menu)
    await call.answer()
    await state.finish()


@dp.callback_query_handler(text_contains="clients")
async def get_client(call: CallbackQuery, state: FSMContext):
    clients = get_clients_from_manager()

    choice = InlineKeyboardMarkup()
    for client_name in clients:
        choice.insert(InlineKeyboardButton(text=client_name, callback_data=f'client:{client_name}'))
    choice.insert(cancel)

    await call.message.edit_text(Text.CLIENTS, reply_markup=choice)
    await call.answer()
    await GetClient.name.set()


@dp.callback_query_handler(state=GetClient.name)
async def get_client_2(call: CallbackQuery, state: FSMContext):
    client_name = call.data.split(':')[1]

    get_client_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=ButtonText.GET_QR, callback_data=f'get_qrcode:{client_name}'),
                InlineKeyboardButton(text=ButtonText.GET_FILE, callback_data=f'get_file:{client_name}'),
            ],
            [
                InlineKeyboardButton(text=ButtonText.GET_RAW, callback_data=f"get_raw:{client_name}"),
            ],
            [
                InlineKeyboardButton(text=ButtonText.DELETE, callback_data=f"delete:{client_name}"),
            ],
            [
                InlineKeyboardButton(text=ButtonText.BACK_MENU, callback_data="cancel")
            ]
        ]
    )

    await call.message.edit_text(Text.CLIENT.format(client_name=client_name), reply_markup=get_client_menu)
    await call.answer()

    await GetClient.next()


@dp.callback_query_handler(state=GetClient.choice)
async def get_client_3(call: CallbackQuery, state: FSMContext):
    command, client_name = call.data.split(":")

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
                    InlineKeyboardButton(text=ButtonText.BACK_MENU, callback_data="cancel")
                ],
            ]
        )
        await call.answer()
        await call.message.edit_text(Text.CLIENT_DELETE_CONFIRM.format(client_name=client_name), reply_markup=conf_del)
        await GetClient.next()


@dp.callback_query_handler(state=GetClient.del_confirm)
async def get_client_4(call: CallbackQuery, state: FSMContext):
    command, client_name = call.data.split(":")
    delete_client(client_name)
    await call.message.edit_text(Text.CLIENT_DELETED.format(client_name=client_name), reply_markup=menu)
    await call.answer()
    await state.finish()
    logger.info(f"deleted client \"{client_name}\" from user {call.from_user.username}:{call.from_user.id}")
