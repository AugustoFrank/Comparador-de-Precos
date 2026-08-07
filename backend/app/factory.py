from playwright.async_api import Page
from app.scrapers.mercado_livre import ScraperMercadoLivre
from app.scrapers.base import ScraperBase


def criar_scraper(url: str, page: Page) -> ScraperBase:
    if "mercadolivre.com" in url:
        return ScraperMercadoLivre(page)

    raise ValueError(f"Loja não suportada para a URL: {url}")