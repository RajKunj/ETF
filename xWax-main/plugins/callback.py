from pyrogram import Client, enums
from .userDb import *
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from texts import *
from info import *

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicker = int(query.data.split("#")[1])
    data = query.data.split("#")[0]

    if clicker not in [query.from_user.id, 0]:
        return await query.answer(
            f"Hey {query.from_user.first_name}, Jaldi Yeha Se Hato", show_alert=True
        )
    if data == "home":
        reply_markup = [
            [InlineKeyboardButton("Join Contest", callback_data=f"join#{clicker}")],
            [InlineKeyboardButton("Your Points", callback_data=f"point#{clicker}")],
            [InlineKeyboardButton("Leader Board", callback_data=f"lead#{clicker}")],
        ]
        await query.message.edit_text(
            text=START_TXT,
            reply_markup=InlineKeyboardMarkup(reply_markup),
            parse_mode=enums.ParseMode.HTML,
        )

    elif data == "join":
        isClaimed = await startedUser.find_one({"userId": clicker})
        if isClaimed["notClaimed"]:
            await updatePoint(clicker)
            await startedUser.find_one_and_update(
                {"userId": clicker}, {"$set": {"notClaimed": False}}
            )
            await query.message.reply(CONGRATS)
        await query.message.edit(
            REF_LINK.format(temp.U_NAME, clicker),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data=f"home#{clicker}")]]
            ),
        )

    elif data == "lead":
        btn = [
            [
                InlineKeyboardButton(text="Rank", callback_data=f"g#{clicker}"),
                InlineKeyboardButton(text="Name", callback_data=f"g#{clicker}"),
                InlineKeyboardButton(text="Points", callback_data=f"g#{clicker}"),
            ],
        ]
        leadUsers = startedUser.find().sort("point", -1).limit(LIMIT)
        index = 1
        async for doc in leadUsers:
            btn.append(
                [
                    InlineKeyboardButton(text=index, callback_data=f"g#{clicker}"),
                    InlineKeyboardButton(
                        text=doc["userName"], callback_data=f"g#{clicker}"
                    ),
                    InlineKeyboardButton(
                        text=doc["point"], callback_data=f"g#{clicker}"
                    ),
                ]
            )
            index += 1
        btn.append(
            [
                InlineKeyboardButton(text="Back", callback_data=f"home#{clicker}"),
            ]
        )
        await query.message.edit(
            text=LEAD_TXT.format(LIMIT), reply_markup=InlineKeyboardMarkup(btn)
        )

    elif data == "g":
        return await query.answer("Jai shree Krishna..", show_alert=True)

    elif data == "point":
        user = await startedUser.find_one({"userId": clicker})
        return await query.message.edit(
            f'Your Current Point is : {user["point"]}',
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Back", callback_data=f"home#{clicker}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Your Ref Link", callback_data=f"join#{clicker}"
                        )
                    ],
                ]
            ),
        )
