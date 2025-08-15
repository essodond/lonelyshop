document.addEventListener('DOMContentLoaded', function() {
    // Gestion des messages d'erreur
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        alerts.forEach(alert => {
            setTimeout(() => {
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }, 3000);
        });
    }

    // Gestion de l'affichage des champs de paiement
    const paymentMethodSelect = document.getElementById('payment_method');
    const mobilePaymentFields = document.getElementById('mobile-payment-fields');
    const cardPaymentFields = document.getElementById('card-payment-fields');

    if (paymentMethodSelect) {
        paymentMethodSelect.addEventListener('change', function() {
            const selectedMethod = this.value;

            // Cacher tous les champs
            mobilePaymentFields.style.display = 'none';
            cardPaymentFields.style.display = 'none';

            // Afficher les champs appropriés
            if (selectedMethod === 'MIXX' || selectedMethod === 'FLOOZ') {
                mobilePaymentFields.style.display = 'block';
            } else if (selectedMethod === 'CARD') {
                cardPaymentFields.style.display = 'block';
            }
        });
    }

    // Validation des formulaires
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const paymentMethod = form.querySelector('#payment_method');
            if (paymentMethod) {
                const selectedMethod = paymentMethod.value;
                let requiredFields;

                if (selectedMethod === 'CARD') {
                    requiredFields = form.querySelectorAll('#card-payment-fields [required]');
                } else if (selectedMethod === 'MIXX' || selectedMethod === 'FLOOZ') {
                    requiredFields = form.querySelectorAll('#mobile-payment-fields [required]');
                } else {
                    requiredFields = form.querySelectorAll('[required]');
                }

                let isValid = true;
                requiredFields.forEach(field => {
                    if (!field.value.trim()) {
                        isValid = false;
                        field.classList.add('is-invalid');
                    } else {
                        field.classList.remove('is-invalid');
                    }
                });

                if (!isValid) {
                    e.preventDefault();
                }
            }
        });
    });
});
