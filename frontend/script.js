async function getRecommendations() {
    const userRequest = document.getElementById("userRequest").value;
    const results = document.getElementById("results");
    const loading = document.getElementById("loading");

    if (!userRequest.trim()) {
        alert("Please enter what you are looking for.");
        return;
    }

    loading.innerHTML = "🔍 OmniAI is searching for the best products...";
    results.innerHTML = "";

    try {
        const response = await fetch("recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                request: userRequest
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        loading.innerHTML = "";

        if (!data.products || data.products.length === 0) {
            results.innerHTML = "<p>No products found. Try another search.</p>";
            return;
        }

        data.products.forEach(product => {
            const card = document.createElement("div");

            card.className = "product";

            card.innerHTML = `
                ${product.image ? `<img src="${product.image}" alt="Product image">` : ""}
                <h3>${product.title || "Product"}</h3>
                <p><strong>Price:</strong> ${product.price || "Not available"}</p>
                <p><strong>Store:</strong> ${product.store || "Not available"}</p>
                <p><strong>Rating:</strong> ${product.rating || "Not available"}</p>
                <p><strong>Reviews:</strong> ${product.reviews || "Not available"}</p>
                ${
                    product.link
                    ? `<a href="${product.link}" target="_blank">View Product →</a>`
                    : ""
                }
            `;

            results.appendChild(card);
        });

    } catch (error) {
        loading.innerHTML = "";

        results.innerHTML = `
            <p>
                ❌ Error: ${error.message}
            </p>
        `;
    }
}