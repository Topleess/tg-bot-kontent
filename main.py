import asyncio

import requests

from generate_quize import generate_quiz

telegram_auth_token = "<bot:token>"
telegram_group_id = "suaitech"

def send_msg_on_telegram(quiz_data):
    telegram_api_url = f"https://api.telegram.org/bot{telegram_auth_token}/sendPoll"
    poll_data = {
        "chat_id": f"@{telegram_group_id}",
        "question": quiz_data['question'],
        "options": quiz_data['options'],
        "is_anonymous": True,
        "type": "quiz",
        "correct_option_id": quiz_data['correct_options_id'],
        "allows_multiple_answers": False,
        "explanation": quiz_data['explanation'],
        "message_thread_id": 314
    }
    print(poll_data['question'])
    tel_resp = requests.post(telegram_api_url, json=poll_data)

    if tel_resp.status_code == 200:
        print("INFO: Quiz has been sent on Telegram")
    else:
        print("ERROR: Could not send message", tel_resp.text)

async def main():
    quiz_data = await generate_quiz()
    if quiz_data:
        send_msg_on_telegram(quiz_data)

if __name__ == "__main__":
    asyncio.run(main())

