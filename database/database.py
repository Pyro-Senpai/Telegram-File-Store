# =====================================================================================##
#
#  ██╗░░██╗███╗░░██╗██████╗░░█████╗░████████╗███████╗██████╗░
#  ██║░░██║████╗░██║██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
#  ██║░░██║██╔██╗██║██████╔╝███████║░░░██║░░░█████╗░░██║░░██║
#  ██║░░██║██║╚████║██╔══██╗██╔══██║░░░██║░░░██╔══╝░░██║░░██║
#  ╚██████╔╝██║░╚███║██║░░██║██║░░██║░░░██║░░░███████╗██████╔╝
#  ░╚═════╝░╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═════╝░
#
#  ░██████╗░██████╗░██████╗░███████╗██████╗░
#  ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗
#  ██║░░░░░██║░░░██║██║░░██║█████╗░░██████╔╝
#  ██║░░░░░██║░░░██║██║░░██║██╔══╝░░██╔══██╗
#  ╚██████╗╚██████╔╝██████╔╝███████╗██║░░██║
#  ░╚═════╝░╚═════╝░╚═════╝░╚══════╝╚═╝░░╚═╝
#
#                         ✨ MADE BY UNRATED CODER ✨
#                  Join Updates Channel: https://t.me/UNRATED_CODER
#=====================================================================================##

import motor, asyncio
import motor.motor_asyncio
import time
import pymongo, os
from config import DB_URI, DB_NAME
from bot import Bot
import logging
from datetime import datetime, timedelta
from functools import wraps

try:
    dbclient = pymongo.MongoClient(DB_URI) if DB_URI else None
    database = dbclient[DB_NAME] if dbclient and DB_NAME else None
except Exception as e:
    logging.error(f"Error connecting to Pymongo: {e}")
    dbclient = None
    database = None

logging.basicConfig(level=logging.INFO)

