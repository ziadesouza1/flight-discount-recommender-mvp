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

  const response = await fetch("http://127.0.0.1:8000/recommend", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  const data = await response.json();

  resultsDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
});