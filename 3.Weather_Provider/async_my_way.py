import asyncio

import aiohttp
from aiohttp import ClientError


async def openweather(
    lon: float,
    lat: float,
    base_url: str = r"https://api.openweathermap.org/data/2.5/weather",
    api: str = r"15a70b773b728dbada35622d2fc6d130",
):
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": api,
                "units": "metric",
            }
            async with session.get(url=rf"{base_url}", params=params) as response:
                if response.status != 200:
                    raise RuntimeError(f"Bad status code: {response.status}")

                data = await response.json()

                return data if data else None
        except asyncio.TimeoutError:
            print("Error: Request timed out")

        except ClientError as e:
            print(f"Client error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")


asyncio.run(openweather(lon=32.127594, lat=51.456565))
