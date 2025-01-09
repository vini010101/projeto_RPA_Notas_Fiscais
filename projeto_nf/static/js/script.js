document.getElementById("formulario").addEventListener("submit", function (event) {
    event.preventDefault(); // Impede o envio imediato do formulário

    // Lista de IDs dos campos obrigatórios
    const campos = ["nome", "fone", "email", "mensagem", "tempo"];
    let formValido = true;

    // Validação dos campos obrigatórios
    campos.forEach(function (campoId) {
        const campo = document.getElementById(campoId);

        if (!campo.value.trim()) {
            campo.style.border = "2px solid red"; // Borda vermelha se o campo estiver vazio
            formValido = false;
        } else {
            campo.style.border = "2px solid green"; // Borda verde se o campo estiver preenchido
        }
    });

    if (!formValido) {
        alert("Por favor, preencha todos os campos obrigatórios.");
        return; // Impede o envio do formulário se houver campos vazios
    }

    // Criação do objeto FormData para enviar os dados
    const formData = new FormData(event.target);

    // Envio dos dados para o servidor
    fetch("/enviar_orcamento", {
        method: "POST",
        body: formData,
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Erro no envio do formulário.");
            }
            return response.json();
        })
        .then((data) => {
            alert("Formulário enviado com sucesso!");
            window.location.href = "/"; // Redireciona após o sucesso
        })
        .catch((error) => {
            console.error("Erro ao enviar formulário:", error);
            alert("Ocorreu um erro ao enviar o formulário. Tente novamente.");
        });
});

// Função de cálculo do custo estimado
document.getElementById("calcular-btn").addEventListener("click", function () {
    const tempo = parseInt(document.getElementById("tempo").value);

    if (isNaN(tempo) || tempo <= 0) {
        alert("Por favor, insira um número válido para os Dias.");
        return;
    }

    const valorHora = 10;
    const horasPorDia = 8;
    const diasPorSemana = 5;
    const valorDiario = valorHora * horasPorDia;
    const valorSemanal = valorDiario * diasPorSemana;
    const custoEstimado = valorSemanal * (tempo / diasPorSemana);

    document.getElementById("resultado").textContent = `Custo estimado: R$ ${custoEstimado.toFixed(2)}`;
    document.getElementById("custo_estimado").value = custoEstimado;
});

// Exibe alerta ao carregar imagens
document.getElementById("imagens").addEventListener("change", function (event) {
    if (event.target.files.length > 0) {
        alert("Imagem carregada com sucesso!");
    }
});
