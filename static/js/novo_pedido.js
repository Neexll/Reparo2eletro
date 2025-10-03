// Variáveis globais para armazenar os dados
let tecnicos = [];
let tiposPecas = [];

// Função para carregar técnicos do servidor
async function carregarTecnicos() {
    try {
        const response = await fetch('/api/tecnicos');
        if (!response.ok) {
            throw new Error(`Erro ao carregar técnicos: ${response.status}`);
        }
        tecnicos = await response.json();
        preencherSelectTecnicos();
    } catch (error) {
        console.error('Erro ao carregar técnicos:', error);
        mostrarMensagem('Erro ao carregar a lista de técnicos. Tente recarregar a página.', 'error');
    }
}

// Função para preencher o select de técnicos
function preencherSelectTecnicos() {
    const selectTecnico = document.getElementById('tecnico_nome');
    if (!selectTecnico) return;
    
    // Limpa opções existentes, exceto a primeira
    selectTecnico.innerHTML = '<option value="" disabled selected>Selecione o técnico...</option>';
    
    // Adiciona os técnicos
    tecnicos.forEach(tecnico => {
        const option = document.createElement('option');
        option.value = tecnico.nome;
        option.textContent = tecnico.nome;
        selectTecnico.appendChild(option);
    });
    
    // Re-inicializa o Select2 com configuração simplificada
    $(selectTecnico).select2({
        theme: 'bootstrap-5',
        width: '100%',
        placeholder: 'Selecione o técnico...',
        allowClear: true,
        dropdownParent: document.body,
        dropdownAutoWidth: true
    });
}

// Função para carregar tipos de peças do servidor
async function carregarTiposPecas() {
    try {
        const response = await fetch('/api/tipos-pecas');
        if (!response.ok) {
            throw new Error(`Erro ao carregar tipos de peças: ${response.status}`);
        }
        tiposPecas = await response.json();
    } catch (error) {
        console.error('Erro ao carregar tipos de peças:', error);
        mostrarMensagem('Erro ao carregar a lista de peças. Tente recarregar a página.', 'error');
    }
}

// Função para mostrar mensagens para o usuário
function mostrarMensagem(mensagem, tipo = 'info') {
    // Remove mensagens antigas
    const mensagensAntigas = document.querySelectorAll('.alert');
    mensagensAntigas.forEach(msg => msg.remove());
    
    // Cria a nova mensagem
    const divMensagem = document.createElement('div');
    divMensagem.className = `alert alert-${tipo} alert-dismissible fade show`;
    divMensagem.role = 'alert';
    divMensagem.innerHTML = `
        ${mensagem}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
    `;
    
    // Insere a mensagem no topo do formulário
    const form = document.getElementById('form-pedido');
    if (form) {
        form.prepend(divMensagem);
    }
}

// Função para inicializar a página
document.addEventListener('DOMContentLoaded', async function() {
    console.log('Página de novo pedido carregada');
    
    try {
        // Carrega os dados iniciais
        await Promise.all([
            carregarTecnicos(),
            carregarTiposPecas()
        ]);
        
        // Inicializa os selects com Select2
        initSelect2();
        
        // Adiciona a primeira linha de peça
        adicionarLinhaPeca();
        
        // Configura o botão de adicionar peça
        const btnAdicionarPeca = document.getElementById('btn-adicionar-peca');
        if (btnAdicionarPeca) {
            btnAdicionarPeca.addEventListener('click', adicionarLinhaPeca);
        }
        
        // Configura o formulário
        const formPedido = document.getElementById('form-pedido');
        if (formPedido) {
            formPedido.addEventListener('submit', validarFormulario);
        }
        
    } catch (error) {
        console.error('Erro ao inicializar a página:', error);
        mostrarMensagem('Erro ao carregar os dados necessários. Por favor, recarregue a página.', 'danger');
    }
});

// Função para inicializar o Select2
function initSelect2() {
    // Verifica se o jQuery e o Select2 estão disponíveis
    if (typeof jQuery === 'undefined' || typeof jQuery.fn.select2 === 'undefined') {
        console.warn('jQuery ou Select2 não encontrados. Carregando...');
        carregarDependencias().then(() => {
            configurarSelect2();
        });
    } else {
        configurarSelect2();
    }
}

