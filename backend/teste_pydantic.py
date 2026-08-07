from pydantic import BaseModel
from typing import Optional

class Produto(BaseModel):
    url: str
    loja: str
    nome: Optional[str] = None
    preco_original: Optional[float] = None
    preco_final: Optional[float] = None
    imagem: Optional[str] = None