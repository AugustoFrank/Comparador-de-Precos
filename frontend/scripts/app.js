console.log("app.js carregou!");

const listaInputs = document.getElementById("lista-inputs");
const btnAdicionar = document.getElementById("btn-adicionar");
const inputLinks = document.getElementById('link-input');
const btnProcessar = document.getElementById('btn-processar');
const divResultado = document.getElementById('resultado');
const divTotal = document.getElementById('total');

btnProcessar.addEventListener('click', () => {
    console.log("Btn clicado");

    async function processarLinks() {
        // const links = inputLinks.value.split('\n').map(link => link.trim()).filter(link => link !== '');
        const todosInputs = document.querySelectorAll(".link-input");
        const links = Array.from(todosInputs)
        .map(input => input.value.trim())
        .filter(link => link !== "");
        try {
            const resposta = await fetch('http://127.0.0.1:8000/processar-links', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(links)
            });

            const produtos = await resposta.json();
            console.log("Produtos:", produtos);
            console.log(JSON.stringify(produtos, null, 2));

            const html = produtos.map(produto => {
                if (!produto.sucesso) {
                    return `
                        <div class="produto produto-erro">
                            <p>⚠️ Não foi possível processar este link.</p>
                            <small>${produto.url}</small>
                        </div>
                    `;
                }
                return `
                    <div class="produto">
                        <img src="${produto.imagem}" alt="${produto.nome}">
                        <div class="produto-info">
                            <span class="produto-nome">${produto.nome}</span>
                            <span class="produto-preco">R$ ${produto.preco_final.toFixed(2)}</span>
                        </div>
                    </div>
                `;
            }).join("");
            
            divResultado.innerHTML = html;
        } catch (erro) {
            console.log("Erro:", erro);
        }
    }

    processarLinks();
});

btnAdicionar.addEventListener("click", () => {
    const novoInput = document.createElement("input");
    // configura o novoInput aqui
    novoInput.type = "text";
    novoInput.className = "link-input";
    novoInput.placeholder = "Cole o link do produto";
    // anexa o novoInput aqui
    listaInputs.appendChild(novoInput);
});