import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as playwright:
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir="./perfil_navegador",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = await context.new_page()
        await page.goto("https://www.mercadolivre.com.br", timeout=60000, wait_until="domcontentloaded")

        input("Faça login manualmente na janela do Chrome, depois pressione Enter aqui no terminal...")

        await context.close()


asyncio.run(main())