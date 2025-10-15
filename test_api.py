"""
Тестирование API Reya для проверки гипотезы о лимите данных
"""
import requests
import json

def test_api_structure():
    """Тест 1: Проверка структуры ответа API"""
    print("=" * 60)
    print("ТЕСТ 1: Структура ответа API")
    print("=" * 60)
    
    url = "https://api.reya.xyz/api/incentives/leaderBoard/total"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Анализ структуры
            print(f"\n📊 Структура ответа:")
            print(f"   Ключи верхнего уровня: {list(data.keys())}")
            
            if 'data' in data:
                print(f"   Количество записей в 'data': {len(data['data'])}")
                if data['data']:
                    print(f"   Первый rank: {data['data'][0].get('rank', 'N/A')}")
                    print(f"   Последний rank: {data['data'][-1].get('rank', 'N/A')}")
                    print(f"   Пример записи: {json.dumps(data['data'][0], indent=2)}")
            
            if 'meta' in data:
                print(f"\n🔍 Метаданные пагинации:")
                print(f"   {json.dumps(data['meta'], indent=2)}")
            
            if 'leaderboard' in data:
                print(f"   Количество записей в 'leaderboard': {len(data['leaderboard'])}")
            
            return data
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"   Ответ: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return None


def test_pagination():
    """Тест 2: Проверка работы пагинации"""
    print("\n" + "=" * 60)
    print("ТЕСТ 2: Пагинация API")
    print("=" * 60)
    
    url = "https://api.reya.xyz/api/incentives/leaderBoard/total"
    
    # Тест с параметром after
    test_params = [
        {},
        {'after': 100},
        {'after': 1000},
        {'after': 5000},
        {'limit': 100},
        {'limit': 1000},
    ]
    
    for params in test_params:
        try:
            print(f"\n📡 Запрос с параметрами: {params}")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data:
                    count = len(data['data'])
                    first_rank = data['data'][0].get('rank', 'N/A') if data['data'] else 'N/A'
                    last_rank = data['data'][-1].get('rank', 'N/A') if data['data'] else 'N/A'
                    print(f"   ✅ Получено записей: {count}")
                    print(f"   📊 Диапазон ranks: {first_rank} - {last_rank}")
                    
                    if 'meta' in data and 'after' in data['meta']:
                        print(f"   ➡️  Следующий 'after': {data['meta']['after']}")
                elif 'leaderboard' in data:
                    count = len(data['leaderboard'])
                    first_rank = data['leaderboard'][0].get('rank', 'N/A') if data['leaderboard'] else 'N/A'
                    last_rank = data['leaderboard'][-1].get('rank', 'N/A') if data['leaderboard'] else 'N/A'
                    print(f"   ✅ Получено записей: {count}")
                    print(f"   📊 Диапазон ranks: {first_rank} - {last_rank}")
            else:
                print(f"   ❌ Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")


def test_different_endpoints():
    """Тест 3: Проверка альтернативных эндпоинтов"""
    print("\n" + "=" * 60)
    print("ТЕСТ 3: Альтернативные эндпоинты")
    print("=" * 60)
    
    endpoints = [
        "https://api.reya.xyz/api/incentives/leaderBoard/total",
        "https://api.reya.xyz/api/incentives/leaderboard",
        "https://api.reya.xyz/api/incentives/leaderBoard",
        "https://api.reya.xyz/api/leaderboard",
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\n🔗 Тестирование: {endpoint}")
            response = requests.get(endpoint, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                keys = list(data.keys())
                print(f"   ✅ Ключи: {keys}")
                
                # Подсчет записей
                if 'data' in data:
                    print(f"   📊 Записей в 'data': {len(data['data'])}")
                if 'leaderboard' in data:
                    print(f"   📊 Записей в 'leaderboard': {len(data['leaderboard'])}")
                    
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")


def test_query_parameters():
    """Тест 4: Различные query параметры"""
    print("\n" + "=" * 60)
    print("ТЕСТ 4: Query параметры")
    print("=" * 60)
    
    url = "https://api.reya.xyz/api/incentives/leaderBoard/total"
    
    param_combinations = [
        {'page': 1},
        {'page': 2},
        {'offset': 0, 'limit': 100},
        {'offset': 100, 'limit': 100},
        {'skip': 0, 'take': 100},
        {'cursor': 0},
        {'from': 0, 'to': 100},
    ]
    
    for params in param_combinations:
        try:
            print(f"\n📡 Параметры: {params}")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    count = len(data['data'])
                    print(f"   ✅ Записей: {count}")
                elif 'leaderboard' in data:
                    count = len(data['leaderboard'])
                    print(f"   ✅ Записей: {count}")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")


def analyze_current_data():
    """Тест 5: Анализ текущего файла данных"""
    print("\n" + "=" * 60)
    print("ТЕСТ 5: Анализ текущего JSON файла")
    print("=" * 60)
    
    try:
        with open('reya_complete_leaderboard.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Файл загружен успешно")
        print(f"\n📊 Статистика файла:")
        print(f"   Timestamp: {data.get('timestamp', 'N/A')}")
        print(f"   Total Entries: {data.get('totalEntries', 'N/A')}")
        print(f"   Фактическое количество записей: {len(data.get('leaderboard', []))}")
        
        if 'leaderboard' in data and data['leaderboard']:
            leaderboard = data['leaderboard']
            
            # Анализ ranks
            ranks = [entry.get('rank', 0) for entry in leaderboard]
            print(f"\n🔢 Анализ ranks:")
            print(f"   Минимальный rank: {min(ranks)}")
            print(f"   Максимальный rank: {max(ranks)}")
            print(f"   Пропуски в ranks: {max(ranks) - min(ranks) + 1 - len(ranks)}")
            
            # Анализ points
            points = [entry.get('totalPoints', 0) for entry in leaderboard]
            print(f"\n💰 Анализ points:")
            print(f"   Максимум: {max(points):.2f}")
            print(f"   Минимум: {min(points):.2f}")
            print(f"   Средний: {sum(points)/len(points):.2f}")
            
            # Распределение по диапазонам
            ranges = {
                '0-1': 0, '1-5': 0, '5-10': 0, '10-20': 0, '20-50': 0,
                '50-100': 0, '100-200': 0, '200-500': 0, '500-1000': 0,
                '1000-2000': 0, '2000-5000': 0, '5000+': 0
            }
            
            for p in points:
                if p < 1: ranges['0-1'] += 1
                elif p < 5: ranges['1-5'] += 1
                elif p < 10: ranges['5-10'] += 1
                elif p < 20: ranges['10-20'] += 1
                elif p < 50: ranges['20-50'] += 1
                elif p < 100: ranges['50-100'] += 1
                elif p < 200: ranges['100-200'] += 1
                elif p < 500: ranges['200-500'] += 1
                elif p < 1000: ranges['500-1000'] += 1
                elif p < 2000: ranges['1000-2000'] += 1
                elif p < 5000: ranges['2000-5000'] += 1
                else: ranges['5000+'] += 1
            
            print(f"\n📈 Распределение по диапазонам:")
            for range_name, count in ranges.items():
                if count > 0:
                    print(f"   {range_name:12} : {count:5} пользователей")
            
    except FileNotFoundError:
        print("❌ Файл reya_complete_leaderboard.json не найден")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    print("\n🔬 КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ API REYA\n")
    
    # Запуск всех тестов
    api_data = test_api_structure()
    test_pagination()
    test_different_endpoints()
    test_query_parameters()
    analyze_current_data()
    
    print("\n" + "=" * 60)
    print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 60)
