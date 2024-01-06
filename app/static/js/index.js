document.addEventListener("DOMContentLoaded", function () {
  // Filtrar datos para Ethereum (ETH)
  const ethData = data.filter((item) => item.Symbol === "ETH");

  // Filtrar datos para Bitcoin (BTC)
  const btcData = data.filter((item) => item.Symbol === "BTC");

  // Extraer fechas y precios para Ethereum y Bitcoin
  const ethDates = ethData.map((item) => new Date(item.Time));
  const ethPrices = ethData.map((item) => parseFloat(item.Price));

  const btcDates = btcData.map((item) => new Date(item.Time));
  const btcPrices = btcData.map((item) => parseFloat(item.Price));

  // Crear el trazado del gráfico
  const traceETH = {
    x: ethDates,
    y: ethPrices,
    mode: "lines+markers",
    name: "Ethereum",
  };

  const traceBTC = {
    x: btcDates,
    y: btcPrices,
    mode: "lines+markers",
    name: "Bitcoin",
  };

  const layout = {
    title: "Precio de Ethereum y Bitcoin a lo largo del tiempo",
    xaxis: {
      title: "Tiempo",
    },
    yaxis: {
      title: "Precio",
    },
  };

  const dataToPlot = [traceETH, traceBTC];

  // Dibujar el gráfico utilizando Plotly.js
  Plotly.newPlot("chart", dataToPlot, layout);
});
