from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .userDb import *
import traceback
from texts import *
from .fsub import *
# 04427417047
@Client.on_message(filters.command("start") & filters.incoming & filters.private)
async def startBot(client, message):
    userId = message.from_user.id
    userName = message.from_user.first_name
    btn = [
        [
            InlineKeyboardButton(
                "Join Contest",
                callback_data=f"join#{userId}",
            )
        ],
        [
            InlineKeyboardButton(
                "Your Points",
                callback_data=f"point#{userId}",
            )
        ],
        [
            InlineKeyboardButton(
                "Leader Board",
                callback_data=f"lead#{userId}",
            )
        ],
    ]
    try:
        isStarted = await startedUser.find_one({"userId": userId})
        if isStarted:
            joined = await chnl_force_sub(client, message)
            if joined:
                await message.reply_text(
                    text=START_TXT, reply_markup=InlineKeyboardMarkup(btn)
                )
            else:
                return
        else:
            try:
                data = message.command[1]
                if data and data.split("-", 1)[0] == "SafeETF":
                    Fullref = data.split("-", 1)
                    refUserId = int(Fullref[1])
                    newPoint = await updatePoint(refUserId)
                    await startUser(userId, userName)
                    joined = await chnl_force_sub(client, message)
                    if joined:
                        await message.reply_text(
                            text=START_TXT, reply_markup=InlineKeyboardMarkup(btn)
                        )
                    await client.send_message(
                        refUserId,
                        f"{message.from_user.mention()} started your bot from your referral link.\nYour Current point is {newPoint}",
                    )
                else:
                    joined = await chnl_force_sub(client, message)
                    if joined:
                        await message.reply_text(
                            text=START_TXT, reply_markup=InlineKeyboardMarkup(btn)
                        )
                    else:
                        return
                    await startUser(userId, userName)
            except IndexError:
                await startUser(userId, userName)
                await message.reply_text(
                    text=START_TXT,
                    reply_markup=InlineKeyboardMarkup(btn),
                )
            except Exception as err:
                traceback.print_exc()
    except Exception:
        traceback.print_exc()


@Client.on_message(filters.command("stats") & filters.incoming & filters.user(ADMIN))
async def stats(_, message):
    msg = await message.reply("Wait...")
    totalUser = await startedUser.count_documents({})
    leadUsers = startedUser.find().sort("point", -1)
    userToShow = "\n\n"
    async for doc in leadUsers:
        userToShow += f"Name : {doc['userName']},  ID : {doc['userId']}, Point : {doc['point']} , Wallet : {doc['wallet']}\n"
    with open("stats.txt", "w", encoding="utf-8") as f:
        f.write(f"Total Users : {totalUser}  {userToShow}")
    await message.reply_document("stats.txt", caption=f"Total users : {totalUser}")
    return await msg.delete()


@Client.on_message(filters.command("wallet") & filters.incoming & filters.private)
async def walletSub(_, message):
    userId = message.from_user.id
    userName = message.from_user.first_name
    try:
        wallet = message.command[1]
        isStatred = await startedUser.find_one({"userId": userId})
        if isStatred:
            await startedUser.update_one(
                {"userId": userId}, {"$set": {"wallet": wallet}}
            )
        else:
            await startUser(userId, userName)
            await startedUser.update_one(
                {"userId": userId}, {"$set": {"wallet": wallet}}
            )
        return await message.reply(WAL_TXT.format(message.from_user.mention(), wallet))
    except IndexError:
        return await message.reply(EMPTY_WAL)
