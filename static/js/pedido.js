// Função para atualizar os defeitos quando uma peça é selecionada
function atualizarDefeitos(selectElement) {
    const pecaRow = selectElement.closest('.peca-row');
    if (!pecaRow) return;
    
    const pecaId = selectElement.options[selectElement.selectedIndex]?.getAttribute('data-id');
    const defeitoSelect = pecaRow.querySelector('select[name="peca_defeito[]"]');
    const defeitoManualInput = pecaRow.querySelector('.defeito-manual');
    const defeitoManualHidden = pecaRow.querySelector('.defeito-manual-hidden');
    
    if (!defeitoSelect || !defeitoManualInput || !defeitoManualHidden) {
        console.error('Elementos necessários não encontrados');
        return;
    }
    
    // Reseta o campo de defeito manual
    defeitoManualInput.value = '';
    defeitoManualHidden.value = '';
    
    // Remove a classe de ativo do modo manual
    pecaRow.classList.remove('defeito-manual-ativo');
    
    if (pecaId) {
        // Limpa as opções atuais
        while (defeitoSelect.options.length > 0) {
            defeitoSelect.remove(0);
        }
        
        // Adiciona a opção padrão de carregamento
        const loadingOption = document.createElement('option');
        loadingOption.value = '';
        loadingOption.disabled = true;
        loadingOption.selected = true;
        loadingOption.textContent = 'Carregando defeitos...';
        defeitoSelect.appendChild(loadingOption);
        
        // Habilita o botão de usar manual
        const usarManualBtn = pecaRow.querySelector('.usar-manual');
        if (usarManualBtn) {
            usarManualBtn.disabled = false;
            usarManualBtn.textContent = 'Usar';
        }
        
        // Busca os defeitos para a peça selecionada
        fetch(`/api/pecas/${pecaId}/defeitos`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro ao carregar defeitos: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(defeitos => {
                // Remove a opção de carregamento
                while (defeitoSelect.options.length > 0) {
                    defeitoSelect.remove(0);
                }
                
                // Adiciona a opção padrão
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.disabled = true;
                defaultOption.selected = true;
                defaultOption.textContent = 'Selecione o defeito...';
                defeitoSelect.appendChild(defaultOption);
                
                // Adiciona a opção para digitar manualmente
                const manualOption = document.createElement('option');
                manualOption.value = 'manual';
                manualOption.textContent = 'Digitar defeito manualmente...';
                defeitoSelect.appendChild(manualOption);
                
                // Adiciona um separador
                const separator = document.createElement('option');
                separator.disabled = true;
                separator.textContent = '──────────────';
                defeitoSelect.appendChild(separator);
                
                // Adiciona os defeitos retornados
                if (Array.isArray(defeitos) && defeitos.length > 0) {
                    defeitos.forEach((defeito) => {
                        const option = document.createElement('option');
                        option.value = defeito;
                        option.textContent = defeito;
                        defeitoSelect.appendChild(option);
                    });
                } else {
                    const option = document.createElement('option');
                    option.value = '';
                    option.disabled = true;
                    option.textContent = 'Nenhum defeito cadastrado';
                    defeitoSelect.appendChild(option);
                }
            })
            .catch(error => {
                console.error('Erro ao carregar defeitos:', error);
                
                // Remove a opção de carregamento
                while (defeitoSelect.options.length > 0) {
                    defeitoSelect.remove(0);
                }
                
                // Adiciona uma opção de erro
                const errorOption = document.createElement('option');
                errorOption.value = '';
                errorOption.disabled = true;
                errorOption.selected = true;
                errorOption.textContent = 'Erro ao carregar defeitos. Tente novamente.';
                defeitoSelect.appendChild(errorOption);
                
                const option = document.createElement('option');
                option.value = '';
                option.disabled = true;
                option.selected = true;
                option.textContent = 'Erro ao carregar defeitos';
                defeitoSelect.appendChild(option);
                
                // Habilita o botão de usar manual mesmo em caso de erro
                const usarManualBtn = pecaRow.querySelector('.usar-manual');
                if (usarManualBtn) {
                    usarManualBtn.disabled = false;
                }
            });
    } else {
        // Limpa o select de defeitos se nenhuma peça estiver selecionada
        while (defeitoSelect.options.length > 0) {
            defeitoSelect.remove(0);
        }
        
        const option = document.createElement('option');
        option.value = '';
        option.disabled = true;
        option.selected = true;
        option.textContent = 'Selecione uma peça primeiro';
        defeitoSelect.appendChild(option);
        
        // Desabilita o botão de usar manual
        const usarManualBtn = pecaRow.querySelector('.usar-manual');
        if (usarManualBtn) {
            usarManualBtn.disabled = true;
        }
    }
}

// Função para adicionar uma nova linha de peça
function addPecaRow() {
    console.log('Adicionando nova linha de peça...');
    
    const template = document.getElementById('peca-template');
    if (!template) {
        console.error('Template de peça não encontrado');
        return;
    }
    
    const clone = template.content.cloneNode(true);
    const pecasContainer = document.getElementById('pecas-container');
    
    if (!pecasContainer) {
        console.error('Container de peças não encontrado');
        return;
    }
    
    // Adiciona a nova linha ao container
    pecasContainer.appendChild(clone);
    
    // Inicializa os eventos para a nova linha
    const newRow = pecasContainer.lastElementChild;
    if (newRow) {
        initDefeitoManualEventsForRow(newRow);
    }
    
    console.log('Nova linha de peça adicionada com sucesso');
}

// Inicializa a página quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM carregado, inicializando...');
    
    // Adiciona a primeira linha de peça
    if (typeof addPecaRow === 'function') {
        console.log('Adicionando primeira linha de peça...');
        addPecaRow();
    }
    
    // Configura o botão de adicionar peça
    const addPecaBtn = document.getElementById('add-peca-btn');
    if (addPecaBtn) {
        addPecaBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (typeof addPecaRow === 'function') {
                addPecaRow();
            }
        });
    }
});

// Torna as funções disponíveis globalmente
window.atualizarDefeitos = atualizarDefeitos;
window.addPecaRow = addPecaRow;
