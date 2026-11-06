from bot.telegram import create_bot, send_job_notification
from crawler.search import search_job, filter_jobs
from database.jobs import save_job
from model.mapper import get_new_jobs
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

TELEGRAM_CHAT_ID = os.getenv("CHAT_ID")
BOT_TOKEN = os.getenv("TOKEN_BOT")


def get_interval_seconds():
    try:
        return max(60, int(os.getenv("CHECK_INTERVAL_SECONDS", "14400")))
    except ValueError:
        return 14400


CHECK_INTERVAL_SECONDS = get_interval_seconds()


async def main_loop(bot):
    print("Iniciando ciclo de busca e notificação...")
    raw_jobs = search_job()
    filtered_jobs_dicts = filter_jobs(raw_jobs)
    new_jobs = get_new_jobs(filtered_jobs_dicts)

    if not new_jobs:
        print("Nenhuma nova vaga encontrada neste ciclo.")
        return

    print(f"Encontradas {len(new_jobs)} novas vagas. Enviando notificações...")

    for job in new_jobs:
        if await send_job_notification(bot, job, TELEGRAM_CHAT_ID):
            save_job(job)
            print(f"Vaga enviada e salva: {job.title}")
        else:
            print(f"Vaga não salva, será tentada novamente: {job.title}")


async def main():
    if not BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise RuntimeError("Configure TOKEN_BOT e CHAT_ID no ambiente ou no arquivo .env")

    bot = create_bot(BOT_TOKEN)
    await bot.initialize()

    try:
        while True:
            try:
                await main_loop(bot)
            except Exception as exc:
                print(f"Erro no ciclo de busca/notificação: {exc}")

            print(f"Ciclo concluído. Aguardando {CHECK_INTERVAL_SECONDS}s para o próximo...")
            await asyncio.sleep(CHECK_INTERVAL_SECONDS)
    finally:
        await bot.shutdown()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Encerrando...")
