import aiohttp


class AsyncDataProvider:
    async def get(self, url: str, session: aiohttp.ClientSession=None) -> str:
        if session:
            async with session.get(url) as response:
                return await response.content.read()
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.content.read()
