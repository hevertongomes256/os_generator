// ================================
// DASHBOARD JAVASCRIPT
// ================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ================================
    // SIDEBAR TOGGLE
    // ================================
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
            sidebarOverlay.classList.toggle('show');
        });
    }
    
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
        });
    }
    
    // Fechar sidebar ao redimensionar para desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 992) {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
        }
    });
    
    // ================================
    // MODAL PDF FUNCTIONS
    // ================================
    let pdfModal = null;
    
    window.openModal = function(orderId) {
        const modalOrderId = document.getElementById('modalOrderId');
        if (modalOrderId) {
            modalOrderId.value = orderId;
        }
        
        if (!pdfModal) {
            const modalElement = document.getElementById('osTypeModal');
            if (modalElement && typeof bootstrap !== 'undefined') {
                pdfModal = new bootstrap.Modal(modalElement);
            }
        }
        
        if (pdfModal) {
            pdfModal.show();
        }
    };
    
    window.baixarPDF = function() {
        const orderId = document.getElementById('modalOrderId').value;
        const tipoRadio = document.querySelector('input[name="tipo"]:checked');
        
        if (orderId && tipoRadio) {
            const tipo = tipoRadio.value;
            // Ajuste a URL conforme sua configuração de URLs do Django
            window.location.href = `/orders/generate_pdf/${orderId}/?type=${tipo}`;
            
            if (pdfModal) {
                pdfModal.hide();
            }
        }
    };
    
    // ================================
    // CHARTS SETUP
    // ================================
    function initializeCharts() {
        // Verificar se Chart.js está carregado
        if (typeof Chart === 'undefined') {
            console.warn('Chart.js não está carregado');
            return;
        }
        
        // Configurações globais do Chart.js
        Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
        Chart.defaults.font.size = 12;
        Chart.defaults.color = '#6b7280';
        
        // Gráfico de Ordens por Mês
        const ordersCanvas = document.getElementById('ordersChart');
        if (ordersCanvas && window.chartData) {
            const ctx = ordersCanvas.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: JSON.parse(window.chartData.months || '[]'),
                    datasets: [{
                        label: 'Ordens Criadas',
                        data: JSON.parse(window.chartData.order_counts || '[]'),
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: '#3b82f6',
                        pointBorderColor: '#ffffff',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        pointHoverRadius: 7
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleColor: '#ffffff',
                            bodyColor: '#ffffff',
                            borderColor: '#3b82f6',
                            borderWidth: 1,
                            cornerRadius: 8,
                            displayColors: false
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                display: false
                            },
                            ticks: {
                                maxTicksLimit: 6
                            }
                        },
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: '#f3f4f6'
                            },
                            ticks: {
                                stepSize: 1,
                                callback: function(value) {
                                    return Math.floor(value) === value ? value : '';
                                }
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    }
                }
            });
        }
        
        // Gráfico de Faturamento Mensal
        const revenueCanvas = document.getElementById('revenueChart');
        if (revenueCanvas && window.chartData) {
            const ctx = revenueCanvas.getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: JSON.parse(window.chartData.months || '[]'),
                    datasets: [{
                        label: 'Faturamento (R$)',
                        data: JSON.parse(window.chartData.order_values || '[]'),
                        backgroundColor: 'rgba(16, 185, 129, 0.8)',
                        borderColor: '#10b981',
                        borderWidth: 1,
                        borderRadius: 6,
                        borderSkipped: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleColor: '#ffffff',
                            bodyColor: '#ffffff',
                            borderColor: '#10b981',
                            borderWidth: 1,
                            cornerRadius: 8,
                            displayColors: false,
                            callbacks: {
                                label: function(context) {
                                    return 'R$ ' + context.parsed.y.toLocaleString('pt-BR', {
                                        minimumFractionDigits: 2,
                                        maximumFractionDigits: 2
                                    });
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                display: false
                            },
                            ticks: {
                                maxTicksLimit: 6
                            }
                        },
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: '#f3f4f6'
                            },
                            ticks: {
                                callback: function(value) {
                                    return 'R$ ' + value.toLocaleString('pt-BR', {
                                        minimumFractionDigits: 0,
                                        maximumFractionDigits: 0
                                    });
                                }
                            }
                        }
                    }
                }
            });
        }
    }
    
    // Inicializar charts quando a página carregar
    initializeCharts();
    
    // ================================
    // MELHORIAS DE UX
    // ================================
    
    // Smooth scroll para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Auto-close alerts após 5 segundos
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.transition = 'opacity 0.3s ease-out';
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }
        }, 5000);
    });
    
    // Tooltips para elementos com title
    const elementsWithTitle = document.querySelectorAll('[title]');
    elementsWithTitle.forEach(element => {
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            new bootstrap.Tooltip(element);
        }
    });
    
    // Highlight da linha da tabela atual
    const tableRows = document.querySelectorAll('.orders-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // ================================
    // KEYBOARD SHORTCUTS
    // ================================
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K para focar no campo de busca
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[name="search"]');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
        
        // ESC para fechar modal ou sidebar
        if (e.key === 'Escape') {
            if (sidebar && sidebar.classList.contains('show')) {
                sidebar.classList.remove('show');
                sidebarOverlay.classList.remove('show');
            }
            
            if (pdfModal) {
                pdfModal.hide();
            }
        }
    });
    
    // ================================
    // LOADING STATES
    // ================================
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Carregando...';
            }
        });
    });
});

// ================================
// UTILITY FUNCTIONS
// ================================

// Função para formatar números como moeda
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Função para debounce (útil para campos de busca)
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Função para mostrar notificações toast
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}
