from datetime import datetime, date

br = input("дата рождения : ")

bir = datetime.strptime(br, "%d.%m.%Y").date()

nedel = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
day = nedel[bir.weekday()]

print(f"Вы родились в {day}")


year = bir.year
vis = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
if vis:
    print(f"{year} год был високосным")
else:
    print(f"{year} год не был високосным")

let = date.today()

age = let.year - bir.year


if (let.month, let.day) < (bir.month, bir.day):
    age -= 1

print(f"Сейчас вам {age} лет")