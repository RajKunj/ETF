from pyrogram import Client
from info import *
from plugins.userDb import temp

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="ref_Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,)
    async def start(self):
        global bot_uName
        await super().start()
        me = await self.get_me()
        temp.U_NAME = me.username
        print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")
        await self.send_message(ADMIN, f"**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")

if __name__ == '__main__':
    Bot().run()