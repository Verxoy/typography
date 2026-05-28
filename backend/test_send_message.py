import requests

print("📤 Тест отправки сообщения...")

response = requests.post(
    'http://127.0.0.1:8000/api/send-message/',
    json={
        'name': 'Иван Иванов',
        'email': 'ivan@example.com',
        'phone': '+79991234567',
        'message': 'Привет! Хочу заказать визитки.'
    }
)

print(f"✅ Статус: {response.status_code}")
print(f"📦 Ответ: {response.json()}")