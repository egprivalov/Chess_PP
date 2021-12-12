import logging

def xycheck(x,y): #Функция ввода координат с проверкой
    check = False
    while not check:
        try:
            x, y = map(int, input("Введите координаты фигуры: ").split())
            if x <= 8 and x >= 1 and y <= 8 and y >= 1:
                check = True
                logging.info(f"Good input: {x, y}")
            else:
                print("Число должно находится в промежутке от 1 до 8")
                logging.exception(f"Число выпадает из промежутка 1-8! Input: {x,y}")
        except ValueError:
            print("Некорректно введенный данные. Попробуйте цифры.")
            logging.exception(f"Некорректный ввод! Input: {x, y}")
            check = False
    return (x,y)

def is_same_color(x1,y1,x2,y2):  #Проверка совпадения цветов
    if (x1+x2+y1+y2) % 2 == 0:
        return True
    else:
        return False

def blank_field_create():  # Создание шахматного поля
    for i in range(8):
        for j in range(8):
            Field[i].append(cells[(i + j) % 2])

def field_out():  #Функция вывода поля
    for i in range(8):
        print(*Field[i])

#Проверки для фигур

#Проверка башни
def tower_can_eat(x1,y1,x2,y2):
    if x1==x2 or y1 == y2:
        return True
    else:
        return False

#Проверка слона
def oficer_can_eat(x1,y1,x2,y2):
    if abs(x2-x1) == abs(y2-y1):
        return True
    else:
        return False

def oficer_find_way(x1, y1, x2, y2):
    diag = [abs(x2-x1), abs(y2-y1)]
    center = []
    if x1>x2:
        center.append(x1-diag[0]/2)
    else:
        center.append(x1 + diag[0] / 2)
    if y1 > y2:
        center.append(y1 - diag[1] / 2)
    else:
        center.append(y1 + diag[1] / 2)

    possib = [[center[0]+diag[1]/2, center[1]+diag[0]/2],
              [center[0]+diag[1]/2, center[1]-diag[0]/2],
              [center[0]-diag[1]/2, center[1]+diag[0]/2],
              [center[0]-diag[1]/2, center[1]-diag[0]/2]]
    for i in possib:
        check = True
        for j in i:
            if j>8 or j<0:
                check = False
        if check and oficer_can_eat(i[0], i[1], x2, y2):
            return list(map(int, i))

#Проверка коника
def horse_can_eat(x1,y1,x2,y2):
    if abs(x2-x1) + abs(y1-y2) == 3 and abs(x1 - x2) and abs(y1 - y2):
        return True
    else:
        return False

#Проверка коника на два хода
def horse2_can_eat(x1, y1, x2, y2):
    moves = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]
    for i in moves:
        if horse_can_eat(x1 + i[0], y1 + i[1], x2, y2):
            return (x1 + i[0], y1 + i[1])
    return False

def main():
    global Field, cells

    cells = ["■", "□"] #Клетки поля
    Field = [[] for _ in range(8)] #Массив поля

    #Инициализируем файл для логирования
    logging.basicConfig(filename="LogFile1.log", level=logging.INFO)
    

    #Создадим пустое поле
    blank_field_create()

    #Ввод координат двух фигур
    x1=0
    x2=0
    y1=0
    y2=0

    while x1==x2 and y1==y2:
        x1,y1=xycheck(x1,y1)
        x2,y2=xycheck(x2,y2)
        if (x1==x2 and y1==y2):
            print("Координаты фигур должны отличаться")
            logging.exception(f"Координаты фигур совпадают! Input: First figure{x1, y1}, First figure{x2, y2}")

    #Отметка фигур на поле
    Field[8-y1][x1-1] = "◐"
    Field[8-y2][x2-1] = "◑"

    if is_same_color(x1,y1,x2,y2):
        print("Фигуры стоят на клетках одного цвета")
    else:
        print("Фигуры стоят на клетках разных цветов")

    #Выбор фигуры
    print("Выберите фигуру №1. Для выбора:\nФерзя-введите 1\nЛадьи-введите 2\nСлона-введите 3\nКоня-введите 4")
    while True:
        n=input()
        try:
            n=int(n)
            if n > 4 or n < 1:
                print("Необходимо число от 1 до 4. Попробуйте снова")
                logging.exception(f"Число выпадает из промежутка 1-4! Input: {n}")
            else:
                break
        except ValueError:
            print("Некорректный ввод")
            logging.exception(f"Некорректный ввод! Input: {n}")

    if n == 1:  #Ферзь
        if tower_can_eat(x1, y1, x2, y2) or oficer_can_eat(x1,y1,x2,y2):
            print("Ферзь может добраться до второй фигуры за один ход")
        else:
            Field[8-y2][x1-1] = "◎"
            print("Ферзь может добраться до второй фигуры за два хода")

    elif n == 2:  #Ладья
        if tower_can_eat(x1,y1,x2,y2):
            print("Ладья может добраться до второй фигуры за один ход")
        else:
            Field[8-y2][x1-1] = "◎"
            print("Ладья может добраться до второй фигуры за два хода")

    elif n == 3:  #Слон
        if oficer_can_eat(x1, y1, x2, y2):
            print("Слон может добраться до второй фигуры за один ход")
        elif is_same_color(x1, y1, x2, y2):
            first_move = oficer_find_way(x1, y1, x2, y2)
            Field[8-first_move[1]][first_move[0]-1] = "◎"
            print("Слон может добраться до второй фигуры за два хода")
        else:
            print("Слон не может добраться до второй фигуры. Они на разных цветах")

    elif n == 4:  #Конь
        if horse_can_eat(x1, y1, x2, y2):
            print("Конь может добраться до второй фигуры за один ход")
        else:
            second_move = horse2_can_eat(x1, y1, x2, y2)
            if second_move:
                Field[8-second_move[1]][second_move[0]-1] = "◎"
                print("Конь может добраться до второй фигуры за два хода")
            else:
                print("Конь не может добраться до второй фигуры за два хода")

    #Вывод итогового поля
    field_out()

    print("■-черная клетка\n"
          "□-белая клетка\n"
          "◐-первая фигура\n"
          "◑-вторая фигура\n"
          "◎-Промежуточный ход, если до цели можно добраться лишь за два хода")

main()