// Função para carregar dependências
function carregarDependencias() {
    return new Promise((resolve, reject) => {
        const jqueryScript = document.createElement('script');
        jqueryScript.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
        
        const select2Script = document.createElement('script');
        select2Script.src = 'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js';
        
        const select2Css = document.createElement('link');
        select2Css.rel = 'stylesheet';
        select2Css.href = 'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css';
        
        // Carrega o jQuery primeiro
        jqueryScript.onload = () => {
            // Depois carrega o Select2
            select2Script.onload = () => {
                document.head.appendChild(select2Css);
                resolve();
            };
            select2Script.onerror = () => {
                console.error('Erro ao carregar o Select2');
                reject();
            };
            document.head.appendChild(select2Script);
        };
        
        jqueryScript.onerror = () => {
            console.error('Erro ao carregar o jQuery');
            reject();
        };
        
        document.head.appendChild(jqueryScript);
    });
}

// Função para configurar o Select2
function configurarSelect2() {
    // Verifica se o jQuery e o Select2 estão disponíveis
    if (typeof jQuery === 'undefined' || typeof jQuery.fn.select2 === 'undefined') {
        console.error('jQuery ou Select2 não foram carregados corretamente');
        return;
    }

    // Configuração para os selects
    const select2Config = {
        theme: 'bootstrap-5',
        width: '100%',
        dropdownAutoWidth: true,
        dropdownParent: document.body,
        minimumResultsForSearch: 0,
        allowClear: true,
        closeOnSelect: true,
        placeholder: 'Selecione uma opção',
        dropdownCssClass: 'select2-dropdown-below',
        containerCssClass: 'select2-container--bootstrap-5',
        selectionCssClass: 'form-select',
        dropdownCss: {
            'z-index': '100000',
            'position': 'absolute'
        }
    };

    // Aplica o Select2 aos campos existentes
    $('.form-select').each(function() {
        // Remove o Select2 se já estiver inicializado
        if ($(this).hasClass('select2-hidden-accessible')) {
            $(this).select2('destroy');
        }
        
        // Inicializa o Select2
        const select2Instance = $(this).select2(select2Config);
        
        // Força a abertura do dropdown para verificar se está funcionando
        // Isso é apenas para depuração e pode ser removido depois
        // $(this).on('click', function() {
        //     $(this).select2('open');
        // });
    });

    // Ajusta o z-index do dropdown
    $(document).on('select2:open', function(e) {
        const $select = $(e.target);
        const $dropdown = $select.data('select2').$dropdown;
        
        // Ajusta o z-index do dropdown
        $dropdown.css('z-index', '100000');
        
        // Ajusta a posição do dropdown se estiver muito baixo na tela
        const selectRect = $select[0].getBoundingClientRect();
        const windowHeight = window.innerHeight;
        
        if (selectRect.bottom > windowHeight / 2) {
            $dropdown.addClass('select2-dropdown--above');
        } else {
            $dropdown.removeClass('select2-dropdown--above');
        }
    });
}

// Função para adicionar uma nova linha de peça
function adicionarLinhaPeca() {
    const container = document.getElementById('container-pecas');
    if (!container) return null;
    
    // Cria um ID único para a linha
    const linhaId = 'peca-' + Date.now();
    
    // Cria o HTML da nova linha
    const novaLinha = `
        <div class="card mb-3 card-peca" id="${linhaId}">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label><i class="fas fa-cog"></i> Peça</label>
                            <select name="peca_nome[]" class="form-select select-peca" required 
                                    onchange="atualizarDefeitos(this)">
                                <option value="" disabled selected>Carregando peças...</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label><i class="fas fa-exclamation-triangle"></i> Defeito</label>
                            <div class="defeito-container">
                                <select name="peca_defeito[]" class="form-select select-defeito" required disabled>
                                    <option value="" disabled selected>Selecione uma peça primeiro</option>
                                </select>
                                <div class="ou-separator">ou</div>
                                <div class="input-group">
                                    <input type="text" class="form-control input-defeito-manual" 
                                           placeholder="Digite o defeito manualmente" disabled>
                                    <button type="button" class="btn btn-outline-secondary btn-usar-manual" disabled>
                                        Usar
                                    </button>
                                </div>
                                <input type="hidden" name="defeito_manual[]" class="input-defeito-hidden" value="">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="text-end mt-2">
                    <button type="button" class="btn btn-sm btn-danger btn-remover-peca" 
                            onclick="removerLinhaPeca('${linhaId}')">
                        <i class="fas fa-trash"></i> Remover
                    </button>
                </div>
            </div>
        </div>
    `;
    
    // Adiciona a nova linha ao container
    container.insertAdjacentHTML('beforeend', novaLinha);
    
    const linhaElement = document.getElementById(linhaId);
    
    // Preenche o select de peças
    preencherSelectPecas(linhaElement);
    
    // Inicializa os eventos para a nova linha
    inicializarEventosLinha(linhaElement);
    
    return linhaId;
}

