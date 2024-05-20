import pandas as pd

# Загрузка данных из файла pattern_set.csv
pattern_set_file_path = 'pattern_set.csv'
p_set = pd.read_csv(pattern_set_file_path, delimiter=';')

# Определение функции whether_sub, которая проверяет, является ли последовательность X подпоследовательностью Y
def whether_sub(X, Y):
    m, n = len(X), len(Y)
    if m > n:
        return 0
    i, k = 0, 0
    while i < m:
        if k == n:
            return 0
        for j in range(k, n):
            if X[i] == Y[j]:
                i += 1
                k = j + 1
                break
            elif j == n - 1:
                return 0
    return 1

# Создание набора записей паттернов
def create_pr_set(p_set):
    pr_set = []  # Инициализация списка для хранения записей паттернов
    n = len(p_set)  # Получение количества паттернов в наборе
    for i in range(n):
        same_trend_num = 0  # Инициализация счетчика для совпадающих трендов
        o_num = 0  # Инициализация счетчика для случаев подпоследовательностей
        S_i = p_set.iloc[i]['Segment']  # Извлечение сегмента S_i для текущего паттерна
        Trend_i = p_set.iloc[i]['Trend']  # Извлечение тренда Trend_i для текущего паттерна
        for j in range(n):
            S_j = p_set.iloc[j]['Segment']  # Извлечение сегмента S_j для сравниваемого паттерна
            Trend_j = p_set.iloc[j]['Trend']  # Извлечение тренда Trend_j для сравниваемого паттерна
            is_sub = whether_sub(S_i, S_j)  # Проверка, является ли S_i подпоследовательностью S_j
            if is_sub:
                o_num += 1  # Увеличение счетчика подпоследовательностей
                if Trend_i == Trend_j:
                    same_trend_num += 1  # Увеличение счетчика совпадающих трендов
            print(f'Comparing S_i: {S_i} with S_j: {S_j}, is_sub: {is_sub}, o_num: {o_num}, same_trend_num: {same_trend_num}')
        PACC = (same_trend_num / o_num) * 100 if o_num != 0 else 0  # Вычисление точности паттерна (PACC) в процентах
        pr_set.append({
            'S': S_i,  # Сегмент паттерна
            'Trend': Trend_i,  # Тренд паттерна
            'oNum': o_num,  # Количество раз, когда паттерн является подпоследовательностью других паттернов
            'sameTrendNum': same_trend_num,  # Количество совпадений трендов
            'PACC': PACC  # Точность паттерна в процентах
        })
    return pr_set

# Создание набора записей паттернов
pr_set = create_pr_set(p_set)

# Преобразование в DataFrame для удобного отображения и записи в файл
pr_set_df = pd.DataFrame(pr_set)

# Вывод результата на экран
print(pr_set_df)

# Запись результата в CSV файл
pr_set_df.to_csv('pattern_record_set.csv', index=False, sep=';')

# Определение функции прогнозирования
def forecast_next_trend(current_pattern, pr_set):
    matching_patterns = []
    
    # Поиск паттернов, которые являются подпоследовательностями последнего паттерна
    for index, row in pr_set.iterrows():
        pattern = row['S']
        trend = row['Trend']
        pacc = row['PACC']

        if whether_sub(current_pattern, pattern):
            matching_patterns.append((pattern, trend, pacc))
            print(f'Найденный совпадавший паттерн: {pattern}, Trend: {trend}, PACC: {pacc}')
    
    if not matching_patterns:
        return "Нет совпадающих паттернов для прогноза"
    
    # Выбор паттерна с наибольшей точностью (PACC)
    matching_patterns.sort(key=lambda x: x[2], reverse=True)
    best_match = matching_patterns[0]
    
    return best_match[1]

# Получение последнего сегмента
current_sequence = p_set['Segment'].iloc[-1]

print(f'Последний сегмент для прогнозирования: {current_sequence}')

# Прогнозирование на основе последнего сегмента
predicted_trend = forecast_next_trend(current_sequence, pr_set_df)

print(f'Прогнозируемый тренд для последнего сегмента ({current_sequence}): {predicted_trend}')