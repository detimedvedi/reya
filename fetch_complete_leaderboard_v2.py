"""
Улучшенный парсер полного лидерборда Reya с детальным логированием
"""
import requests
import json
import time
from datetime import datetime

def fetch_complete_leaderboard_v2():
    """
    Fetch complete Reya leaderboard with improved pagination handling
    """
    
    base_url = "https://api.reya.xyz/api/incentives/leaderBoard/total"
    all_data = []
    page = 1
    max_pages = 10000  # Увеличено для получения всех 80,000+ записей (4000+ страниц)
    
    print("=" * 70)
    print("🚀 НАЧАЛО ПАРСИНГА ПОЛНОГО ЛИДЕРБОРДА REYA")
    print("=" * 70)
    print(f"⏰ Время старта: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 URL: {base_url}\n")
    
    # Первый запрос без параметров
    print(f"📡 Страница {page}: Запрос начальных данных...")
    
    try:
        response = requests.get(base_url, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Ошибка HTTP {response.status_code}")
            print(f"   Ответ: {response.text[:500]}")
            return None
        
        data = response.json()
        print(f"✅ Успешный ответ")
        print(f"   Структура ответа: {list(data.keys())}")
        
        # Определяем структуру данных
        if 'data' in data:
            records = data['data']
            data_key = 'data'
        elif 'leaderboard' in data:
            records = data['leaderboard']
            data_key = 'leaderboard'
        else:
            print(f"❌ Неизвестная структура данных: {list(data.keys())}")
            return None
        
        all_data.extend(records)
        
        if records:
            first_rank = records[0].get('rank', 'N/A')
            last_rank = records[-1].get('rank', 'N/A')
            first_points = records[0].get('totalPoints', 0)
            last_points = records[-1].get('totalPoints', 0)
            
            print(f"   📊 Получено записей: {len(records)}")
            print(f"   🔢 Диапазон ranks: {first_rank} → {last_rank}")
            print(f"   💰 Диапазон points: {first_points:.2f} → {last_points:.2f}")
        
        # Проверяем метаданные пагинации
        meta = data.get('meta', {})
        print(f"   🔍 Метаданные: {meta}")
        
        after = meta.get('after')
        has_more = meta.get('hasMore', False)
        
        # Если есть пагинация, продолжаем
        while (after or has_more) and page < max_pages:
            page += 1
            print(f"\n📡 Страница {page}: Запрос следующей порции (after={after})...")
            
            # Пробуем разные варианты параметров
            params_variants = [
                {'after': after},
                {'cursor': after},
                {'offset': len(all_data)},
                {'page': page},
            ]
            
            success = False
            
            for params in params_variants:
                if not params.get('after') and not params.get('cursor'):
                    # Пропускаем варианты без after/cursor если они есть
                    if after:
                        continue
                
                try:
                    response = requests.get(base_url, params=params, timeout=30)
                    
                    if response.status_code != 200:
                        continue
                    
                    data = response.json()
                    records = data.get(data_key, [])
                    
                    if not records:
                        print(f"   ⚠️  Пустой ответ с параметрами {params}")
                        print(f"   ✅ Достигнут конец данных - всего получено {len(all_data)} записей")
                        success = False
                        break
                    
                    # Проверяем, не дубликаты ли это
                    first_new_rank = records[0].get('rank', 0)
                    last_existing_rank = all_data[-1].get('rank', 0) if all_data else 0
                    
                    if first_new_rank <= last_existing_rank:
                        print(f"   ⚠️  Дубликаты данных (rank {first_new_rank} <= {last_existing_rank})")
                        continue
                    
                    # Успешно получили новые данные
                    all_data.extend(records)
                    success = True
                    
                    first_rank = records[0].get('rank', 'N/A')
                    last_rank = records[-1].get('rank', 'N/A')
                    first_points = records[0].get('totalPoints', 0)
                    last_points = records[-1].get('totalPoints', 0)
                    
                    print(f"   ✅ Получено записей: {len(records)} (параметры: {params})")
                    print(f"   🔢 Диапазон ranks: {first_rank} → {last_rank}")
                    print(f"   💰 Диапазон points: {first_points:.2f} → {last_points:.2f}")
                    print(f"   📈 Всего накоплено: {len(all_data)} записей")
                    
                    # Обновляем метаданные
                    meta = data.get('meta', {})
                    after = meta.get('after')
                    has_more = meta.get('hasMore', False)
                    
                    if meta:
                        print(f"   🔍 Новые метаданные: {meta}")
                    
                    break
                    
                except Exception as e:
                    print(f"   ⚠️  Ошибка с параметрами {params}: {e}")
                    continue
            
            if not success:
                print(f"   ✅ Парсинг завершен - получены все доступные данные")
                break
            
            # Пауза между запросами (уменьшена для ускорения)
            time.sleep(0.3)
            
            # Прогресс каждые 100 страниц
            if page % 100 == 0:
                print(f"\n📊 Прогресс: {page} страниц, {len(all_data):,} записей")
        
        if page >= max_pages:
            print(f"\n⚠️  Достигнут лимит страниц ({max_pages}) - возможно есть еще данные")
        
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    # Финальная обработка
    print("\n" + "=" * 70)
    print("📊 ФИНАЛЬНАЯ ОБРАБОТКА ДАННЫХ")
    print("=" * 70)
    
    print(f"✅ Всего получено записей: {len(all_data)}")
    
    if not all_data:
        print("❌ Нет данных для сохранения")
        return None
    
    # Сортировка по rank
    print("🔄 Сортировка по rank...")
    all_data.sort(key=lambda x: x.get('rank', 0))
    
    # Проверка на дубликаты
    ranks = [entry.get('rank') for entry in all_data]
    unique_ranks = len(set(ranks))
    
    if unique_ranks < len(ranks):
        print(f"⚠️  Обнаружены дубликаты ranks: {len(ranks)} записей, {unique_ranks} уникальных")
        # Удаляем дубликаты, оставляя первое вхождение
        seen_ranks = set()
        unique_data = []
        for entry in all_data:
            rank = entry.get('rank')
            if rank not in seen_ranks:
                seen_ranks.add(rank)
                unique_data.append(entry)
        all_data = unique_data
        print(f"   ✅ После удаления дубликатов: {len(all_data)} записей")
    
    # Статистика
    ranks = [entry.get('rank', 0) for entry in all_data]
    points = [entry.get('totalPoints', 0) for entry in all_data]
    
    print(f"\n📈 СТАТИСТИКА:")
    print(f"   🔢 Ranks: {min(ranks)} → {max(ranks)}")
    print(f"   💰 Points: {min(points):.2f} → {max(points):.2f}")
    print(f"   📊 Средние points: {sum(points)/len(points):.2f}")
    
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
    
    print(f"\n📊 РАСПРЕДЕЛЕНИЕ ПО ДИАПАЗОНАМ:")
    for range_name, count in ranges.items():
        if count > 0:
            pct = (count / len(all_data)) * 100
            print(f"   {range_name:12} : {count:5} ({pct:5.1f}%)")
    
    # Создание финального датасета
    final_data = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": base_url,
        "totalEntries": len(all_data),
        "minPoints": min(points),
        "maxPoints": max(points),
        "avgPoints": sum(points) / len(points),
        "leaderboard": all_data
    }
    
    return final_data


