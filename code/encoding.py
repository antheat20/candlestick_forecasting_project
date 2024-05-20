import pandas as pd

# Загрузка CSV файла с ценами акций
file_path = 'D:/code/data.csv'
data = pd.read_csv(file_path, delimiter=';')

# Правила кодирования свечей
def encode_candlestick(row):
    op, hp, lp, cp = row['op'], row['hp'], row['lp'], row['cp']
    if hp > op > cp > lp:
        return 'a'
    elif hp == op > cp > lp:
        return 'b'
    elif hp > op == cp > lp:
        return 'c'
    elif hp > op > cp == lp:
        return 'd'
    elif hp > cp > op > lp:
        return 'e'
    elif hp == cp > op > lp:
        return 'f'
    elif hp > cp == op > lp:
        return 'g'
    elif hp > cp > lp == op:
        return 'h'
    elif hp == op == cp > lp:
        return 'i'
    elif hp > op == cp == lp:
        return 'j'
    elif hp == cp > op == lp:
        return 'k'
    elif hp > op == lp == cp:
        return 'l'
    else:
        return None  # Случай, когда все четыре цены равны, не рассматривается

# Добавление нового столбца с закодированными свечами
data = data[['date', 'op', 'hp', 'lp', 'cp']]
data['code'] = data.apply(encode_candlestick, axis=1)

# Вывод результата на экран
print(data)

# Сохранение результата в новый CSV файл
output_path = 'D:/code/encoded_data.csv'
data.to_csv(output_path, index=False, sep=';', encoding='utf-8')

print(f'Закодированные данные сохранены в {output_path}')