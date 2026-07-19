from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest

# Adicionar a tipagem correta ajuda o Python e evita problemas de execução
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Verifica se a mensagem existe antes de tentar responder
       if update.message:
           await update.message.reply_text('Olá! Eu sou um bot, vou te ajudar mandando estágios encontrados por mim! :).')
       else:
           # Opcional: logar ou lidar com o caso onde não há mensagem (ex: se o comando for acionado de forma inesperada)
           print("Recebido comando /start sem uma mensagem associada.")


def create_bot(bot_token):
    # Criamos uma configuração de rede mais "paciente" para evitar o erro de TimedOut
    config_rede = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)

    # Cria a aplicação injetando a configuração de rede
    application = Application.builder().token(bot_token).request(config_rede).build()

    # Adiciona o handler para o comando /start
    application.add_handler(CommandHandler("start", start))

    # Inicia o bot
    print("Bot iniciado... Pressione Ctrl+C para parar.")
    return application

async def send_job_notifications(application: Application, jobs_to_send, chat_id):
    if not jobs_to_send:
        print("Nenhuma nova vaga para enviar.")
        return

    for job in jobs_to_send:
        message_text = (
            f"*Título:* {job.title}\n"
            f"*Empresa:* {job.company}\n"
            f"*Local:* {job.zone}\n"
            f"*Type:* {job.work_mode}"
            f"*Fonte:* {job.source}\n\n"
            f"[Ver Vaga]({job.url})"
        )
        try:
            await application.bot.send_message(
                chat_id=chat_id,
                text=message_text,
                parse_mode='Markdown'
            )
            print(f"Vaga enviada: {job.title}")
        except Exception as e:
            print(f"Erro ao enviar vaga {job.title}: {e}")
