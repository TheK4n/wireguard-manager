from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup

from data import Text, ReturnCodes
from keyboards import cancel, menu
from loader import dp, logger
from shell_interface import add_client, put_bytes_to_file
from states import AddClient


@dp.callback_query_handler(text="cancel", state=AddClient)
async def cancel_order(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(Text.MENU, reply_markup=menu)
    await call.answer()
    await state.finish()


@dp.callback_query_handler(text_contains="add_client")
async def get_client(call: CallbackQuery, state: FSMContext):

    cancel_menu = InlineKeyboardMarkup()
    cancel_menu.insert(cancel)
    await call.message.edit_text(Text.ASK_NAME, reply_markup=cancel_menu)
    await call.answer()

    await AddClient.name.set()


@dp.message_handler(state=AddClient.name)
async def get_client_2(message: Message, state: FSMContext):
    client_name = message.text
    command_result = add_client(client_name)

    if command_result.returncode:
        if command_result.returncode == ReturnCodes.SystemFail:
            await message.answer(Text.ERROR_1)
        elif command_result.returncode == ReturnCodes.ValidationError:
            await message.answer(Text.ERROR_11)
        elif command_result.returncode == ReturnCodes.PeerAlreadyExists:
            await message.answer(Text.ERROR_12.format(client_name=client_name))
        elif command_result.returncode == ReturnCodes.SubnetError:
            await message.answer(Text.ERROR_24)
        logger.error(f"adding client {message.text} from user {message.from_user.username}:{message.from_user.id}")
    else:
        photo = put_bytes_to_file(command_result.stdout)
        await message.reply(Text.CLIENT_ADDED.format(client_name=client_name))
        await message.answer_photo(photo=photo)
        logger.info(f"added client {message.text} from user {message.from_user.username}:{message.from_user.id}")

    await message.answer(Text.MENU, reply_markup=menu)
    await state.finish()
