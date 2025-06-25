import asyncio
from database.crud import ServerCRUD    
from config import settings
from bot import bot, dp
from bot.handlers import router as message_router
from bot.callback_handlers.configs import router as config_router
from bot.callback_handlers.servers import router as server_router
from bot.callback_handlers.users import router as user_router
from xuiapi import XUIAPI


async def main():
    server_list = await ServerCRUD.find_all()
    servers = [XUIAPI(
            host=server.server_host,
            port=server.server_port,
            webpath=server.server_webpath
        ) for server in server_list]
    tasks = [inst.login(server.server_login, server.server_password) for inst, server in list(zip(servers, server_list))]
    results = await asyncio.gather(*tasks)
    api_list = {server.id: api for server, api in list(zip(server_list, servers)) if api is not None}
    dp['api_list'] = api_list

    dp.include_router(message_router)
    dp.include_router(config_router)
    dp.include_router(server_router)
    dp.include_router(user_router)
    await dp.start_polling(bot)


asyncio.run(main())

