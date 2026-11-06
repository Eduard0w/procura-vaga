import html

from telegram import Bot
from telegram.request import HTTPXRequest
from model.job import Job


def create_bot(bot_token):
    rede = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    return Bot(token=bot_token, request=rede)


def format_job_message(job: Job):
    return (
        f"<b>Título:</b> {html.escape(str(job.title))}\n"
        f"<b>Empresa:</b> {html.escape(str(job.company))}\n"
        f"<b>Local:</b> {html.escape(str(job.zone))}\n"
        f"<b>Type:</b> {html.escape(str(job.work_mode))}\n"
        f"<b>Fonte:</b> {html.escape(str(job.source))}\n\n"
        f'<a href="{html.escape(str(job.url), quote=True)}">Ver Vaga</a>'
    )


async def send_job_notification(bot: Bot, job: Job, chat_id):
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=format_job_message(job),
            parse_mode="HTML"
        )
        return True
    except Exception as exc:
        print(f"Erro ao enviar vaga {job.title}: {exc}")
        return False
