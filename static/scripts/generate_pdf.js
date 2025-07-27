let osTypeModal = null;

function openModal(orderId) {
    document.getElementById('modalOrderId').value = orderId;

    if (!osTypeModal) {
        osTypeModal = new bootstrap.Modal(document.getElementById('osTypeModal'));
    }
    osTypeModal.show();
}

function closeModal() {
    if (!osTypeModal) {
        osTypeModal = new bootstrap.Modal(document.getElementById('osTypeModal'));
    }
    osTypeModal.hide();
}

// Função para baixar PDF
function baixarPDF() {
    var orderId = document.getElementById('modalOrderId').value;
    var tipo = document.querySelector('input[name="tipo"]:checked').value;
    window.location.href = '/orders/generate_pdf/' + orderId + '/?type=' + tipo;
    closeModal();
}
