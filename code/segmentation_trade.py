import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Загрузка данных
file_path = 'D:/code/encoded_data.csv'
data = pd.read_csv(file_path, delimiter=';')

# Преобразование столбца даты в формат datetime
data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y')

# Извлечение данных
dates = data['date'].tolist()
open_prices = data['op'].tolist()
high_prices = data['hp'].tolist()
low_prices = data['lp'].tolist()
close_prices = data['cp'].tolist()
codes = data['code'].tolist()

# Определение точек изменения цены с учетом кодов свечей
def identify_change_points(prices, codes):
    change_points = [(0, 'Начало', codes[0])]  # Начальная точка
    for i in range(1, len(prices) - 1):
        cpleft = prices[i - 1]
        cpA = prices[i]
        cpright = prices[i + 1]

        if cpleft != cpA or cpA != cpright or codes[i] != codes[i-1] or codes[i] != codes[i+1]:
            change_points.append((i, codes[i], 'Change'))

    change_points.append((len(prices) - 1, 'Конец', codes[-1]))  # Конечная точка
    return change_points

change_points = identify_change_points(close_prices, codes)

# Исключение последнего сегмента с конечной точкой
change_points = change_points[:-1]

# Сегментация последовательности цен закрытия и определение трендов
def segment_and_label_trends(prices, change_points):
    segments = []
    trends = []
    for i in range(1, len(change_points)):
        start = change_points[i - 1][0]
        end = change_points[i][0]
        segment = prices[start:end + 1]
        segments.append(segment)
        trend = determine_trend(segment)
        trends.append(trend)

    return segments, trends

def determine_trend(segment):
    if segment[0] < segment[-1]:
        return 'Up'
    elif segment[0] > segment[-1]:
        return 'Down'
    else:
        return 'Equal'

segments, trends = segment_and_label_trends(close_prices, change_points)

# Формирование свечных паттернов
def form_patterns(change_points, trends):
    patterns = []
    for i in range(len(trends)):
        pattern = {
            'Segment': f'{change_points[i][1]}-{change_points[i + 1][1]}',
            'Trend': trends[i]
        }
        patterns.append(pattern)
    return patterns

patterns = form_patterns(change_points, trends)

# Преобразование в DataFrame для удобного отображения
patterns_df = pd.DataFrame(patterns)

# Вывод результата на экран
print(patterns_df)

# Запись результата в CSV файл
patterns_df.to_csv('D:/code/pattern_set.csv', index=False, sep=';')

# Создание графика
fig, ax = plt.subplots(figsize=(14, 8))

# Добавление свечей
for i in range(len(dates)):
    color = 'green' if close_prices[i] >= open_prices[i] else 'red'
    ax.plot([dates[i], dates[i]], [low_prices[i], high_prices[i]], color=color)
    ax.plot([dates[i], dates[i]], [open_prices[i], close_prices[i]], color=color, linewidth=6)

# Добавление линии цен закрытия
ax.plot(dates, close_prices, label='Цены закрытия', color='blue')

# Добавление меток для кодов свечей, исключая конечную точку
for point in change_points:
    date = dates[point[0]]
    ax.text(date, close_prices[point[0]], point[1], fontsize=8, color='black', ha='right')

# Форматирование даты на оси X
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=45)

plt.xlabel('Дата')
plt.ylabel('Цена')
plt.title('Свечной временной ряд с ценами закрытия')
plt.legend()
plt.tight_layout()
plt.show()