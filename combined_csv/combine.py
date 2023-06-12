import os
import sqlite3
import csv

def combine(csv_file1,csv_file2):
    with open(csv_file1, "r", newline="") as file1:
        reader1 = csv.reader(file1)
        data1 = list(reader1)

    # Открываем второй CSV-файл для чтения
    with open(csv_file2, "r", newline="") as file2:
        reader2 = csv.reader(file2)
        # for row in reader2:
        # # Замена пустого места на NULL
        #     processed_row = [value if value != '' else None for value in row]   
        next(reader2)
        data2 = list(reader2)

    # Объединяем данные из двух файлов
    merged_data = data1 + data2

    return merged_data

# Путь к папке hh_json_parser
hh_folder = "../hh_json_parser"
# Путь к папке enbek-parser
enbek_folder = "../enbek_parser"

almaty_vac1 = os.path.join(enbek_folder, "enbek_Алмата_vacancies.csv")
almaty_vac2 = os.path.join(hh_folder, "hh_Алмата_vacancies.csv")

with open('алмата_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Астана_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Астана_vacancies.csv")
with open('астана_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Атырау_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Атырау_vacancies.csv")
with open('атырау_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Актобе_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Актобе_vacancies.csv")
with open('актобе_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Актау_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Актау_vacancies.csv")
with open('актау_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Жезказган_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Жезказган_vacancies.csv")
with open('жезказган_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Караганда_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Караганда_vacancies.csv")
with open('караганда_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Кокшетау_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Кокшетау_vacancies.csv")
with open('кокшетау_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Костанай_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Костанай_vacancies.csv")
with open('костанай_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Кызылорда_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Кызылорда_vacancies.csv")
with open('кызылорда_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Павлодар_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Павлодар_vacancies.csv")
with open('павлодар_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Петропавловск_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Петропавловск_vacancies.csv")
with open('петропавловск_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Семей_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Семей_vacancies.csv")
with open('семей_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Талдыкорган_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Талдыкорган_vacancies.csv")
with open('талдыкорган_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Тараз_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Тараз_vacancies.csv")
with open('тараз_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Темиртау_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Темиртау_vacancies.csv")
with open('темиртау_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Уральск_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Уральск_vacancies.csv")
with open('уральск_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Усть-Каменогорск_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Усть-Каменогорск_vacancies.csv")
with open('усть-каменогорск_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Шымкент_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Шымкент_vacancies.csv")
with open('шымкент_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

almaty_vac1 = os.path.join(hh_folder, "hh_Экибастуз_vacancies.csv")
almaty_vac2 = os.path.join(enbek_folder, "enbek_Экибастуз_vacancies.csv")
with open('экибастуз_vacancies.csv', "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(combine(almaty_vac1,almaty_vac2))

database_path = os.path.join("..", "tg_bot", "vacancies.db")
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

cursor.execute("DELETE FROM алмата_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "алмата_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO алмата_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM астана_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "астана_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO астана_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM атырау_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "атырау_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO атырау_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM жезказган_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "жезказган_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO жезказган_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM караганда_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "караганда_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO караганда_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM кокшетау_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "кокшетау_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO кокшетау_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM костанай_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "костанай_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO костанай_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM кызылорда_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "кызылорда_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO кызылорда_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM павлодар_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "павлодар_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO павлодар_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM петропавловск_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "петропавловск_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO петропавловск_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM семей_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "семей_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO семей_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM талдыкорган_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "талдыкорган_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO талдыкорган_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM тараз_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "тараз_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO тараз_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM темиртау_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "темиртау_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO темиртау_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM уральск_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "уральск_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO уральск_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute('DELETE FROM "усть-каменогорск_vacancies"')
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "усть-каменогорск_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany('INSERT INTO "усть-каменогорск_vacancies" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', csv_data)
conn.commit()

cursor.execute("DELETE FROM шымкент_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "шымкент_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO шымкент_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM экибастуз_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "экибастуз_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO экибастуз_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM актау_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "актау_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO актау_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()

cursor.execute("DELETE FROM актобе_vacancies")
conn.commit()
csv_file_path = os.path.join("..", "combined_csv", "актобе_vacancies.csv")
with open(csv_file_path, 'r', newline='') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Пропуск заголовков столбцов, если они есть
    cursor.executemany("INSERT INTO актобе_vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", csv_data)
conn.commit()


#Добавить Актобе и Актау



