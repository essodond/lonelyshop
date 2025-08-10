
function updateCartBadge(quantity) {
    const badge = document.getElementById('cart-badge');
    if (quantity > 0) {
        badge.textContent = quantity;
        badge.style.display = 'inline-block';
    } else {
        badge.style.display = 'none';
    }
}

// Exemple d'appel (par exemple après fetch ou au chargement de la page)
updateCartBadge(3);  // Affiche un badge avec "3"

document.addEventListener("DOMContentLoaded", function() {
    updateTotal();

    // Ajouter des écouteurs d'événements pour les boutons de quantité
    document.querySelectorAll(".quantity button").forEach(button => {
        button.addEventListener("click", function() {
            const input = this.parentElement.querySelector("input");
            let quantity = parseInt(input.value);
            if (this.textContent === "+") {
                quantity++;
            } else if (this.textContent === "-" && quantity > 1) {
                quantity--;
            }
            input.value = quantity;
            updateTotal();
        });
    });

    // Ajouter des écouteurs d'événements pour les champs de quantité
    document.querySelectorAll(".quantity input").forEach(input => {
        input.addEventListener("change", function() {
            if (parseInt(this.value) < 1) {
                this.value = 1;
            }
            updateTotal();
        });
    });
});

function updateTotal() {
    let total = 0;
    document.querySelectorAll(".cart-item").forEach(item => {
        const price = parseFloat(item.querySelector(".price").textContent.replace("€", "").trim());
        const quantity = parseInt(item.querySelector("input").value);
        total += price * quantity;
    });
    document.querySelector(".total span:last-child").textContent = total + " Fcfa";
}

