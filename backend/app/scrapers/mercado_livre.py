import time
from playwright.async_api import Page
from app.models.produto import Produto
from app.scrapers.base import ScraperBase


def converter_preco(texto: str) -> float:
    partes = texto.split()
    reais = float(partes[0])
    centavos = float(partes[3]) / 100
    return reais + centavos


class ScraperMercadoLivre(ScraperBase):
    def __init__(self, page: Page):
        self.page = page

    async def extrair(self, url: str) -> Produto:
        inicio = time.time()
        try:
            await self.page.goto(url, timeout=60000, wait_until="domcontentloaded")

            nome = await self.page.locator(".ui-pdp-title").inner_text(timeout=60000)

            preco_final_texto = await self.page.locator(
                ".ui-pdp-price__second-line .andes-money-amount"
            ).first.get_attribute("aria-label", timeout=60000)
            preco_final = converter_preco(preco_final_texto)

            preco_original = None
            original_locator = self.page.locator(".ui-pdp-price__original-value")
            if await original_locator.count() > 0:
                texto_original = await original_locator.get_attribute("aria-label")
                texto_original = texto_original.replace("Antes: ", "")
                preco_original = converter_preco(texto_original)

            imagem = await self.page.locator("img.ui-pdp-image").first.get_attribute("src")

            duracao = time.time() - inicio
            print(f"[{url}] processado em {duracao:.2f} segundos")

            return Produto(
                url=url,
                loja="mercado_livre",
                nome=nome.strip(),
                preco_original=preco_original,
                preco_final=preco_final,
                imagem=imagem,
                sucesso=True,
            )
        except Exception as e:
            return Produto(
                url=url,
                loja="mercado_livre",
                sucesso=False,
                erro=str(e),
            )