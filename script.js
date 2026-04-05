const form = document.getElementById("search-form");
const resultsDiv = document.getElementById("results");

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  const payload = {
    origin: document.getElementById("origin").value,
    destination: document.getElementById("destination").value,
    date: document.getElementById("date").value,
    number_of_passengers: Number(document.getElementById("number_of_passengers").value)
  };

  // 🔹 Show loading
  resultsDiv.innerHTML = "<p>Searching best deals...</p>";

  try {
    const response = await fetch("http://127.0.0.1:8000/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error("Something went wrong with the request");
    }

    const data = await response.json();

    if (!data.results || data.results.length === 0) {
      resultsDiv.innerHTML = `<p>No matching flights found.</p>`;
      return;
    }

    let tableHtml = `
      <table>
        <thead>
          <tr>
            <th>Flight</th>
            <th>Base</th>
            <th>Total</th>
            <th>Cashback</th>
            <th>Savings</th>
            <th>Final Price</th>
          </tr>
        </thead>
        <tbody>
    `;

    data.results.forEach((flight, index) => {
      const savings =
        flight.total_base_price - flight.final_price;
      
      const highlight = index === 0 ? 'style="background-color: #d4edda;"' : "";

      tableHtml += `
        <tr ${highlight}>
          <td>${flight.flight_no}</td>
          <td>$${flight.price.toFixed(2)}</td>
          <td>$${flight.total_base_price.toFixed(2)}</td>
          <td>$${(flight.cashback_value ?? 0).toFixed(2)}</td>
          <td style="color: green;">-$${savings.toFixed(2)}</td>
          <td><strong>$${flight.final_price.toFixed(2)}</strong></td>
        </tr>
      `;
    });

    resultsDiv.innerHTML = tableHtml;

  } catch (error) {
    console.error(error);
    resultsDiv.innerHTML = `<p style="color: red;">Error fetching results. Please try again.</p>`;
  }
});