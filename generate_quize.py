import json
import os

from openai import AsyncOpenAI

from prompt import prompt_template
from datetime import datetime

TOKEN = 'caila:token'
openai = AsyncOpenAI(
    api_key=TOKEN,
    base_url="https://caila.io/api/adapters/openai"
)

async def fetch_completion(prompt: str):
    try:
        res = await openai.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="just-ai/openai-proxy/gpt-4o-mini",
            temperature=1,
            response_format={"type": "json_object"},
            stream=False
        )

        content = res.choices[0].message.content

        return content
    except Exception as e:
        print(f"error {e}")
        return None

async def generate_quiz():
    day_of_week = datetime.now().strftime('%A')

    topics = {
        'Monday': "Machine Learning уровень средний",
        'Tuesday': "Back-End Python, сети, базы данных на python уровень средний/сложный",
        'Wednesday': "Product Management, суть познакомить с разными терминами",
        'Thursday': "DevOps начальный уровень linux",
        'Friday': "Algorithms средний/продвинутый уровень",
        'Saturday': "Product Management, суть познакомить с разными терминами",
        'Sunday': "Mobile Development, уровень senior"
    }
    topic = topics.get(day_of_week, "General Knowledge")

    if day_of_week not in ['Wednesday', 'Saturday']:
        used_topics = load_used_topics(day_of_week)
    else:
        used_topics = load_used_topics('Bulat_theme')

    prompt = prompt_template % (topic, used_topics)
    quiz = await fetch_completion(prompt)
    quiz_json = json.loads(quiz)
    if day_of_week not in ['Wednesday', 'Saturday']:
        save_used_topic(day_of_week, quiz_json['question'])
    else:
        save_used_topic(day_of_week, quiz_json['question'])
    return quiz_json


def load_used_topics(day_of_week):
    filename = f'{day_of_week}.txt'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return f.read()
    return ''

def save_used_topic(day_of_week, question):
    filename = f'{day_of_week}.txt'
    with open(filename, 'a') as f:
        f.write(question + "\n")