// Função para preencher o select de peças em uma linha específica
function preencherSelectPecas(linhaElement) {
    const selectPeca = linhaElement.querySelector('.select-peca');
    if (!selectPeca) {
        console.error('Elemento select-peca não encontrado');
        return;
    }
    
    // Limpa as opções existentes
    selectPeca.innerHTML = '';
    
    // Adiciona a opção padrão
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.disabled = true;
    defaultOption.selected = true;
    defaultOption.textContent = 'Selecione a peça...';
    selectPeca.appendChild(defaultOption);
    
    // Verifica se existem tipos de peças carregados
    if (tiposPecas && tiposPecas.length > 0) {
        // Adiciona as opções de peças
        tiposPecas.forEach(tipo => {
            const option = document.createElement('option');
            option.value = tipo.nome;
            option.textContent = tipo.nome;
            option.dataset.id = tipo.id;
            selectPeca.appendChild(option);
        });
    } else {
        console.warn('Nenhum tipo de peça disponível');
        const option = document.createElement('option');
        option.value = '';
        option.disabled = true;
        option.textContent = 'Nenhuma peça disponível';
        selectPeca.appendChild(option);
    }
    
    // Habilita o select
    selectPeca.disabled = false;
    
    // Remove o Select2 se já estiver inicializado
    if ($(selectPeca).hasClass('select2-hidden-accessible')) {
        $(selectPeca).select2('destroy');
    }
    
    // Inicializa o Select2
    $(selectPeca).select2({
        theme: 'bootstrap-5',
        width: '100%',
        dropdownAutoWidth: true,
        dropdownParent: document.body,
        minimumResultsForSearch: 0,
        placeholder: 'Selecione a peça...',
        dropdownCssClass: 'select2-dropdown-below',
        containerCssClass: 'select2-container--bootstrap-5',
        selectionCssClass: 'form-select',
        dropdownCss: {
            'z-index': '99999',
            'position': 'absolute'
        }
    });
}

// Função para remover uma linha de peça
function removerLinhaPeca(id) {
    const linha = document.getElementById(id);
    if (linha) {
        linha.remove();
    }
}

// Função para inicializar os eventos de uma linha
function inicializarEventosLinha(linha) {
    if (!linha) return;
    
    // Botão de usar manual
    const btnUsarManual = linha.querySelector('.btn-usar-manual');
    const inputDefeito = linha.querySelector('.input-defeito-manual');
    const inputHidden = linha.querySelector('.input-defeito-hidden');
    const selectDefeito = linha.querySelector('.select-defeito');
    
    if (btnUsarManual && inputDefeito && inputHidden) {
        btnUsarManual.addEventListener('click', function() {
            if (inputDefeito.value.trim() !== '') {
                inputHidden.value = inputDefeito.value.trim();
                inputDefeito.value = '';
                this.textContent = 'Alterar';
                this.classList.remove('btn-outline-secondary');
                this.classList.add('btn-outline-success');
                
                // Seleciona a opção manual
                if (selectDefeito) {
                    // Remove a opção manual se já existir
                    const opcaoManual = Array.from(selectDefeito.options).find(
                        opt => opt.value === 'manual' && opt.text === inputHidden.value
                    );
                    
                    if (opcaoManual) {
                        opcaoManual.remove();
                    }
                    
                    // Adiciona a nova opção manual
                    const novaOpcao = new Option(inputHidden.value, 'manual');
                    selectDefeito.add(novaOpcao);
                    selectDefeito.value = 'manual';
                }
            } else {
                alert('Por favor, digite um defeito antes de confirmar.');
                inputDefeito.focus();
            }
        });
    }
    
    // Evento de tecla Enter no campo de defeito manual
    if (inputDefeito) {
        inputDefeito.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                if (btnUsarManual) {
                    btnUsarManual.click();
                }
            }
        });
    }
}

