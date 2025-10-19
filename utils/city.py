import asyncio
import aiohttp

url = 'https://nominatim.openstreetmap.org/search?format=json&q='


async def check(name: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url + name) as response:
            if response.status == 200 and len(await response.json()) > 0:
                return True
                # return await response.json()   
            return False
            

# print(asyncio.run(check('Москва')))