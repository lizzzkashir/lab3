import numpy as np

arr = np.random.randint(-100, 101, size=20)
print(f"Исходный массив:\n{arr}\n")


mi = np.min(arr)
ma = np.max(arr)
cr = np.mean(arr)
print(f"Минимальное значение: {mi}")
print(f"Максимальное значение: {ma}")
print(f"Среднее значение: {cr:.2f}\n")


otr = arr[arr < 0]
print(f"Отрицательные элементы: {otr}\n")

arrcop = arr.copy()
arrcop[arrcop > 10] = 0
print(f"Массив после замены:\n{arrcop}\n")

crarif = np.mean(arr[1::2])

print(f"Среднее арифметическое элементов на нечётных позициях: {crarif:.2f}")