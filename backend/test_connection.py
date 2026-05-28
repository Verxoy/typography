import pyodbc

# Параметры подключения
server = 'localhost'
database = 'Typography_db'
username = 'typography_login'  # Или 'sa'
password = 'TempPass123!'      # Ваш пароль

# Строка подключения
conn_str = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)

print("🔄 Попытка подключения к SQL Server...")
print(f"   Сервер: {server}")
print(f"   База данных: {database}")
print(f"   Пользователь: {username}")

try:
    conn = pyodbc.connect(conn_str)
    print("\n✅ Подключение успешно!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    version = cursor.fetchone()[0]
    print(f"\n📊 Версия SQL Server:\n{version}")
    
    cursor.execute("SELECT DB_NAME()")
    db_name = cursor.fetchone()[0]
    print(f"\n📁 Текущая база данных: {db_name}")
    
    conn.close()
    print("\n Соединение закрыто.")
    
except Exception as e:
    print(f"\n❌ Ошибка подключения: {e}")
    print("\n💡 Возможные причины:")
    print("   1. Неверный логин или пароль")
    print("   2. SQL Server не запущен")
    print("   3. База данных не существует")
    print("   4. Неправильное имя сервера (попробуйте .\\SQLEXPRESS)")