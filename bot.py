import pandas as pd
from twilio.rest import Client
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Configuração do Twilio
account_sid = "SEU_SID"
auth_token = "SEU_TOKEN"
client = Client(account_sid, auth_token)

# Configuração do Telegram
TELEGRAM_BOT_TOKEN = 'SEU_BOT_TOKEN'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Lista de números para envio
numeros_para_envio = [
    "NUMEROS",
]

# Comando /start para resposta inicial
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_first_name = message.from_user.first_name
    user_id = message.from_user.id
    user_username = message.from_user.username
    welcome_text = f"Opa, {user_first_name}! Bem-vindo(a) ao serviço de envio de SMS!\n\n🧾 Seu perfil:\n├👤 ID: {user_id}\n└@{user_username}\n\nEscolha uma opção abaixo👇"

    # Criação do teclado inline com opções
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Enviar SMS para números predefinidos📩", callback_data="enviar_sms_predefinidos"))
    markup.add(InlineKeyboardButton("Enviar SMS para números personalizados✉️", callback_data="enviar_sms_personalizado"))
    markup.row(
    InlineKeyboardButton('Ajuda', callback_data="ajuda"),
    InlineKeyboardButton('Desenvolvedor', url='https://t.me/GVsuporte')
)

    # Envia a mensagem de boas-vindas com o teclado inline
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# Callback para os botões inline
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "enviar_sms_predefinidos":
        # Solicita a mensagem a ser enviada para os números predefinidos
        msg = bot.send_message(call.message.chat.id, "Digite a mensagem que deseja enviar como SMS:")
        bot.register_next_step_handler(msg, processar_sms_predefinido)
    elif call.data == "enviar_sms_personalizado":
        # Solicita os números de telefone para enviar o SMS
        msg = bot.send_message(call.message.chat.id, "DIGITE OS NÚMEROS DE TELEFONES SEPARADOS POR VÍRGULA❗️\n\nExemplo: +5511999999999,+5521999999999):")
        bot.register_next_step_handler(msg, receber_numeros)
    elif call.data == "ajuda":
        msg = bot.send_message(call.message.chat.id, "Para enviar SMS para um número em específico selecione a opção:\nEnviar SMS para números personalizados✉️\n\nCaso prefira enviar para números já definidos pelo bot, selecione:\nEnviar SMS para números predefinidos📩")

# Processar a mensagem de SMS e enviar para os números predefinidos
def processar_sms_predefinido(message):

    corpo_mensagem = message.text  # Obtém o texto do SMS
    try:
        for numero in numeros_para_envio:
            # Enviar SMS usando Twilio
            msg = client.messages.create(
                to=numero,
                from_="+12563872998",  # Seu número Twilio
                body=corpo_mensagem
            )
            print(f'SMS enviado para {numero}: {msg.sid}')
        
        bot.reply_to(message, "SMS enviado com sucesso ✅")
    except Exception as e:
        bot.reply_to(message, f"⚠️Ocorreu um erro ao enviar o SMS⚠️\n\ncaso o erro persistir, informe sobre com o desenvolvedor❗️")

# Receber os números personalizados para o envio
def receber_numeros(message):
    numeros_digitados = message.text.split(",")  # Divide os números por vírgula
    msg = bot.send_message(message.chat.id, "Digite a mensagem que deseja enviar como SMS:")
    bot.register_next_step_handler(msg, processar_sms_personalizado, numeros_digitados)

# Processar a mensagem de SMS e enviar para os números personalizados
def processar_sms_personalizado(message, numeros_digitados):
    corpo_mensagem = message.text  # Obtém o texto do SMS
    try:
        for numero in numeros_digitados:
            # Enviar SMS usando Twilio
            msg = client.messages.create(
                to=numero.strip(),
                from_="+12563872998",  # Seu número Twilio
                body=corpo_mensagem
            )
            print(f'SMS enviado para {numero.strip()}: {msg.sid}')
        
        bot.reply_to(message, "SMS enviado com sucesso ✅")
    except Exception as e:
        bot.reply_to(message, f"⚠️Ocorreu um erro ao enviar o SMS⚠️\n\ncaso o erro persistir, informe sobre com o desenvolvedor❗️")

# Iniciar o bot
if __name__ == '__main__':
    bot.polling()
