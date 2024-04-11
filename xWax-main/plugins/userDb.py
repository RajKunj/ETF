import motor.motor_asyncio
from info import DB_URL
client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
db = client['refUserDb']
startedUser = db['startedUser']
async def startUser(userId , userName):
    doc = {
        'userId' : userId,
        'userName' :userName,
        'point' : 0,
        'wallet': None,
        'notClaimed' : True}
    await startedUser.insert_one(doc)
async def updatePoint(userId):
    user = await startedUser.find_one({'userId'  : userId})
    point = int(user['point'])
    newPoint = point +  130
    await startedUser.update_one({'userId' : userId} ,{ '$set':{'point': newPoint }})
    return newPoint
class temp(object):
    U_NAME = None