import psycopg2
import csv
import re  

def connect():
    return psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password= '***  ' , 
        database='l10'
)

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            phone VARCHAR(20)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def validate_phone(phone):
    pattern = r"^87\d{2}$" 
    if re.match(pattern, phone):
        return True
    return False

def insert_from_console():
    conn = connect()
    cur = conn.cursor()
    name = input("Введите имя: ")
    
    while True:
        phone = input("Введите телефон (начинается с 87 и состоит из 4 цифр): ")
        if validate_phone(phone):
            break
        else:
            print("Неверный формат номера телефона. Он должен начинаться с 87 и состоять из 4 цифр.")
    
    cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Проверка телефона для каждой строки
            if validate_phone(row['phone']):
                cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (row['first_name'], row['phone']))
            else:
                print(f"Неверный формат телефона для пользователя {row['first_name']} - {row['phone']}")
    conn.commit()
    cur.close()
    conn.close()

def insert_many_console():
    conn = connect()
    cur = conn.cursor()
    while True:
        name = input("Введите имя (или 'q' для выхода): ").strip()
        if name.lower() == 'q':
            break
        
        # Проверка телефона
        while True:
            phone = input("Введите телефон (начинается с 87 и состоит из 4 цифр): ").strip()
            if validate_phone(phone):
                break
            else:
                print("Неверный формат номера телефона")
        
        cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

def update_user():
    conn = connect()
    cur = conn.cursor()
    name = input("Введите имя пользователя для обновления: ")
    choice = input("Что  хотите обновить? (name/phone): ")
    if choice == 'name':
        new_name = input("Введите новое имя: ")
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, name))
    elif choice == 'phone':
        new_phone = input("Введите новый телефон: ")
        while not validate_phone(new_phone):
            print("Неверный формат телефона")
            new_phone = input("Введите новый телефон: ")
        cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s", (new_phone, name))
    conn.commit()
    cur.close()
    conn.close()

def query_users():
    conn = connect()
    cur = conn.cursor()
    print("1. Показать всех пользователей")
    print("2. Поиск по имени")
    print("3. Поиск по номеру")
    choice = input("Выбор: ")
    if choice == '1':
        cur.execute("SELECT * FROM phonebook")
    elif choice == '2':
        name = input("Введите имя: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
    elif choice == '3':
        phone = input("Введите телефон: ")
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def delete_user():
    conn = connect()
    cur = conn.cursor()
    delete_by = input("Удалить по (name/phone): ").strip().lower()
    value = input("Введите значение: ").strip()

    if delete_by == "name":
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (value,))
    elif delete_by == "phone":
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (value,))
    else:
        print("Неверный выбор.")
        conn.close()
        return

    conn.commit()
    cur.close()
    conn.close()

def main():
    create_table()
    while True:
        print("\n=== PhoneBook Menu ===")
        print("1. Добавить запись вручную")
        print("2. Загрузить из CSV")
        print("3. Показать/найти пользователей")
        print("4. Обновить запись")
        print("5. Удалить запись")
        print("6. Добавить несколько пользователей")
        print("0. Выход")
        choice = input("Выбор: ")
        if choice == '1':
            insert_from_console()
        elif choice == '2':
            filename = input("Введите путь к CSV файлу: ")
            insert_from_csv(filename)
        elif choice == '3':
            query_users()
        elif choice == '4':
            update_user()
        elif choice == '5':
            delete_user()
        elif choice == '6':
            insert_many_console()
        elif choice == '0':
            break
        else:
            print("Неверный выбор!")

if __name__ == '__main__':
    main()
