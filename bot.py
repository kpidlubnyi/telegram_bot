from telegram import Update
from telegram.ext import Application, CommandHandler
import requests
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.environ.get('BOT_TOKEN')

async def start(update, context):
    await update.message.reply_text('Siema!')

async def help_command(update, context):
    await update.message.reply_text("Nie będę ci pomagał")

def get_currency(CUR):
    if len(CUR) != 3 or not isinstance(CUR, str):
        raise ValueError("Currency must be 3 symbols long!")
    
    CUR = CUR.strip().upper()
    
    try:
        response = requests.get(rf'https://api.nbp.pl/api/exchangerates/rates/C/{CUR}/?format=json')
        code, bid, ask = response.get('code'), response.get('rates')[0].get('bid'), response.get('rates')[0].get('ask')
        return f'{code}: {bid} / {ask}'
    except requests.exceptions.JSONDecodeError:
        pass

async def currency(update, context):
    if context.args:
        cur = ' '.join(context.args)
        
    response = get_currency(cur)
    await update.message.reply_text(response)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('currency', currency))

    PORT = int(os.environ.get('PORT', 8000))
    application.run_webhook(
        listen = '0.0.0.0',
        port=PORT,
        webhook_url=f'https://telegram-bot-id0a.onrender.com'
    )

if __name__ == '__main__':
    main()