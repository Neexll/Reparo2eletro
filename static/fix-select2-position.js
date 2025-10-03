/**
 * Corrige o posicionamento do Select2
 * Este script deve ser carregado após o jQuery e o Select2
 */
(function($) {
    // Aguarda o documento estar pronto
    $(document).ready(function() {
        console.log('Script de correção do Select2 carregado');
        
        // Função para corrigir o posicionamento do Select2
        function fixSelect2Position() {
            console.log('Aplicando correção de posicionamento do Select2');
            
            // Remove qualquer instância existente do Select2
            if ($.fn.select2) {
                $('select').select2('destroy');
            }
            
            // Configuração padrão para todos os selects
            const select2Config = {
                theme: 'bootstrap-5',
                width: '100%',
                dropdownAutoWidth: true,
                dropdownParent: $(document.body), // Usa o body como parent
                minimumResultsForSearch: 10,
                allowClear: true,
                closeOnSelect: true,
                placeholder: 'Selecione uma opção',
                dropdownCssClass: 'select2-dropdown-fixed',
                containerCssClass: 'select2-container-fixed'
            };
            
            // Inicializa o Select2 para todos os selects
            $('select').select2(select2Config);
            
            // Ajusta o posicionamento do dropdown quando aberto
            $(document).on('select2:open', function(e) {
                const selectId = e.target.id;
                const $select = $(`#${selectId}`);
                
                // Aguarda um pequeno atraso para garantir que o dropdown foi renderizado
                setTimeout(function() {
                    const $dropdown = $('.select2-dropdown');
                    
                    if ($dropdown.length) {
                        // Obtém a posição do select
                        const selectRect = $select[0].getBoundingClientRect();
                        
                        // Calcula a posição do dropdown
                        const dropdownTop = selectRect.bottom + window.scrollY;
                        const dropdownLeft = selectRect.left + window.scrollX;
                        
                        // Aplica os estilos diretamente no dropdown
                        $dropdown.css({
                            'position': 'absolute',
                            'top': dropdownTop + 'px',
                            'left': dropdownLeft + 'px',
                            'width': selectRect.width + 'px',
                            'min-width': '200px',
                            'max-width': '90vw',
                            'z-index': '99999',
                            'margin': '0',
                            'padding': '0',
                            'border': '1px solid #e2e8f0',
                            'border-radius': '0.5rem',
                            'box-shadow': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)'
                        });
                        
                        console.log('Dropdown reposicionado:', {
                            top: dropdownTop,
                            left: dropdownLeft,
                            width: selectRect.width
                        });
                    }
                }, 10);
            });
            
            // Ajusta o posicionamento quando a janela é redimensionada
            $(window).on('resize', function() {
                if ($('.select2-dropdown').is(':visible')) {
                    $('select').trigger('select2:open');
                }
            });
            
            // Ajusta o posicionamento quando a página é rolada
            $(window).on('scroll', function() {
                if ($('.select2-dropdown').is(':visible')) {
                    $('select').trigger('select2:open');
                }
            });
        }
        
        // Inicializa a correção
        fixSelect2Position();
        
        // Reaplica a correção após 1 segundo (caso haja carregamento dinâmico de conteúdo)
        setTimeout(fixSelect2Position, 1000);
    });
    
    // Adiciona um estilo global para o dropdown
    const style = document.createElement('style');
    style.textContent = `
        .select2-dropdown-fixed {
            position: absolute !important;
            z-index: 99999 !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 0.5rem !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
            margin-top: 4px !important;
            background-color: white !important;
            overflow: hidden !important;
        }
        
        .select2-container-fixed {
            position: relative !important;
            z-index: 1 !important;
        }
        
        /* Garante que o dropdown não seja cortado */
        html, body, .container, .row, [class*="col-"], .card, .modal-content, .form-container {
            overflow: visible !important;
        }
    `;
    document.head.appendChild(style);
    
})(jQuery);
