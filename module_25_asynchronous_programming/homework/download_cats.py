import asyncio
import aiohttp
from pathlib import Path


async def download_cat(session: aiohttp.ClientSession, idx: int, folder: Path):
    url = "https://api.thecatapi.com/v1/images/search"
    async with session.get(url) as resp:
        data = await resp.json()
        img_url = data[0]['url']
    async with session.get(img_url) as img_resp:
        img_data = await img_resp.read()

    filename = folder / f"cat_{idx}.jpg"
    await asyncio.to_thread(write_file, filename, img_data)


def write_file(path: Path, data: bytes):
    with open(path, 'wb') as f:
        f.write(data)


async def main(num_cats: int = 10):
    folder = Path("cats")
    folder.mkdir(exist_ok=True)

    async with aiohttp.ClientSession() as session:
        tasks = [download_cat(session, i, folder) for i in range(num_cats)]
        await asyncio.gather(*tasks)
    print(f"Скачано {num_cats} котиков в папку {folder.absolute()}")


if __name__ == "__main__":
    asyncio.run(main())