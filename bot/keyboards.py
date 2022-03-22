from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Add client", callback_data='add_client'),
        ],
        [
            InlineKeyboardButton(text="Clients", callback_data="clients"),
        ],

    ]
)
cancel = InlineKeyboardButton(text="<< Back to menu", callback_data="cancel")
cancel_inline = InlineKeyboardMarkup(row_width=2)
cancel_inline.insert(cancel)