if __name__ == "__main__":
    leaderboard_data = fetch_complete_leaderboard_v2()
    
    if leaderboard_data:
        # Сохранение в JSON
        filename = "reya_complete_leaderboard.json"
        
        print(f"\n💾 Сохранение в {filename}...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(leaderboard_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Данные успешно сохранены!")
        print(f"\n📄 Файл: {filename}")
        print(f"📊 Всего пользователей: {leaderboard_data['totalEntries']:,}")
        print(f"💰 Диапазон points: {leaderboard_data['minPoints']:.2f} - {leaderboard_data['maxPoints']:.2f}")
        print(f"📈 Средние points: {leaderboard_data['avgPoints']:.2f}")
        
        # Топ-3 и последние 3
        print(f"\n🏆 ТОП-3:")
        for i in range(min(3, len(leaderboard_data['leaderboard']))):
            user = leaderboard_data['leaderboard'][i]
            print(f"   {i+1}. {user['walletAddress'][:10]}... - {user['totalPoints']:.2f} points")
        
        print(f"\n📉 ПОСЛЕДНИЕ 3:")
        for i in range(max(0, len(leaderboard_data['leaderboard']) - 3), len(leaderboard_data['leaderboard'])):
            user = leaderboard_data['leaderboard'][i]
            print(f"   {user['rank']}. {user['walletAddress'][:10]}... - {user['totalPoints']:.2f} points")
        
        print("\n" + "=" * 70)
        print("✅ ПАРСИНГ ЗАВЕРШЕН УСПЕШНО")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("❌ ПАРСИНГ ЗАВЕРШЕН С ОШИБКОЙ")
        print("=" * 70)
