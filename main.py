from bot.telegram import create_bot, send_job_notifications
from crawler.search import search_job, filter_jobs
from model.mapper import mapper_job_save
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

TELEGRAM_CHAT_ID = os.getenv("CHAT_ID")
BOT_TOKEN = os.getenv("TOKEN_BOT")

async def main_loop():
    print("Iniciando ciclo de busca e notificação...")
    raw_jobs = search_job()  # Pega os dados da API
    filtered_jobs_dicts = filter_jobs(raw_jobs)  # Filtra os dados da API (ainda dicionários)
    newly_saved_jobs = mapper_job_save(filtered_jobs_dicts) # Salva novas vagas e retorna as salvas

    # Cria a instância do bot fora do loop para não recriar a cada ciclo
    application = create_bot(BOT_TOKEN)

    if newly_saved_jobs:
        print(f"Encontradas {len(newly_saved_jobs)} novas vagas. Enviando notificações...")
        await send_job_notifications(application, newly_saved_jobs, TELEGRAM_CHAT_ID)
    else:
        print("Nenhuma nova vaga encontrada neste ciclo.")


async def main():
    while True:
        await main_loop()
        print("Ciclo concluído. Aguardando para o próximo...")
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())
