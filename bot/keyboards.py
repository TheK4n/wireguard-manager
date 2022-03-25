from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data import ButtonText

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=ButtonText.ADD_CLIENT, callback_data='add_client'),
        ],
        [
            InlineKeyboardButton(text=ButtonText.ClIENTS, callback_data="clients"),
        ],

    ]
)
cancel = InlineKeyboardButton(text=ButtonText.BACK_MENU, callback_data="cancel")
cancel_inline = InlineKeyboardMarkup(row_width=2)
cancel_inline.insert(cancel)


