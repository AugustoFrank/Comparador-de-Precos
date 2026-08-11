from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright
import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from app.factory import criar_scraper


@asynccontextmanager
async def lifespan(app: FastAPI):
    playwright = await async_playwright().start()
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir="perfil_navegador",
        headless=False,
        args=["--disable-blink-features=AutomationControlled"],

    )
    app.state.context = context

    yield

    await context.close()
    await playwright.stop()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/processar-links")
async def processar_links(links: list[str]):
    context = app.state.context

    async def processar_um(url: str):
        page = await context.new_page()
        scraper = criar_scraper(url, page)
        produto = await scraper.extrair(url)
        if produto.sucesso:
            await page.close()
        return produto

    resultados = await asyncio.gather(*[processar_um(url) for url in links])

    # await context.close()
    return resultados