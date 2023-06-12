from bs4 import BeautifulSoup

# Пример HTML-кода
html = """
<div>
    <p>Это текст блока, который содержит слово "Мера".</p>
    <p>Это другой текст без слова "Мера".</p>
</div>
"""

# Создаем объект BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Находим все блоки <p> и проверяем содержит ли хотя бы одно слово "Мера"
blocks = soup.find_all('p')
for block in blocks:
    if 'Мера' in block.get_text():
        print("Блок содержит слово 'Мера'")
        break
else:
    print("Блоки не содержат слово 'Мера'")