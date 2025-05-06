
async function carregarDetalhes() {
  const urlParams = new URLSearchParams(window.location.search);
  const id = urlParams.get('id');

  const resposta = await fetch('/api/dados');
  const produtos = await resposta.json();
  const produto = produtos[id];

  document.getElementById("nome").textContent = produto.nome;
  document.getElementById("detalhes").textContent = produto.detalhes || "Sem detalhes adicionais";
  document.getElementById("valor").textContent = produto.valor;

  const historico = produto.historico || [produto.valor];

  const valores = historico.map(v => parseFloat(v.replace(/[^\d,]/g, '').replace(',', '.')));
  const labels = historico.map((_, i) => `Dia ${i + 1}`);

  const ctx = document.getElementById('graficoPreco').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Preço (R$)',
        data: valores,
        borderWidth: 2
      }]
    }
  });
}
carregarDetalhes();
