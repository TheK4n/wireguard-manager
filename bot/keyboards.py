from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data import MESSAGES

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=MESSAGES["ADD_CLIENT"], callback_data='add_client'),
        ],
        [
            InlineKeyboardButton(text=MESSAGES["CLIENTS"], callback_data="clients"),
        ],

    ]
)
cancel = InlineKeyboardButton(text=MESSAGES["BACK_MENU"], callback_data="cancel")
cancel_inline = InlineKeyboardMarkup(row_width=2)
cancel_inline.insert(cancel)


