from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


#Todos os menus de botões são organizados e tratados por este módulo, com o propósito de encurtar o código principal e torná-lo mais eficaz.

#Classe responsável por gerar menus com botões e agilizar esse processo para o código principal
class generate_buttons:
    def __init__(self, button):
        self.button = button
        self.markup = InlineKeyboardMarkup()
    
    def menu(self):
        for n in range(0, len(self.button), 2):
            #Adicionando os botões via Markup e fazendo todas as formatações str necessárias para identificar os botões que devem ser usados
            try:
                self.markup.add(InlineKeyboardButton(self.button[n][3:].replace('_', ' '), callback_data=self.button[n]), InlineKeyboardButton(self.button[n+1][3:].replace('_', ' '), callback_data=self.button[n+1]))
            except:
                if len(self.button[n]) == 2:
                    self.markup.add(InlineKeyboardButton(self.button[n][0][3:].replace('_', ' '), callback_data=self.button[n][1]))
                else:
                    self.markup.add(InlineKeyboardButton(self.button[n][3:].replace('_', ' '), callback_data=self.button[n]))
        return self.markup


def buttons(menu):
    buttons_menu = generate_buttons(defaults[menu])
    return buttons_menu.menu()



#Significado das iniciais usadas no código:

       #    mp = MENU PRINCIPAL 
       #    at = ÁREA DE TRABALHO
       #    st = SETOR DE TURMAS
       #    tu = TURMA

       #    ma = MÉTODOS AVALIATIVOS
       #    mt = MÉTODO
       #    ca = CAMPO AVALIATIVO
       #    cf = CONFIGURAÇÕES
       #    sf = SYSTEM FUNCTIONS


#Este dicionário organiza os menus de botões para que a função buttons() possa chamá-los
#Obs: sem este dicionário, o código seria muito longo, esse dicionário ajuda a encurtar e melhorar a legibilidade do código para facilitar futuras manutenções
defaults = {

    'menu_principal': ['mp_Área_de_trabalho', 'mp_Relatório_geral', 'mp_Suporte', 'mp_Apoie_o_ProfAux', 'mp_Meu_plano'],
    'area_de_trabalho': ['at_Minhas_turmas', 'at_Métodos_avaliativos', 'at_Anotações', 'at_Configurações', ['mp_Voltar', 'mp_Menu_principal']],
    'minhas_turmas': ['st_Adicionar_turma'],
    'metodos_avaliativos': ['ma_Adicionar_método'],
    'anotacoes': ['sf_Editar_anotações'],
    'configuracoes': ['cf_Média_verde', 'cf_Canais_de_recebimento', 'cf_Alterar_apelido', 'cf_Alterar_divisor'],
    'canais_de_recebimento': ['cf_Meus_canais', 'cf_Recebimento'],
    'meus_canais': ['cf_Adicionar email', 'cf_Confirmar email'],
    'recebimento':['cf_attemail', 'cf_attpv'], # 'cf_attcanal'
    'turma': ['tu_Adicionar_turma', 'tu_Adicionar_aluno', 'tu_Remover_aluno', 'tu_Renomear_aluno', 'tu_Campo_avaliativo', 'tu_Excluir_turma', 'tu_Renomear_turma'],
    'metodo_avaliativo': ['mt_Adicionar_método', 'mt_Adicionar_questão', 'mt_Remover_questão', 'mt_Renomear_método', 'mt_Alterar_descrição', 'mt_Excluir_método'],
    'campo_avaliativo': ['ca_Avaliar', 'ca_Pontuações_da_turma'],
    'avaliar': ['ca_Avaliação_individual', 'ca_Avaliação_geral', 'ca_Selecionar_método'],
    
    'apoie_o_profaux': [['mp_Voltar', 'mp_Menu_principal']],

    'meu_plano': [['mp_Voltar', 'mp_Menu_principal']]

    }
