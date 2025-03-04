import random
import string
import os
import asyncio
from flask import Flask, request, render_template_string
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

app = Flask(__name__)
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GROUP_LINK = "https://t.me/+2oxLmAzwvTM4MDgy"
current_password = ""

bot = Bot(token=TOKEN)
dp = Dispatcher()

def generate_password():
    """Tasodifiy 6 xonali parol yaratish"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def update_password():
    global current_password
    current_password = generate_password()
    print(f"Yangi maxfiy parol: {current_password}")

update_password()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Maxfiy Guruh Havolasi</title>
</head>
<body>
    <h2>Maxfiy guruhga kirish</h2>
    <form method="POST">
        <label for="password">Parolni kiriting:</label>
        <input type="text" id="password" name="password" required>
        <button type="submit">Tasdiqlash</button>
    </form>
    {% if message %}
        <p>{{ message }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        user_password = request.form.get('password')
        if user_password == current_password:
            message = f"To‘g‘ri! Guruh havolasi: <a href='{GROUP_LINK}'>Bu yerda</a>"
        else:
            message = "Noto‘g‘ri parol. Qaytadan urinib ko‘ring."
    return render_template_string(HTML_TEMPLATE, message=message)

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Salom! Guruh havolasini olish uchun maxfiy parolni yuboring.")

@dp.message()
async def check_password(message: Message):
    if message.text == current_password:
        await message.answer(f"To‘g‘ri! Guruh havolasi: {GROUP_LINK}")
    else:
        await message.answer("Noto‘g‘ri parol. Qaytadan urinib ko‘ring.")

async def run_bot():
    await dp.start_polling(bot)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host='0.0.0.0', port=5000)
