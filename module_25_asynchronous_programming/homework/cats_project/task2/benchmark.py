import asyncio
import aiohttp
import requests
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path

CAT_API = "https://api.thecatapi.com/v1/images/search"
FOLDER = Path("cats_comparison")

def get_image_url():
    return requests.get(CAT_API).json()[0]['url']

def download_image(url, idx):
    return requests.get(url).content

def save_image(data, idx):
    with open(FOLDER / f"cat_{idx}.jpg", 'wb') as f:
        f.write(data)

def threads_download(n):
    with ThreadPoolExecutor(max_workers=10) as ex:
        urls = [get_image_url() for _ in range(n)]
        futures = [ex.submit(download_image, url, i) for i, url in enumerate(urls)]
        for i, fut in enumerate(futures):
            save_image(fut.result(), i)

def processes_download(n):
    with ProcessPoolExecutor(max_workers=4) as ex:
        urls = [get_image_url() for _ in range(n)]
        results = list(ex.map(download_image, urls, range(n)))
        for i, data in enumerate(results):
            save_image(data, i)

async def async_download_one(session, idx):
    async with session.get(CAT_API) as resp:
        data = await resp.json()
        img_url = data[0]['url']
    async with session.get(img_url) as img_resp:
        img_data = await img_resp.read()
    await asyncio.to_thread(save_image, img_data, idx)

async def async_download_all(n):
    async with aiohttp.ClientSession() as session:
        tasks = [async_download_one(session, i) for i in range(n)]
        await asyncio.gather(*tasks)

def measure(func, n):
    FOLDER.mkdir(exist_ok=True)
    start = time.perf_counter()
    if asyncio.iscoroutinefunction(func):
        asyncio.run(func(n))
    else:
        func(n)
    elapsed = time.perf_counter() - start
    for f in FOLDER.glob("*"):
        f.unlink()
    return elapsed

if __name__ == "__main__":
    print("Тестирование для 10, 50, 100 котиков...\n")
    results = {}
    for cnt in (10, 50, 100):
        t_th = measure(threads_download, cnt)
        t_pr = measure(processes_download, cnt)
        t_as = measure(async_download_all, cnt)
        results[cnt] = (t_th, t_pr, t_as)
        print(f"{cnt}: потоки={t_th:.2f}с, процессы={t_pr:.2f}с, асинхронность={t_as:.2f}с")

    print("\n| Кол-во | Потоки | Процессы | Асинхронность |")
    print("|--------|--------|----------|---------------|")
    for cnt, (th, pr, asy) in results.items():
        print(f"| {cnt} | {th:.2f} | {pr:.2f} | {asy:.2f} |")