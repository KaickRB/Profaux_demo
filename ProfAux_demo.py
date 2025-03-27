import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from messages import msg
from menus import buttons
import asyncio
import time
import mercadopago
from mysql.connector import pooling
import traceback


#Token necessário para acessar o Telebot via API
bot = telebot.TeleBot("API TOKEN", parse_mode='HTML', num_threads=10)


# Dados para realizar a conexão ao banco de dados MySQL

# Configurando o database
db_config = {
    "host": "host",
    "user": "user",
    "password": "password",
    "database": "database"}

# Configurações do pool de conexões
pool_config = {
    "pool_name": "pool_mysql",
    "pool_size": 25,  # número máximo de conexões simultâneas
    "pool_reset_session": True  # Redefinir a sessão após uma conexão ser liberada
}

# Criando o pool de conexões
connection_pool = pooling.MySQLConnectionPool(**pool_config, **db_config)

#Acessando a API do Mercado Pago para receber e verificar pagamentos
sdk = mercadopago.SDK('Nome do APP')
acess_token = 'Token de acesso'


#Função responsável por capturar e enviar para o setor de manutenção todos os erros inesperados que ocorrerem no telebot
def capturar_erros(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            traceback_str = traceback.format_exc()
            #Enviando erro completo ao canal do telegram
            bot.send_message(-1001987739620, f"""❌❌❌❌❌❌❌❌\n\n{traceback_str}\n\n""")

    return wrapper

# Gerar pagamentos (Os dados abaixo são todos fictícios)
@capturar_erros
def createPayment(call, infos):
    # Conexão ao banco de dados MySql
    con = connection_pool.get_connection()
    cursor = con.cursor()

    try:
        cursor.execute(f"""insert into transacoes
                    (id_usuario, id_mensagem, usuario, nome_usuario, link_pagamento, chave_pix, id_pagamento, valor_pagamento, plano)
                    values
                    ({call.from_user.id}, '{call.message.message_id}', '{call.from_user.username}', '{call.from_user.first_name}', 'vazio', 'vazio', '{'vazio'}', 'vazio', 'null');""")
        con.commit()
    except:
        pass

    # Definição das informaões e valores necessários para seguir o processo
    valor = infos[1]
    plano = infos[0]

    # Gerando pagamento
    payment_data = {
        "transaction_amount": valor,
        "description": f"Assinatura de nível {plano} do profaux",
        "payment_method_id": 'pix',
        "installments": 1,
        "payer": {
            "email": 'suporte@empresa.com'
        }
    }

    result = sdk.payment().create(payment_data)

    # Obtendo informações do pagamento
    payment_link = result['response']['point_of_interaction']['transaction_data']['ticket_url']
    pix_key = result['response']['point_of_interaction']['transaction_data']['qr_code']
    payment_id = result['response']['id']

    #Avisando ao setor financeiro que um novo pagamento foi gerado por um cliente
    bot.send_message(-1001832589391,
                     f"""Pagamento gerado!📈\n\nNome: 👩🏻‍🏫 {call.from_user.first_name} 👨🏽‍🏫\nUsername🪪: @{call.from_user.username}\nId 🔎: {call.from_user.id}\n\nValor 💶: {valor},00R$\nPlano 📊: {plano}\nId pagamento 🧩: {payment_id}\n\nLink Pagamento 🔗: {payment_link}\n\nChave pix 🔑: {pix_key}\n\nCódigo indicação 📥: empresa123""")

    # Registrando informações do pagamento no banco de dados para futuros acessos
    cursor.execute(f"""update transacoes
                        set link_pagamento = '{payment_link}', chave_pix = '{pix_key}', id_pagamento = '{payment_id}', valor_pagamento = '{valor}', nome_usuario = '{call.from_user.first_name}',usuario = '@{call.from_user.username}', plano = '{plano}', id_mensagem = '{call.message.message_id}'
                        where id_usuario = {call.from_user.id} and status_pagamento = 'pendente';""")
    con.commit()

    # Retornando informações para o cliente
    payment_infos = [payment_link, pix_key]

    cursor.close()
    con.close()
    return payment_infos

    #Também há uma função para a verificação de pagamentos, porém, não irei adicioná-la aqui, porque isso iria revelar todo o procedimento que é realizado para aprovar os pagamentos dos clientes do projeto.




#O Telebot costuma aguardar respostas dos usuários, isso gera um acúmulo no uso de Threads
#Essa função é responsável por fechar as Threads que o usuário deixa em aberto assim que ele acessa outros trechos do Telebot
def clearStep(call):
    return bot.clear_step_handler_by_chat_id(call.from_user.id), bot.answer_callback_query(call.id)


#Edição de mensagens simplificada, para melhorar a legibilidade do código
def edit_msg(call, msg, button_menu):
    try:
        return bot.edit_message_text(msg, call.from_user.id, call.message.id, reply_markup=button_menu)
    except:
        pass

#Mensagem inicial do Telebot
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, msg['menu_principal'], reply_markup=buttons('menu_principal'))


#Função responsável por identificar mensagens irrelevantes no chat, para que o usuário não precise excluí-las manualmente
@bot.message_handler(func=lambda message: True)
def limpaChat(message):
    print(f"{message.text}")
    time.sleep(0.5)
    bot.delete_message(message.chat.id, message.message_id)




#Decorador responsável por executar tarefas quando um botão é pressionado pelo usuário
@bot.callback_query_handler(func=lambda call: True)
def funcBotoes(call):
    print(call.data)
    if call.data[0:3] == 'mp_': #abrevição para MENU PRINCIPAL
        
        #Botões presentes no menu principal
        if call.data == 'mp_Menu_principal':
            asyncio.run(clearStep(call))
            
            edit_msg(call, msg['menu_principal'], buttons('menu_principal'))
        
        elif call.data == 'mp_Área_de_trabalho':
            asyncio.run(clearStep(call))
            
            edit_msg(call, msg['area_de_trabalho'], buttons('area_de_trabalho'))

        elif call.data == 'mp_Relatório_geral':
            pass
        
        elif call.data == 'mp_Suporte':
            pass

        elif call.data == 'mp_Apoie_o_ProfAux':
            asyncio.run(clearStep(call))
            
            edit_msg(call, msg['apoie_o_profaux'], buttons('apoie_o_profaux'))
        
        elif call.data == 'mp_Meu_plano':
            asyncio.run(clearStep(call))
            
            edit_msg(call, msg['meu_plano'], buttons('meu_plano'))

    elif call.data[0:3] == 'at': #ÁREA DE TRABALHO
        pass

    elif call.data[0:3] == 'ct_': #CENTRO DE TURMAS
        pass

    elif call.data[0:3] == 'tu_': #TURMA
        pass

    elif call.data[0:3] == 'mt_': #MÉTODOS AVALIATIVOS
        pass

    elif call.data[0:3] == 'ma_': #MÉTODO
        pass

    elif call.data[0:3] == 'ca_': #CAMPO AVALIATIVO
        pass

    elif call.data[0:3] == 'cf_': #CONFIGURAÇÕES
        pass

    elif call.data[0:3] == 'sf_': #SYSTEM FUNCTIONS
        pass





bot.infinity_polling()