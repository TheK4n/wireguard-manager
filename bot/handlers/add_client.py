from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup

from keyboards import cancel, menu
from loader import dp
from shell_interface import add_client, put_bytes_to_file
from states import AddClient


@dp.callback_query_handler(text="cancel", state=AddClient)
async def cancel_order(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('WireGuard Manager bot menu', reply_markup=menu)
    await call.answer()
    await state.finish()


@dp.callback_query_handler(text_contains="add_client")
async def get_client(call: CallbackQuery, state: FSMContext):

    cancel_menu = InlineKeyboardMarkup()
    cancel_menu.insert(cancel)
    await call.message.edit_text('Send me a name for a new client', reply_markup=cancel_menu)
    await call.answer()

    await AddClient.name.set()


@dp.message_handler(state=AddClient.name)
async def get_client_2(message: Message, state: FSMContext):
    client_name = message.text
    command_result = add_client(client_name)

    if command_result.returncode:
        await message.answer("Error")
    else:
        photo = put_bytes_to_file(command_result.stdout)
        await message.answer(f"Client \"{client_name}\" was added, here his QR code")
        await message.answer_photo(photo=photo)

    await message.answer("WireGuard Manager bot menu", reply_markup=menu)
    await state.finish()
