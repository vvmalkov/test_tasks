import asyncio
import aiohttp


class APIException(Exception):
    pass


class BitlyAPI:
    BASE_URL = "https://api-ssl.bitly.com/v4"
    HEADERS = {
        "Content-Type": "application/json",
    }

    def __init__(self, token):
        self.token = token
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={
            "Authorization": f"Bearer {self.token}",
            **self.HEADERS
        })
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def shorten(self, long_url: str) -> str:
        try:
            data = {
                "long_url": long_url,
            }
            async with self.session.post(f"{self.BASE_URL}/shorten", json=data) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["link"]
                else:
                    error_text = await response.text()
                    raise APIException(f"Error {response.status}: {error_text}")
        except aiohttp.ClientError as err:
            raise APIException(f"HTTP error occurred: {err}") from err


async def main():
    token = "38c84115c8a13d1bebc185af26d71a2b177174ac"
    async with BitlyAPI(token) as api:
        try:
            responses = await asyncio.gather(
                api.shorten('https://yandex.ru'),
                api.shorten('https://google.com'),
                return_exceptions=True
            )
            for response in responses:
                if isinstance(response, Exception):
                    raise response
                print(response)  # out: [200] SHORTEN LINK
            response = await api.shorten('bad_link')
            print(response)
        except APIException as err:
            print(err)  # output: [404] NOT FOUND


if __name__ == "__main__":
    asyncio.run(main())
