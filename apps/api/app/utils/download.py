from pathlib import Path

import httpx


async def download_file(
    url: str,
    destination: str,
):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        response.raise_for_status()

        with open(destination, "wb") as file:
            file.write(response.content)

    return destination