// Função para atualizar os defeitos quando uma peça é selecionada
function atualizarDefeitos(selectElement) {
    // Encontra a linha da peça mais próxima (usando a classe correta)
    const pecaRow = selectElement.closest('.card-peca') || selectElement.closest('.card');
    if (!pecaRow) {
        console.error('Linha da peça não encontrada');
        return;
    }
    
    // Obtém o ID da peça selecionada
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const pecaId = selectedOption ? selectedOption.dataset.id : null;
    
    const selectDefeito = pecaRow.querySelector('.select-defeito');
    const inputManual = pecaRow.querySelector('.input-defeito-manual');
    const btnUsarManual = pecaRow.querySelector('.btn-usar-manual');
    const inputHidden = pecaRow.querySelector('.input-defeito-hidden');
    
    if (!selectDefeito) {
        console.error('Elemento select de defeito não encontrado');
        return;
    }
    
    // Remove o Select2 se já estiver inicializado
    if ($(selectDefeito).hasClass('select2-hidden-accessible')) {
        $(selectDefeito).select2('destroy');
    }
    
    // Desabilita o select de defeitos e mostra mensagem de carregamento
    selectDefeito.innerHTML = '<option value="" disabled selected>Carregando defeitos...</option>';
    selectDefeito.disabled = true;
    
    // Desabilita temporariamente o campo de defeito manual
    if (inputManual) {
        inputManual.disabled = true;
        inputManual.value = '';
    }
    
    // Desabilita temporariamente o botão de usar manual
    if (btnUsarManual) {
        btnUsarManual.disabled = true;
        btnUsarManual.textContent = 'Usar';
        btnUsarManual.classList.remove('btn-outline-success');
        btnUsarManual.classList.add('btn-outline-secondary');
    }
    
    // Limpa o valor do campo oculto de defeito manual
    if (inputHidden) {
        inputHidden.value = '';
    }
    
    if (pecaId) {
        // Faz a requisição para buscar os defeitos da peça
        fetch(`/api/pecas/${pecaId}/defeitos`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro ao carregar defeitos: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(defeitos => {
                // Limpa o select
                selectDefeito.innerHTML = '';
                
                // Adiciona a opção padrão
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.disabled = true;
                defaultOption.selected = true;
                defaultOption.textContent = 'Selecione o defeito...';
                selectDefeito.appendChild(defaultOption);
                
                // Adiciona a opção para digitar manualmente
                const manualOption = document.createElement('option');
                manualOption.value = 'manual';
                manualOption.textContent = 'Digitar defeito manualmente...';
                selectDefeito.appendChild(manualOption);
                
                // Adiciona um separador
                const separator = document.createElement('option');
                separator.disabled = true;
                separator.textContent = '──────────────';
                selectDefeito.appendChild(separator);
                
                // Adiciona os defeitos retornados
                if (Array.isArray(defeitos) && defeitos.length > 0) {
                    defeitos.forEach(defeito => {
                        const option = document.createElement('option');
                        option.value = defeito;
                        option.textContent = defeito;
                        selectDefeito.appendChild(option);
                    });
                } else {
                    const noDefeitos = document.createElement('option');
                    noDefeitos.disabled = true;
                    noDefeitos.selected = true;
                    noDefeitos.textContent = 'Nenhum defeito cadastrado';
                    selectDefeito.appendChild(noDefeitos);
                }
                
                // Habilita o select
                selectDefeito.disabled = false;
                
                // Configuração do Select2 para garantir que o dropdown seja posicionado corretamente
                const select2Config = {
                    theme: 'bootstrap-5',
                    width: '100%',
                    dropdownParent: $(selectDefeito).closest('.card-body'), // Usa o card-body como container pai
                    minimumResultsForSearch: 0,
                    placeholder: 'Selecione o defeito...',
                    allowClear: true,
                    dropdownAutoWidth: false,
                    dropdownCss: {
                        'z-index': '999999 !important',
                        'position': 'absolute !important',
                        'width': '100% !important',
                        'box-sizing': 'border-box !important',
                        'left': '0 !important',
                        'top': '100% !important',
                        'margin-top': '4px !important',
                        'transform': 'none !important',
                        'will-change': 'transform !important'
                    },
                    containerCss: {
                        'position': 'relative',
                        'z-index': '1',
                        'width': '100%'
                    },
                    // Desativa o posicionamento automático do Select2
                    dropdownAutoWidth: false,
                    width: '100%',
                    // Desativa as transformações CSS que podem afetar o posicionamento
                    templateResult: function(data) {
                        // Remove qualquer transformação que possa estar sendo aplicada
                        const $result = $(data.element);
                        return $result.text();
                    },
                    templateSelection: function(data) {
                        // Remove qualquer transformação que possa estar sendo aplicada
                        const $selection = $(data.element);
                        return $selection.text();
                    }
                };
                
                // Remove o Select2 se já estiver inicializado
                if ($(selectDefeito).hasClass('select2-hidden-accessible')) {
                    $(selectDefeito).select2('destroy');
                }
                
                // Inicializa o Select2
                const $select = $(selectDefeito).select2(select2Config);
                
                // Ajusta o posicionamento do dropdown quando aberto
                $(document).on('select2:opening', function(e) {
                    if (e.target === selectDefeito) {
                        // Força o posicionamento correto antes de abrir o dropdown
                        const $container = $(selectDefeito).closest('.card-body');
                        $container.css({
                            'position': 'relative',
                            'z-index': '1'
                        });
                    }
                });

                $(document).on('select2:open', function(e) {
                    if (e.target === selectDefeito) {
                        const $dropdown = $select.data('select2').$dropdown;
                        if ($dropdown) {
                            // Remove qualquer estilo que possa estar afetando o posicionamento
                            $dropdown.attr('style', '');
                            
                            // Obtém a posição do select
                            const $selectElement = $(selectDefeito);
                            const selectRect = selectDefeito.getBoundingClientRect();
                            const windowHeight = window.innerHeight;
                            const windowWidth = window.innerWidth;
                            
                            // Calcula a posição correta
                            const containerOffset = $selectElement.offsetParent().offset();
                            const relativeTop = selectRect.top - containerOffset.top;
                            
                            // Aplica os estilos diretamente
                            $dropdown.css({
                                'position': 'absolute',
                                'top': (relativeTop + selectRect.height + 4) + 'px',
                                'left': '0',
                                'width': '100%',
                                'max-width': 'none',
                                'margin': '0',
                                'transform': 'none',
                                'z-index': '999999',
                                'display': 'block',
                                'opacity': '1'
                            });
                            
                            // Verifica se o dropdown está saindo da tela
                            const dropdownRect = $dropdown[0].getBoundingClientRect();
                            const spaceBelow = windowHeight - (selectRect.top + selectRect.height + dropdownRect.height);
                            const spaceAbove = selectRect.top - dropdownRect.height;
                            
                            if (spaceBelow < 0 && spaceAbove > 0) {
                                // Se não há espaço abaixo, mas há espaço acima, posiciona acima
                                $dropdown.addClass('select2-dropdown--above');
                                $dropdown.css('top', (relativeTop - dropdownRect.height - 4) + 'px');
                            } else {
                                $dropdown.removeClass('select2-dropdown--above');
                            }
                            
                            // Garante que o dropdown não ultrapasse a largura da janela
                            if (dropdownRect.left < 0) {
                                $dropdown.css('left', '0');
                            }
                            if (dropdownRect.right > windowWidth) {
                                $dropdown.css('right', '0');
                            }
                            
                            // Força o redesenho para garantir que os estilos sejam aplicados
                            $dropdown[0].offsetHeight;
                        }
                    }
                });
                
                // Ajusta o posicionamento quando a janela é redimensionada
                $(window).on('resize', function() {
                    if ($select.data('select2').isOpen()) {
                        $select.select2('close').select2('open');
                    }
                });
                
                // Habilita o campo de defeito manual
                if (inputManual) {
                    inputManual.disabled = false;
                }
                
                // Habilita o botão de usar manual
                if (btnUsarManual) {
                    btnUsarManual.disabled = false;
                }
                // Adiciona o evento de mudança para o modo manual
                $(selectDefeito).on('change', function() {
                    if (this.value === 'manual') {
                        if (inputManual) {
                            inputManual.focus();
                        }
                    } else if (inputHidden) {
                        // Limpa o valor do defeito manual quando seleciona uma opção da lista
                        inputHidden.value = '';
                    }
                });
            })
            .catch(error => {
                console.error('Erro ao carregar defeitos:', error);
                
                // Limpa e configura a mensagem de erro
                selectDefeito.innerHTML = '';
                const errorOption = document.createElement('option');
                errorOption.disabled = true;
                errorOption.selected = true;
                errorOption.textContent = 'Erro ao carregar defeitos';
                selectDefeito.appendChild(errorOption);
                
                // Habilita o select mesmo com erro para permitir usar o modo manual
                selectDefeito.disabled = false;
                
                // Habilita o botão de usar manual em caso de erro
                if (btnUsarManual) {
                    btnUsarManual.disabled = false;
                }
                
                // Habilita o campo de defeito manual em caso de erro
                if (inputManual) {
                    inputManual.disabled = false;
                }
                
                // Re-inicializa o Select2 mesmo com erro
                $(selectDefeito).select2({
                    theme: 'bootstrap-5',
                    width: '100%',
                    dropdownParent: $(selectDefeito).parent(),
                    dropdownAutoWidth: true,
                    dropdownParent: $(document.body),
                    minimumResultsForSearch: 0,
                    placeholder: 'Erro ao carregar'
                });
                
                // Mostra mensagem de erro para o usuário
                mostrarMensagem('Não foi possível carregar os defeitos. Você pode digitar o defeito manualmente.', 'warning');
            });
    } else {
        // Se nenhuma peça estiver selecionada
        selectDefeito.innerHTML = '';
        const option = document.createElement('option');
        option.disabled = true;
        option.selected = true;
        option.textContent = 'Selecione uma peça primeiro';
        selectDefeito.appendChild(option);
        selectDefeito.disabled = true;
        
        // Desabilita o botão de usar manual
        if (btnUsarManual) {
            btnUsarManual.disabled = true;
        }
        
        // Desabilita o campo de defeito manual
        if (inputManual) {
            inputManual.disabled = true;
            inputManual.value = '';
        }
        
        // Limpa o valor do campo oculto de defeito manual
        if (inputHidden) {
            inputHidden.value = '';
        }
    }
}

// Função para validar o formulário antes do envio
function validarFormulario(event) {
    let isValid = true;
    
    // Valida cada linha de peça
    const linhasPecas = document.querySelectorAll('.card[id^="peca-"]');
    if (linhasPecas.length === 0) {
        alert('Adicione pelo menos uma peça ao pedido.');
        event.preventDefault();
        return false;
    }
    
    linhasPecas.forEach(linha => {
        const selectPeca = linha.querySelector('.select-peca');
        const selectDefeito = linha.querySelector('.select-defeito');
        const inputHidden = linha.querySelector('.input-defeito-hidden');
        
        // Valida se a peça foi selecionada
        if (!selectPeca || !selectPeca.value) {
            alert('Por favor, selecione uma peça para todos os itens.');
            selectPeca?.focus();
            isValid = false;
            event.preventDefault();
            return;
        }
        
        // Valida se o defeito foi selecionado ou informado manualmente
        if ((!selectDefeito || !selectDefeito.value) && (!inputHidden || !inputHidden.value)) {
            alert('Por favor, selecione ou informe um defeito para todas as peças.');
            selectDefeito?.focus();
            isValid = false;
            event.preventDefault();
            return;
        }
        
        // Se estiver no modo manual, garante que o valor esteja no campo oculto
        if (selectDefeito?.value === 'manual' && inputHidden) {
            if (!inputHidden.value) {
                const inputManual = linha.querySelector('.input-defeito-manual');
                if (inputManual && inputManual.value.trim()) {
                    inputHidden.value = inputManual.value.trim();
                } else {
                    alert('Por favor, preencha o defeito manualmente.');
                    inputManual?.focus();
                    isValid = false;
                    event.preventDefault();
                    return;
                }
            }
        }
    });
    
    // Valida os campos do pedido
    const numeroPedido = document.getElementById('numero_pedido');
    const tecnico = document.getElementById('tecnico_nome');
    const linha = document.getElementById('linha');
    
    if (!numeroPedido || !numeroPedido.value.trim()) {
        alert('Por favor, informe o número do pedido.');
        numeroPedido?.focus();
        isValid = false;
        event.preventDefault();
        return false;
    }
    
    if (!tecnico || !tecnico.value) {
        alert('Por favor, selecione um técnico.');
        tecnico?.focus();
        isValid = false;
        event.preventDefault();
        return false;
    }
    
    if (!linha || !linha.value) {
        alert('Por favor, selecione uma linha.');
        linha?.focus();
        isValid = false;
        event.preventDefault();
        return false;
    }
    
    return isValid;
}
