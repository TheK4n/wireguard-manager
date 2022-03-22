from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaDocument

from keyboards import cancel, menu
from loader import dp
from shell_interface import get_clients_from_manager, get_config_qrcode, put_bytes_to_file, get_config_raw, \
    delete_client
from states import GetClient


@dp.callback_query_handler(text="cancel", state=GetClient)
async def cancel_order(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('WireGuard Manager bot menu', reply_markup=menu)
    await call.answer()
    await state.finish()


@dp.callback_query_handler(text_contains="clients")
async def get_client(call: CallbackQuery, state: FSMContext):

    clients = get_clients_from_manager()

    choice = InlineKeyboardMarkup()
    for client_name in clients:
        choice.insert(InlineKeyboardButton(text=client_name, callback_data=f'client:{client_name}'))
    choice.insert(cancel)

    await call.message.edit_text('Clients', reply_markup=choice)
    await call.answer()
    await GetClient.name.set()


@dp.callback_query_handler(state=GetClient.name)
async def get_client_2(call: CallbackQuery, state: FSMContext):
    client_name = call.data.split(':')[1]

    get_client_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Get QR Code", callback_data=f'get_qrcode:{client_name}'),
                InlineKeyboardButton(text="Get File", callback_data=f'get_file:{client_name}'),
            ],
            [
                InlineKeyboardButton(text="Get Raw", callback_data=f"get_raw:{client_name}"),
            ],
            [
                InlineKeyboardButton(text="Delete", callback_data=f"delete:{client_name}"),
            ],
            [
                InlineKeyboardButton(text="<< Back to menu", callback_data="cancel")
            ]
        ]
    )

    await call.message.edit_text(f'Client "{client_name}"', reply_markup=get_client_menu)
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
    elif command == "get_file":
        document = put_bytes_to_file(get_config_raw(client_name))
        document.name = client_name + ".conf"
        await call.message.answer_document(document=document)
        await call.answer()
    elif command == "get_raw":
        await call.message.answer(get_config_raw(client_name).decode())
        await call.answer()
    elif command == "delete":
        if not delete_client(client_name).returncode:
            await call.message.answer("Client deleted", reply_markup=menu)
            await call.answer()
            await call.message.delete()
            await state.finish()