def connection_check(default_return=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            if self.database is None:
                logging.error(f"Database not connected. Failed to execute {func.__name__}")
                return default_return
            try:
                return await func(self, *args, **kwargs)
            except Exception as e:
                logging.error(f"Error in {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator

class Rohit:

    def __init__(self, DB_URI, DB_NAME):
        try:
            self.dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI) if DB_URI else None
            self.database = self.dbclient[DB_NAME] if self.dbclient and DB_NAME else None
        except Exception as e:
            logging.error(f"Error connecting to Motor: {e}")
            self.dbclient = None
            self.database = None

        if self.database is not None:
            self.channel_data = self.database['channels']
            self.admins_data = self.database['admins']
            self.user_data = self.database['users']
            self.banned_user_data = self.database['banned_user']
            self.autho_user_data = self.database['autho_user']
            self.del_timer_data = self.database['del_timer']
            self.fsub_data = self.database['fsub']
            self.rqst_fsub_data = self.database['request_forcesub']
            self.rqst_fsub_Channel_data = self.database['request_forcesub_channel']
        else:
            self.channel_data = None
            self.admins_data = None
            self.user_data = None
            self.banned_user_data = None
            self.autho_user_data = None
            self.del_timer_data = None
            self.fsub_data = None
            self.rqst_fsub_data = None
            self.rqst_fsub_Channel_data = None


    @connection_check(default_return=False)
    async def present_user(self, user_id: int):
        found = await self.user_data.find_one({'_id': user_id})
        return bool(found)

    @connection_check(default_return=False)
    async def add_user(self, user_id: int):
        await self.user_data.insert_one({'_id': user_id})
        return True

    @connection_check(default_return=[])
    async def full_userbase(self):
        user_docs = await self.user_data.find().to_list(length=None)
        user_ids = [doc['_id'] for doc in user_docs]
        return user_ids

    @connection_check(default_return=False)
    async def del_user(self, user_id: int):
        await self.user_data.delete_one({'_id': user_id})
        return True


    @connection_check(default_return=False)
    async def admin_exist(self, admin_id: int):
        found = await self.admins_data.find_one({'_id': admin_id})
        return bool(found)

    @connection_check(default_return=False)
    async def add_admin(self, admin_id: int):
        if not await self.admin_exist(admin_id):
            await self.admins_data.insert_one({'_id': admin_id})
        return True

    @connection_check(default_return=False)
    async def del_admin(self, admin_id: int):
        if await self.admin_exist(admin_id):
            await self.admins_data.delete_one({'_id': admin_id})
        return True

    @connection_check(default_return=[])
    async def get_all_admins(self):
        users_docs = await self.admins_data.find().to_list(length=None)
        user_ids = [doc['_id'] for doc in users_docs]
        return user_ids


    @connection_check(default_return=False)
    async def ban_user_exist(self, user_id: int):
        found = await self.banned_user_data.find_one({'_id': user_id})
        return bool(found)

    @connection_check(default_return=False)
    async def add_ban_user(self, user_id: int):
        if not await self.ban_user_exist(user_id):
            await self.banned_user_data.insert_one({'_id': user_id})
        return True

    @connection_check(default_return=False)
    async def del_ban_user(self, user_id: int):
        if await self.ban_user_exist(user_id):
            await self.banned_user_data.delete_one({'_id': user_id})
        return True

    @connection_check(default_return=[])
    async def get_ban_users(self):
        users_docs = await self.banned_user_data.find().to_list(length=None)
        user_ids = [doc['_id'] for doc in users_docs]
        return user_ids



    @connection_check(default_return=False)
    async def set_del_timer(self, value: int):        
        existing = await self.del_timer_data.find_one({})
        if existing:
            await self.del_timer_data.update_one({}, {'$set': {'value': value}})
        else:
            await self.del_timer_data.insert_one({'value': value})
        return True

    @connection_check(default_return=0)
    async def get_del_timer(self):
        data = await self.del_timer_data.find_one({})
        if data:
            return data.get('value', 600)
        return 0


    @connection_check(default_return=False)
    async def channel_exist(self, channel_id: int):
        found = await self.fsub_data.find_one({'_id': channel_id})
        return bool(found)

    @connection_check(default_return=False)
    async def add_channel(self, channel_id: int):
        if not await self.channel_exist(channel_id):
            await self.fsub_data.insert_one({'_id': channel_id})
        return True

    @connection_check(default_return=False)
    async def rem_channel(self, channel_id: int):
        if await self.channel_exist(channel_id):
            await self.fsub_data.delete_one({'_id': channel_id})
        return True

    async def del_channel(self, channel_id: int):
        return await self.rem_channel(channel_id)

    @connection_check(default_return=[])
    async def show_channels(self):
        channel_docs = await self.fsub_data.find().to_list(length=None)
        channel_ids = [doc['_id'] for doc in channel_docs]
        return channel_ids

    
    @connection_check(default_return="off")
    async def get_channel_mode(self, channel_id: int):
        data = await self.fsub_data.find_one({'_id': channel_id})
        return data.get("mode", "off") if data else "off"

    @connection_check(default_return=False)
    async def set_channel_mode(self, channel_id: int, mode: str):
        await self.fsub_data.update_one(
            {'_id': int(channel_id)},
            {'$set': {'mode': mode}},
            upsert=True
        )
        return True


    @connection_check(default_return=False)
    async def req_user(self, channel_id: int, user_id: int):
        await self.rqst_fsub_Channel_data.update_one(
            {'_id': int(channel_id)},
            {'$addToSet': {'user_ids': int(user_id)}},
            upsert=True
        )
        return True


    @connection_check(default_return=False)
    async def del_req_user(self, channel_id: int, user_id: int):
        await self.rqst_fsub_Channel_data.update_one(
            {'_id': int(channel_id)},
            {'$pull': {'user_ids': int(user_id)}}
        )
        return True

    @connection_check(default_return=False)
    async def req_user_exist(self, channel_id: int, user_id: int):
        found = await self.rqst_fsub_Channel_data.find_one({
            '_id': int(channel_id),
            'user_ids': int(user_id)
        })
        return bool(found)


    async def reqChannel_exist(self, channel_id: int):
        channel_ids = await self.show_channels()

        if channel_id in channel_ids:
            return True
        else:
            return False

    @connection_check(default_return=True)
    async def get_retrieve_status(self):
        data = await self.database['settings'].find_one({'_id': 'retrieve_status'})
        if data:
            return data.get('value', True)
        return True

    @connection_check(default_return=False)
    async def set_retrieve_status(self, value: bool):
        await self.database['settings'].update_one(
            {'_id': 'retrieve_status'},
            {'$set': {'value': value}},
            upsert=True
        )
        return True


db = Rohit(DB_URI, DB_NAME)

# =====================================================================================##
#                         ✨ MADE BY UNRATED CODER ✨
#                  Join Updates Channel: https://t.me/UNRATED_CODER
#====================================================================================##
