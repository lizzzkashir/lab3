import json
from collections import defaultdict
# часть 1

with open('library.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# словари для быстрого поиска
bo = {book['id']: book for book in data['books']}
rea = {reader['id']: reader for reader in data['readers']}

print(f"Всего книг: {len(data['books'])}")
print(f"Всего читателей: {len(data['readers'])}")
print(f"Всего выдач: {len(data['loans'])}\n")

# часть 2
# для статистики по читателям
statict = defaultdict(lambda: { "total": 0, "returned": 0, "active": 0, "active_cost": 0, "max_book_price": 0})

for loan in data['loans']:
    r_id = loan['reader_id']
    b_id = loan['book_id']

    if r_id in rea and b_id in bo:   # сущ читатель и книга
        statict[r_id]["total"] += 1  #  брал

        if loan['status'] == 'returned':
            statict[r_id]["returned"] += 1
        elif loan['status'] == 'active':
            statict[r_id]["active"] += 1

            # стоимость
            cena = bo[b_id]['price']
            statict[r_id]["active_cost"] += cena

            if cena > statict[r_id]["max_book_price"]:
                statict[r_id]["max_book_price"] = cena

# список для вывода топа и сортировки
tyty = []
de = []

for r_id, stats in statict.items():
    name = rea[r_id]['name']

    if stats["active"] > 0:
        tyty.append({
            "name": name, "active": stats["active"],
            "cost": stats["active_cost"], "max_price": stats["max_book_price"]
        })

    if stats["active"] == 0:
        de.append({
            "name": name, "total": stats["total"], "active": stats["active"], "cost": stats["active_cost"]
        })


tyty.sort(key=lambda x: x['active'], reverse=True)

print("Топ-5 самых активных читателей (по количеству активных книг):")
for i, r in enumerate(tyty[:5], 1):
    print(f"{i}. {r['name']}: {r['active']} книги (стоимостью {r['cost']} руб, самая дорогая: {r['max_price']} руб)")

print("\nДолжники:")
if not de:
    print(" Нет должников")
for d in de:
    print(f"- {d['name']} (взял {d['total']} книги, не вернул {d['active']}, долг: {d['cost']} руб.)")
print()

# часть 3

#  жанры множества
roman = {book['genre'] for book in data['books']}

# 2 авторы  > 3 книг
autcout = defaultdict(int) # число книг у автора
for book in data['books']:
    autcout[book['author']] += 1
populur = {author for author, count in autcout.items() if count > 3}

# 3 статистика
static = defaultdict(lambda: {"books_count": 0, "total_price": 0, "popularity": 0})
bpop = defaultdict(int)  # Сколько раз брали конкретную книгу

for book in data['books']:
    g = book['genre']
    static[g]["books_count"] += 1
    static[g]["total_price"] += book['price']

for loan in data['loans']: # выдача
    b_id = loan['book_id']
    if b_id in bo:
        g = bo[b_id]['genre']
        static[g]["popularity"] += 1 #увеличиваем популярность жанра
        bpop[b_id] += 1

# Самая популярная книга
populboorss = max(bpop, key=bpop.get) if bpop else None
mo = bo[populboorss]['title'] if populboorss else "Нет"
maxxximca = bpop[populboorss] if populboorss else 0 # сколько раз взяли

# кто брал каждый жанр
readall = set(rea.keys())
for r_id in rea.keys():
    # жанры которые брал конкретный читатель
    reagen = set()
    for loan in data['loans']:
        if loan['reader_id'] == r_id and loan['book_id'] in bo:
            reagen.add(bo[loan['book_id']]['genre'])
    # если хоть чтото не взял то удаляем
    if not roman.issubset(reagen):
        readall.discard(r_id)

# переводим в имена
namesss = {rea[r_id]['name'] for r_id in readall}

print("Статистика по жанрам:")
sorted_genres = sorted(static.items(), key=lambda x: x[1]['popularity'], reverse=True)
for i, (genre, stats) in enumerate(sorted_genres, 1):
    print(f"{i}. {genre}: {stats['books_count']} книг, {stats['total_price']} руб., взяли {stats['popularity']} раз")

print(f'\nСамая популярная книга: "{mo}" (взята {maxxximca} раз)')
print(f"Жанры, которые брали все читатели: {namesss if namesss else 'Нет таких'}")
print(f"Авторы с более чем 3 книгами: {populur if populur else 'Нет таких'}\n")

# часть 4

# сумма долга
deb = sum(stats["active_cost"] for stats in statict.values())
lcount = sum(1 for loan in data['loans'] if loan['status'] == 'active') #кол книг

report = {
    "summary": {
        "total_books": len(data['books']),
        "total_readers": len(data['readers']),
        "total_loans": len(data['loans']),
        "active_loans": lcount,
        "total_debt": deb
    },
    "top_readers": [],
    "genre_statistics": {},
    "debtors": []
}

# top_readers
for r in tyty[:5]:
    macena = r['max_price']
    noname = "Неизвестно"
    for b_id, b_info in bo.items():
        if b_info['price'] == macena:
            noname = b_info['title']
            break

    report["top_readers"].append({
        "name": r['name'],
        "active_books": r['active'],
        "total_cost": r['cost'],
        "most_expensive_book": noname
    })

# genre_statistics
for genre, stats in static.items():
    report["genre_statistics"][genre] = {
        "book_count": stats['books_count'],
        "total_value": stats['total_price'],
        "popularity": stats['popularity']
    }

# debtors
for d in de:
    report["debtors"].append({
        "name": d['name'],
        "books_taken": d['total'],
        "books_not_returned": d['active'],
        "debt_amount": d['cost']
    })

with open('report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=4, ensure_ascii=False)

print("все")