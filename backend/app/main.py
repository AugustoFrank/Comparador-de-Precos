from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright
import asyncio

from app.factory import criar_scraper


@asynccontextmanager
async def lifespan(app: FastAPI):
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    app.state.browser = browser

    yield

    await browser.close()
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
    browser = app.state.browser
    context = await browser.new_context()

    async def processar_um(url: str):
        page = await context.new_page()
        scraper = criar_scraper(url, page)
        produto = await scraper.extrair(url)
        await page.close()
        return produto

    resultados = await asyncio.gather(*[processar_um(url) for url in links])

    await context.close()
    return resultados