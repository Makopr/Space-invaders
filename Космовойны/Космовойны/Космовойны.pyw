import config

import pygame

import random

import os

import time

# Возвращает True, если нажат ESC, пробел или правая кнопка мыши
def getPressedESC():
    ret = False

    for event in eventPygame:
        # Если нажата клавиша
        if (event.type == pygame.KEYDOWN):
            # ... если это пробел
            if (event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE):
                ret = True
        # Если нажата кнопка мыши
        if (event.type == pygame.MOUSEBUTTONDOWN):
            # ... если это правая кнопка
            if (event.button == 3):
                ret = True

    return ret

# Ждём правой кнопки или пробела и переключаемся на меню
def waitPressRMB():
    # Проверяем события
    if (getPressedESC()):
        config.playSound("EXPLOSION_ALIEN")
        fullReset(0, 0, True)

    # Фон
    screen.blit(config.backGround, (0, 0))

    # Выводим надпись "с тенью", сместив нижнюю чуть вниз и вправо
    render = config.text80.render("НАШИ ГЕРОИ:", 1, (150, 150, 150))
    screen.blit(render, (103, 43))
    # "Верхний" текст
    render = config.text80.render("НАШИ ГЕРОИ:", 1, (200, 50, 80))
    screen.blit(render, (100, 40))

    # Выводим таблицу рекордов
    drawRecords(230, 145, 22, (255, 255, 0), (210, 0, 230), config.newRecord, config.text16)

    # Отрисовываем бегущую строку
    drawFloatText()
    # Обрабатываем список с информацией о баннерах
    drawBanner()

# Рисуем рекламный баннер
# Баннер: [Изображение, Прошло кадров, Альфа-канал, Пауза (кадров), Позиция Y]
def drawBanner():
    # Список для удаления неактивных
    deleteBanner = []

    # Обрабатываем каждый по индексу
    for i in range(len(config.advertising)):

        # Получаю ссылку в более короткую переменную
        obj = config.advertising[i]

        # Устанавливаем прозрачность (0-255)
        obj[0].set_alpha(obj[2])

        # Расчёт проявления и выцветания
        if (obj[1] > obj[3]):
            obj[2] -= 10
            if (obj[2] < 0):
                deleteBanner.append([i])
        else:
            if (obj[2] < 255):
                obj[2] += 5

        # Увеличиваем кадр
        obj[1] += 1

        # Выводим баннер на экран
        screen.blit(obj[0], (0, obj[4]))

    # Удаляем неактивные
    for i in range(len(deleteBanner)):
        del config.advertising[i]

# Вводим ник пользователя
def inputPlayerName():
    # Подсвечиваем место ввода ника
    pygame.draw.rect(screen, (100, 200, 0), (200, 175 + config.newRecord * 22, 400, 25))
    
    # Мерцание курсора
    if (config.blink[0] > 0):
        config.blink[0] -= 1
        pygame.draw.rect(screen, (0, 0, 0), (280 + config.text16.size(config.playerName)[0], 178 + config.newRecord * 22, 2, 19))
        if (config.blink[0] == 0):
            config.blink[1] = 30

    if (config.blink[1] > 0):
        config.blink[1] -= 1
        if (config.blink[1] == 0):
            config.blink[0] = 30

    # Записываем либо "Введите ник", если ник пустой, либо
    # выводим введённые символы
    if (config.playerName == ""):
        render = config.text16.render("Введите ник", 1, (37, 37, 37))
        screen.blit(render, (280, 178 + config.newRecord * 22))
    else:
        render = config.text16.render(config.playerName, 1, (37, 37, 37))
        screen.blit(render, (280, 178 + config.newRecord * 22))

    # Проверка нажатых кнопок
    for event in eventPygame:
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_BACKSPACE):
                # Удаляем последний символ
                if (len(config.playerName) > 0):
                    config.playerName = config.playerName[0:len(config.playerName) - 1]
                    config.playSound("PRESSKEY")
            else:
                # Получаем кнопку по коду
                ch = event.key
                # Нажата клавиша (левый или правый) SHIFT?
                if ((pygame.key.get_mods() == 1
                    or pygame.key.get_mods() == 2)
                    and (ch != 13)):

                    # Обрабатываем символы ! и _
                    if (chr(ch) == "1"):
                        ch = ord("!")
                    elif (chr(ch) == "-"):
                        ch = ord("_")
                    else:
                        ch -= 32
                # Код клавиши Enter - 13
                if (ch == 13):
                    # Если пустой ник, то устанавливаем ник по умолчанию
                    if (config.playerName == ""):
                        config.playerName = config.defaultName
                    # Устанавливаем имя
                    config.records[config.newRecord][0] = config.playerName
                    # Сбрасываем позицию "нового рекорда", чтобы программа понимала,
                    # что рекорд записан и теперь игрок в обычных условиях
                    config.newRecord = 10
                    # Сохраняем рекорды
                    if (not config.cheat):
                        config.saveRecords(config.records)
                    # Восстанавливаем параметры мерцания курсора
                    config.blink = [30, 0]
                    # Ждём нажатие пробела или правой кнопки для начала новой игры
                    appentTextToUpLine("Нажмите ПРОБЕЛ, ESC или ПКМ для выхода в меню", "START", (255, 255, 255), 3, 1)
                    config.gameState = config.WAITPRESSRMB
                else:
                    # Получаем символ по коду
                    ch = chr(ch)
                    # Проверяем символ в допустимом наборе
                    if (ch in config.characterSet):
                        # Проверяем длину имени
                        if (len(config.playerName) < 20 ):
                            # Добавляем символ
                            config.playerName += ch
                            config.playSound("PRESSKEY")

# Рисуем таблицу рекордов в финале
def drawFinalRecord():
    # Фон
    screen.blit(config.backGround, (0, 0))

    # Если человек попал в таблицу рекордов
    # (его место не равно десятому, последнему)
    if (config.newRecord != 10):
        # Организуем ввод имени пользователя
        inputPlayerName()

    # Выводим надпись "с тенью"
    render = config.text80.render("НАШИ ГЕРОИ:", 1, (150, 150, 150))
    screen.blit(render, (103, 43))

    render = config.text80.render("НАШИ ГЕРОИ:", 1, (200, 50, 80))
    screen.blit(render, (100, 40))

    # Выводим таблицу очков
    drawRecords(230, 145, 22, (255, 255, 0), (210, 0, 230), config.newRecord, config.text16)

    # Отрисовываем бегущую строку
    drawFloatText()
    # Обрабатываем список с информацией о баннерах
    drawBanner()

# Возвращаем номер позиции в таблице рекордов
def getNumberRecordPosition():
    # Добавляем к рекордам последнюю строку, чтобы определить место пользователя (см. учебник)
    config.records.append(["", config.level, config.score])
    ret = 10

    # Обычное перемещение по списку! Не сработает, если исходный список не отсортирован!
    for i in range(9, -1, -1):
        if (config.records[ret][2] > config.records[i][2]):
            config.records[ret], config.records[i] = config.records[i], config.records[ret]
            ret = i

    # Удаляем последнюю запись, т.к. она уже не нужна
    del config.records[10]

    # Возвращаем номер занятого места (или 10, если человек не попал в таблицу рекордов)
    return ret

# Очки в финале игры
def checkScore():
    # Удаляем объекты - бегущие строки (если они есть)
    del config.textFloatOnScreen[:]

    # Получаем место пользователя в таблице рекордов
    config.newRecord = getNumberRecordPosition()

    # Если игрок занял место, то поздравляем его
    if (config.newRecord != 10):
        # Баннер: [Изображение, Прошло кадров, Альфа-канал, Пауза (кадров), Позиция Y]
        config.advertising.append([config.bannerName[random.randint(0, len(config.bannerName) - 1)],
                                   0, 0, 255, config.HEIGHT - 95])

        config.playSound("TABLERECORD")
        appentTextToUpLine(f"ПОЗДРАВЛЯЕМ! Вы заняли в таблице очков {config.newRecord + 1} место!", "START", (155, 200, 200), 3, 1)

        # Меняем состояние игры для прорисовки таблицы очков и ввода имени
        config.gameState = config.CHECKSCORE
    # Иначе начинаем игру заново с открытым меню
    else:
        fullReset(0, 0, True)

# Сцена окончания игры
def drawEndGame():
    # Фон финала
    screen.blit(config.backendgame, (0, 0))

    # Координаты, относительно которых выводится таблица бонусов
    x = 300
    y = 120

    # Рисуем базовые элементы бонусной таблицы
    renderBase(x, y)

    # Каждые восемь кадров
    if (countFPS % 8 == 0):
        # Считаем добавленные очки
        calcAddingScore(config.endGameScoreCalc,
                        config.greenScore // 2,
                        config.yellowScore // 2,
                        config.redScore // 2,
                        config.rocketScore // 100,
                        config.blueScore // 2)

    # Рисуем анимацию "увеличение бонусов"
    calcScoreNextLevel(x, y, config.endGameScoreCalc)

    # Обязательно с помощью and проверяем, чтобы на экране не было других бегущих строк
    if (config.endGameScoreCalc[13] and len(config.textFloatOnScreen) == 0):
        appentTextToUpLine("Нажмите ПРОБЕЛ, ESC или ПКМ для продолжения!", "START", (255, 255, 255), 2, 1)

    # Включаем обработку нажатия клавиш и дальнейшие действия
    if (config.endGameScoreCalc[13]):
        drawBonus(x, y, config.endGameScoreCalc)
        if (getPressedESC()):
            config.playSound("EXPLOSION_ALIEN")
            checkScore()

    drawInfoLine()
    drawFloatText()

# Определяем конец игры
def goEndGame():
    config.playSound("NONE")
    config.playSound("BACKGROUND_MUSIC_PAUSE")
    config.playSound("THEEND")

    del config.textFloatOnScreen[:]

    # Чтобы не отображались очки до того, как они начнут считаться
    config.screenScore = 0

    # Добавляем бегущую строку
    appentTextToUpLine("Вы не сдержали инопланетян, вас захватили. Готовьтесь, завтра на работу!", "START", (255, 50, 50), 3, 1)

    # Устанавливаем в информационную строку значение ракет
    config.maxPlayerRocket = config.endGameScoreCalc[9]

    # Используем тот же список для контроля счёта
    config.counterScoreUnit = [0, 0, 0, 0, 0]

    # Устанавливаем состояние "Конец игры", обрабатываемое в главном цикле
    config.gameState = config.ENDGAME

# Отрисовка бонусной строки
def drawBonus(x, y, dataBonus):
    render = config.text20.render("БОНУС:", 1, (255, 255, 255))
    screen.blit(render, (x, y + 215))

    summ = dataBonus[1] + dataBonus[4] + dataBonus[7] + dataBonus[10] + dataBonus[15]
    render = config.text20.render("= " + str(summ), 1, (100, 155, 255))
    screen.blit(render, (x + 130, y + 215))

# Отрисовка очков на экране переключения уровня
def calcScoreNextLevel(x, y, object):
    if (config.screenScore > 0):
        render = config.text20.render("= " + str(object[1]), 1, (100, 255, 100))
        screen.blit(render, (x + 130, y + 5))
    if (config.screenScore > 1):
        render = config.text20.render("= " + str(object[4]), 1, (255, 255, 100))
        screen.blit(render, (x + 130, y + 45))
    if (config.screenScore > 2):
        render = config.text20.render("= " + str(object[7]), 1, (255, 50, 50))
        screen.blit(render, (x + 130, y + 85))
    if (config.screenScore > 3):
        render = config.text20.render("= " + str(object[15]), 1, (255, 0, 150))
        screen.blit(render, (x + 130, y + 125))
    if (config.screenScore > 4):
        render = config.text20.render("= " + str(object[10]), 1, (255, 0, 150))
        screen.blit(render, (x + 130, y + 165))

# Отрисовываем основу
def renderBase(x, y):
    screen.blit(config.invadersTexture[0], (x, y))
    screen.blit(config.invadersTexture[2], (x, y + 40))
    screen.blit(config.invadersTexture[4], (x, y + 80))
    screen.blit(config.superInvaderTexture[0], (x, y + 120))
    screen.blit(config.playerRocketTexture[0], (x + 6, y + 160))

    render = config.text20.render("x " + str(config.counterScoreUnit[0]), 1, (255, 255, 255))
    screen.blit(render, (x + 35, y + 5))

    render = config.text20.render("x " + str(config.counterScoreUnit[1]), 1, (255, 255, 255))
    screen.blit(render, (x + 35, y + 45))

    render = config.text20.render("x " + str(config.counterScoreUnit[2]), 1, (255, 255, 255))
    screen.blit(render, (x + 35, y + 85))

    render = config.text20.render("x " + str(config.counterScoreUnit[4]), 1, (255, 255, 255))
    screen.blit(render, (x + 35, y + 125))

    render = config.text20.render("x " + str(config.counterScoreUnit[3]), 1, (255, 255, 255))
    screen.blit(render, (x + 35, y + 165))

    pygame.draw.line(screen, (255, 255, 255), [x - 50, y + 200], [x + 250, y + 200], 2)

# Функция, возвращающая количество для вычитания
def getStep(data1, data2):
    ret = 1
    # Не "круглые" значения - чтобы все цифры менялись в числе
    # Не спрашивайте откуда эти числа - это рандом на клавиатуре по цифрам
    if (data1 - data2 > 50000):
        ret = 41682
    elif (data1 - data2 > 25000):
        ret = 21378
    elif (data1 - data2 > 1000):
        ret = 734
    elif (data1 - data2 > 100):
        ret = 72
    elif (data1 - data2 > 10):
        ret = 7
    return ret

# Анимация очков
def calcAddingScore(dataObject, greenScore, yellowScore, redScore, rocketScore, blueScore):

    if (dataObject[2]):
        if (config.counterScoreUnit[0] < dataObject[0]):
            # Получаем количество для вычитания
            step = getStep(dataObject[0], config.counterScoreUnit[0])
            # Увеличиваем количество "зелёных" пришельцев
            config.counterScoreUnit[0] += step
            # Добавляем награду для отображения на экране
            dataObject[1] += step * greenScore
            # Добавляем награду к очкам
            config.score += step * greenScore
            config.playSound("TICK")
        config.screenScore = 1
        # Здесь нельзя использовать else, иначе возникнет маленькая и неприятная
        # пауза после того, как программа переведёт пришельцев в очки
        if (config.counterScoreUnit[0] == dataObject[0]):
            dataObject[2] = False
            config.playSound("PLUSSCORE")
    elif (dataObject[5]):
        if (config.counterScoreUnit[1] < dataObject[3]):
            step = getStep(dataObject[3], config.counterScoreUnit[1])
            config.counterScoreUnit[1] += step
            dataObject[4] += step * yellowScore
            config.score += step * yellowScore
            config.playSound("TICK")
        config.screenScore = 2
        if (config.counterScoreUnit[1] == dataObject[3]):
            dataObject[5] = False
            config.playSound("PLUSSCORE")
    elif (dataObject[8]):
        if (config.counterScoreUnit[2] < dataObject[6]):
            step = getStep(dataObject[6], config.counterScoreUnit[2])
            config.counterScoreUnit[2] += step
            dataObject[7] += step * redScore
            config.score += step * redScore
            config.playSound("TICK")
        config.screenScore = 3
        if (config.counterScoreUnit[2] == dataObject[6]):
            dataObject[8] = False
            config.playSound("PLUSSCORE")
    elif (dataObject[16]):
        if (config.counterScoreUnit[4] < dataObject[14]):
            step = getStep(dataObject[14], config.counterScoreUnit[4])
            config.counterScoreUnit[4] += step
            config.maxPlayerRocket -= step
            dataObject[15] += step * blueScore
            config.score += step * blueScore
            config.playSound("TICK")
        config.screenScore = 4
        if (config.counterScoreUnit[4] == dataObject[14]):
            dataObject[16] = False
            config.playSound("PLUSSCORE")
    elif (dataObject[11]):
        if (config.counterScoreUnit[3] < dataObject[9]):
            step = getStep(dataObject[9], config.counterScoreUnit[3])
            config.counterScoreUnit[3] += step
            config.maxPlayerRocket -= step
            dataObject[10] += step * rocketScore
            config.score += step * rocketScore
            config.playSound("TICK")
        config.screenScore = 5
        if (config.counterScoreUnit[3] == dataObject[9]):
            dataObject[11] = False
            config.playSound("PLUSSCORE")
            if (config.gameState == config.NEXTLEVEL):
                config.playSound("NEXTLEVEL")
            # Включаем отображение цифр обратного отсчёта
            dataObject[13] = True
            
# Переключение на следующий уровень
def drawNextLevel():
    # Рисуем фоновое изображение космоса
    screen.blit(config.backGround, (0, 0))

    # Относительные координаты
    x = 300
    y = 120

    renderBase(x, y)

    # Воспроизводим анимацию "добавления очков"
    if (countFPS % 7 == 0):
        # Отправляем количество очков для добавления к общему счёту
        # При вызове drawAddingScore() при поражении количество будет другое
        calcAddingScore(config.nextLevelData,
                        config.greenScore,
                        config.yellowScore,
                        config.redScore,
                        config.rocketScore,
                        config.blueScore)

    calcScoreNextLevel(x, y, config.nextLevelData)

    # Контролируем, заработал ли пользователь дополнительную жизнь?
    if (config.score >= config.addingLiveStep):
        addingLive()

    if (config.nextLevelData[13]):
        drawBonus(x, y, config.nextLevelData)
        # Текст для отображения обратного отсчёта до следующего уровня
        txt = f"Старт... {str(int(config.nextLevelData[12]))}"
        # Формируем текст указанным шрифтом (text32)
        render = config.text32.render(txt, 1, (100, 255, 200))
        # Получаем ширину текста в пикселях
        widthText = config.text32.size(txt)[0]
        # Отображаем строку с текстом
        screen.blit(render, (config.WIDTH // 2 - widthText // 2, y + 255))
        # Уменьшаем параметр, чтобы обратный отсчёт "считал". Вычитаем 0.01 В КАДР!
        config.nextLevelData[12] -= .01

        if (getPressedESC()):
            config.nextLevelData[12] = 0

    if (int(config.nextLevelData[12]) <= 0):
        # Сбрасываем значения для списка - хранилища статистики
        config.resetNextLevelData()
        # Останавливаем все звуки
        config.playSound("NONE")
        # Продолжаем дальше
        startNewGame(config.level, config.score, False)

    drawInfoLine()
    drawFloatText()
    drawBanner()


# Добавление дополнительной жизни
def addingLive():
    # Плюс одна жизнь
    config.lives += 1
    # Увеличиваем следующий порог очков для получения жизни
    config.addingLiveStep *= config.addingLiveStepScale
    # Сообщаем в бегущей строке
    appentTextToUpLine("Дополнительная жизнь!", "START", (0, 255, 20), 4, 1)

# Проверка попаданий в кирпичные стены
def checkHitRocketsAndBomb():
    # Вычисляем максимальную точку, после которой можно рассчитывать столкновения
    maxYBrick = config.HEIGHT - config.SQUARE_SIZE * 3

    # Список для удаления ударившихся о кирпичи ракет игрока
    deleteRocket = []

    # Проверяем КАЖДУЮ ракету с КАЖДЫМ кирпичиком стены
    # 10 кирпичей * 5 стен * 10 ракет = 500 итераций * 60 = 30000 итераций в секунду
    # Цикл для ракет
    for i in range(len(config.playerRocketObjects)):
        # Получаю ссылку в короткую переменную
        obj = config.playerRocketObjects[i]
        # Если ракета находится ниже кирпичей
        if (getY(obj) >= maxYBrick):
            j = 0
            # Цикл для проверки столкновения с каждым кирпичиком
            while (j < len(config.brickObject)):
                # Подробно раскладываю параметры "текущей" ракеты
                brick = config.brickObject[j]
                xRocket = getX(obj) + 4
                yRocket = getY(obj)
                xBrick = getX(brick)
                yBrick = getY(brick)
                distX = abs(xRocket - xBrick)
                distY = abs(yRocket - yBrick)
                # Столкнулись (расстояние меньше 8 пикселей)?
                if (distX < 8 and distY < 8):
                    config.explosionObjects.append([getX(obj) - 64, getY(obj) - 64, 0])
                    brick[2] = False
                    deleteRocket.append(i)
                    j = len(config.brickObject)
                j += 1

    # Удаляем те кирпичи, у которых элемент [2] == False, то есть не используется
    for i in range(len(config.brickObject) - 1, -1, -1):
        if (not config.brickObject[i][2]):
            del config.brickObject[i]

    # Удаляем те ракеты, которые взорвали кирпичи
    for i in range(len(deleteRocket) - 1, -1, -1):
        del config.playerRocketObjects[deleteRocket[i]]

    # Новый список для удаления ракет инопланетян
    deleteRocket = []

    # Проверяем КАЖДУЮ бомбу инопланетянина на столкновение с кирпичами
    for i in range(len(config.invadersBombObject)):
        obj = config.invadersBombObject[i]
        if (getY(obj) >= maxYBrick):
            j = 0
            # Цикл для проверки столкновения с каждым кирпичиком
            while (j < len(config.brickObject)):
                distX = abs(getX(obj) + 4 - getX(config.brickObject[j]))
                distY = abs(getY(obj) - getY(config.brickObject[j]))
                # Столкнулись?
                if (distX < 8 and distY < 32):
                    config.explosionObjects.append([getX(obj) - 64, getY(obj) - 64, 0])
                    config.brickObject[j][2] = False
                    deleteRocket.append(i)
                    j = len(config.brickObject)
                j += 1

    # Удаляем те кирпичи, у которых элемент [2] == False, то есть не используется
    for i in range(len(config.brickObject) - 1, -1, -1):
        if (not config.brickObject[i][2]):
            del config.brickObject[i]

    # Удаляем те ракеты, которые взорвали кирпичи
    for i in range(len(deleteRocket) - 1, -1, -1):
        del config.invadersBombObject[deleteRocket[i]]

# Отрисовка кирпичных стен
def drawBrick():
    if (len(config.brickObject) == 0):
        return 0

    for obj in config.brickObject:
        screen.blit(config.brickTexture, (getX(obj), getY(obj)))

# Отображение таблицы рекордов
def drawRecords(x, y, lineHeight, color1, color2, number, font):

    render = font.render("Место                 Ник                    Уровень     Очки:", 1, color2)
    screen.blit(render, (x, y))
    y += int(lineHeight * 1.5)

    # 10 - максимальное количество записей в таблице рекордов
    for i in range(10):
        color = color1
        if (i == number):
            color = color2

        render = font.render(str(i + 1), 1, color)
        screen.blit(render, (x + 17, y))

        render = font.render(config.records[i][0], 1, color)
        screen.blit(render, (x + 50, y))

        render = font.render(str(config.records[i][1]), 1, color)
        screen.blit(render, (x + 240, y))

        render = font.render(str(config.records[i][2]), 1, color)
        screen.blit(render, (x + 310, y))

        y += lineHeight

# Проверка нажатия мыши
def mouseClick():
    global playGame
    thisX, thisY = pygame.mouse.get_pos()
    x = 0
    y = 0
    for event in eventPygame:
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (event.button == 1):
                x, y = event.pos

    if (thisX > 75 and thisY > 125 and thisX < 315 and thisY < 165):
        config.bgColorMenu1 = config.selectBgColor
    else:
        config.bgColorMenu1 = config.defaultBgColor

    if (thisX > 75 and thisY > 170 and thisX < 315 and thisY < 205):
        config.bgColorMenu2 = config.selectBgColor
    else:
        config.bgColorMenu2 = config.defaultBgColor

    if (thisX > 75 and thisY > 215 and thisX < 315 and thisY < 255):
        config.bgColorMenu3 = config.selectBgColor
    else:
        config.bgColorMenu3 = config.defaultBgColor


    if (thisX > 75 and thisY > 260 and thisX < 315 and thisY < 300):
        config.bgColorMenu4 = config.selectBgColor
    else:
        config.bgColorMenu4 = config.defaultBgColor

    if (thisX > 75 and thisY > 305 and thisX < 315 and thisY < 345):
        config.bgColorMenu5 = config.selectBgColor
    else:
        config.bgColorMenu5 = config.defaultBgColor

    if (thisX > 75 and thisY > 350 and thisX < 315 and thisY < 390):
        config.bgColorMenu6 = config.selectBgColor
    else:
        config.bgColorMenu6 = config.defaultBgColor

    # Щелчок по пункту "Начать заново"
    if (x > 75 and y > 125 and x < 315 and y < 165):
        config.gameState = config.GAME
        config.mouseShoot = True
        config.playSound("NONE")
        fullReset(0, 0, False)

    if (not config.blinkMenu):
        # Щелчок по пункту "Продолжить"
        if (x > 75 and y > 175 and x < 315 and y < 205):
            config.gameState = config.GAME
            config.mouseShoot = True

    # Щелчок по пункту "Звук"
    if (x > 75 and y > 215 and x < 315 and y < 255):
        config.soundInGame = not config.soundInGame
        config.saveSetup()

    # Щелчок по пункту "Музыка"
    if (x > 75 and y > 260 and x < 315 and y < 300):
        config.musicInGame = not config.musicInGame
        # config.playSound("BACKGROUND_MUSIC_PLAY")
        config.saveSetup()

    # Щелчок по пункту "Мышь" или "Клавиатура"
    if (x > 75 and y > 305 and x < 315 and y < 345):
        config.mousePlay = not config.mousePlay
        config.saveSetup()

    # Щелчок по пункту "Выход"
    if (x > 75 and y > 350 and x < 315 and y < 390):
        playGame = False

# Рисуем меню
def drawMenu():

    # Рисуем фон меню
    screen.blit(config.bgMenu, (0, 0))

    # НАЧАТЬ ЗАНОВО
    if (config.blinkMenu):
        # Мерцание первого пункта меню
        if (config.blink[0] > 0):
            config.blink[0] -= 1
            pygame.draw.rect(screen, config.defaultBgColor, (75, 125, 240, 40))
            if (config.blink[0] == 0):
                config.blink[1] = 30

        if (config.blink[1] > 0):
            config.blink[1] -= 1
            pygame.draw.rect(screen, config.selectBgColor, (75, 125, 240, 40))
            if (config.blink[1] == 0):
                config.blink[0] = 30
    else:
        pygame.draw.rect(screen, config.bgColorMenu1, (75, 125, 240, 40))

    screen.blit(config.menu1, (80, 130))

    # Не рисовать "ПРОДОЛЖИТЬ", если не нажата "НАЧАТЬ ЗАНОВО"
    if (not config.blinkMenu):
        # ПРОДОЛЖИТЬ
        pygame.draw.rect(screen, config.bgColorMenu2, (75, 170, 240, 40))
        screen.blit(config.menu2, (80, 175))

    # ЗВУК ВКЛ/ВЫКЛ
    pygame.draw.rect(screen, config.bgColorMenu3, (75, 215, 240, 40))
    screen.blit(config.menu3On if (config.soundInGame) else config.menu3Off, (80, 220))

    # МУЗЫКА ВКЛ/ВЫКЛ
    pygame.draw.rect(screen, config.bgColorMenu4, (75, 260, 240, 40))
    screen.blit(config.menu4On if (config.musicInGame) else config.menu4Off, (80, 265))

    # УПРАВЛЕНИЕ: МЫШЬ ИЛИ КЛАВИАТУРА
    pygame.draw.rect(screen, config.bgColorMenu5, (75, 305, 240, 40))
    screen.blit(config.menu5Mouse if (config.mousePlay) else config.menu5Keyboard, (80, 310))

    # ВЫХОД
    pygame.draw.rect(screen, config.bgColorMenu6, (75, 350, 240, 40))
    screen.blit(config.menu6, (80, 355))

    drawRecords(330, 130, 22, (100, 0, 0), (10, 55, 30), -1, config.text16)

    mouseClick()
    drawFloatText()

# Геттеры
def getX(obj):
    return int(obj[0])

def getY(obj):
    return int(obj[1])

# Добавляем строку к тексту
def appentTextToUpLine(text, position, color, speed, speedScale):
    config.textFloatOnScreen.append([text, position, color, speed, speedScale])

    # Чтобы не играл звук, когда конец игры
    if (config.gameState != config.ENDGAME):
        config.playSound("BONUS")

# Бегущая строка
def drawFloatText():
    for obj in config.textFloatOnScreen:
        floatTextRender = config.text16.render(obj[0], 1, obj[2])
        if (obj[1] == "START"):
            obj[1] = config.WIDTH # + config.text.size(obj[0])[0]

        screen.blit(floatTextRender, (int(obj[1]), int(config.SQUARE_SIZE * 1.3)))
        obj[1] -= obj[3]
        obj[3] *= obj[4]

    for i in range(len(config.textFloatOnScreen) - 1, -1, -1):
        if (config.textFloatOnScreen[i][1] + config.text16.size(config.textFloatOnScreen[i][0])[0] < 0):
            del config.textFloatOnScreen[i]

# Информационная строка вверху
def drawInfoLine():
    screen.blit(config.infoLineTexture, (0, 0))

    # Не допускаем вывода отрицательных значений в информационной строке
    if (config.score < 0):
        config.score = 0

    # Не допускаем вывода отрицательных значений в информационной строке
    if (config.maxPlayerRocket < 0):
        config.maxPlayerRocket = 0

    colorText = (228, 217, 161)

    infoTextRender = config.text.render(str(config.score), 1, colorText)
    screen.blit(infoTextRender, (100, 0))

    infoTextRender = config.text.render(str(config.lives), 1, colorText)
    screen.blit(infoTextRender, (418, 0))

    infoTextRender = config.text.render(str(config.level), 1, colorText)
    screen.blit(infoTextRender, (554, 0))

    # infoTextRender = config.text.render(str(len(config.invadersObject)), 1, colorText)
    infoTextRender = config.text.render(str(config.maxPlayerRocket), 1, colorText)
    screen.blit(infoTextRender, (695, 0))

# Обработка нажатий клавиш игроком
def pressPlayerKeys(v):
    if (v == "SHOOT"):
        # Не допускаем превышения максимального количества ракет. С каждым
        # уничтоженным пришельцем ракеты +1, начиная с уничтожения одного пришельца
        # 1 - +1 ракета, 2 - +1 ракета, 4 - +1 ракета и так далее
        # Начальное количество ракет: 1
        if (len(config.playerRocketObjects) < config.maxPlayerRocket):
            # Воспроизводим звук выстрела
            config.playSound("PLAYER_SHOOT")

            # Засчитываем выпущенную ракету
            config.endGameScoreCalc[9] += 1

            # Создаём и добавляем в список координаты, номер кадра и скорость
            config.playerRocketObjects.append([config.playerX + config.SQUARE_SIZE - 8,
                                               config.playerY - 16,
                                               0,
                                               config.playerRocketSpeed])
            if (config.cheat):
                # Если инопланетяне ещё остались
                if (len(config.invadersObject) > 0):
                    # Находим случайную жертву
                    n = random.randint(0, len(config.invadersObject) - 1)
                    x = getX(config.invadersObject[n])
                    y = getY(config.invadersObject[n])
                    config.playerRocketObjects[-1][0] = x + 5 + config.invadersObject[-1][3]
                    config.playerRocketObjects[-1][1] = y + config.SQUARE_SIZE * 2
        return 0

    if (v == "LEFT"):
        config.playerX -= config.playerSpeed
    elif (v == "RIGHT"):
        config.playerX += config.playerSpeed

    # Проверяем выход за границы экрана
    if (config.playerX < 0):
        config.playerX = 0
    elif (config.playerX > config.WIDTH - config.SQUARE_SIZE * 2):
        config.playerX = config.WIDTH - config.SQUARE_SIZE * 2

# Рисует супер-пришельца
def drawSuperInvaders():
    for obj in config.superInvaderObject:
        if (obj[0] == 0):
            config.playSound("SIRENA")
        screen.blit(config.superInvaderTexture[int(obj[4])], (getX(obj), getY(obj)))
        obj[4] += .1
        if (obj[4] >= len(config.superInvaderTexture)):
            obj[4] = 0
        obj[0] += obj[2]
        obj[2] *= obj[3]

    i = len(config.superInvaderObject) - 1
    while (i > -1):
        if (getX(config.superInvaderObject[i]) > config.WIDTH):
            del config.superInvaderObject[i]
        i -= 1

# Возвращает номер пришельца, в которого попала ракета
def getHit(rocket):
    i = 0
    inv = config.invadersObject
    while (i < len(inv)):
        hitX = abs(getX(rocket) - (getX(inv[i]) + 8))
        hitY = abs(getY(rocket) - getY(inv[i]))
        if (hitX < config.SQUARE_SIZE * 0.2
                and hitY < config.SQUARE_SIZE * 0.2):
            return i
        i += 1
    return None

# Проверка попадания в СУПЕР-пришельца
# Функция почти полностью повторяет getHit()
# Я не стал их объединять и оперировать аргументами
def getHitSuper(rocket):
    i = 0
    inv = config.superInvaderObject
    while (i < len(inv)):
        hitX = abs(getX(rocket) - (getX(inv[i]) + 8))
        hitY = abs(getY(rocket) - getY(inv[i]))
        if (hitX < config.SQUARE_SIZE // 2
                and hitY < config.SQUARE_SIZE // 2):
            return i
        i += 1

    return None

# Прорисовываем запущенные игроком ракеты
def drawPlayerRockets():

    # Номера для удаления из списка ракет игрока и инопланетян
    deleteNumber = []

    for i in range(len(config.playerRocketObjects)):
        # Прорисовываем и изменяем ракеты
        obj = config.playerRocketObjects[i]
        screen.blit(config.playerRocketTexture[int(obj[2])], (getX(obj), getY(obj)))
        obj[1] -= obj[3]
        obj[3] *= config.playerRocketSpeedScale
        obj[2] += 0.2
        if (obj[2] >= len(config.playerRocketTexture)):
            obj[2] = 0

        # Начинаем расчёт попаданий, когда ракета в зоне пришельцев
        if (getY(obj) < config.maxYInvaders + config.SQUARE_SIZE):
            # Находим номер пришельца, в которого попала ракета
            hittingNumber = getHit(obj)
            if (hittingNumber != None):
                config.explosionObjects.append([getX(obj) - 64, getY(obj) - 64, 0])
                # Добавляем номер пришельца, в которого попали, и номер ракеты, которая попала
                deleteNumber.append([hittingNumber, i])
            else:
                # Начинаем расчёт попаданий в СУПЕР-пришельца тогда, когда ракета в первой 1/4 экрана
                # Ниже всё равно СУПЕР-пришельцы не создаются
                if (getY(obj) < config.HEIGHT // 4):
                    hittingNumber = getHitSuper(obj)
                    if (hittingNumber != None):
                        # Создаём взрыв
                        config.explosionObjects.append([getX(obj) - 64, getY(obj) - 64, 0])

                        # Добавляем -1, чтобы не удаляло основного пришельца,
                        # и номер ракеты, которую нужно уничтожить
                        deleteNumber.append([-1, i])

                        # Уничтожаем СУПЕР-пришельца
                        del config.superInvaderObject[hittingNumber]

                        # Добавляем супер-пришельца для расчёта
                        config.endGameScoreCalc[14] += 1
                        config.nextLevelData[14] += 1

                        # Добавляем ракету за сбитого СУПЕР-пришельца
                        # (ну почему я пишу слово СУПЕР большими буквами???)
                        config.maxPlayerRocket += 1
                        appentTextToUpLine("Ракета добавлена!", "START", (255, 0, 150), random.randint(5, 7), 1)

                        # Добавляем очков за сбитого СУПЕР-пришельца
                        config.score += config.level * 100

    # Удаляем из списков по номерам, чтобы не возникало ошибки в циклах
    for i in range(len(deleteNumber) - 1, -1, -1):
        # Если попадание в пришельца из массы, а не в СУПЕР-пришельца
        if (deleteNumber[i][0] != -1):
            # Добавляем очки, считаем по формуле: (3 - Уровень противника + Уровень // 5) * 100
            config.score += (3 - config.invadersObject[deleteNumber[i][0]][2] + config.level // 5) * 100
            # Уменьшаем уровень противника
            config.invadersObject[deleteNumber[i][0]][2] -= 1

        if (config.score >= config.addingLiveStep):
            addingLive()

        # Если попадание в пришельца из массы, а не в СУПЕР-пришельца
        if (deleteNumber[i][0] != -1):
            if (config.invadersObject[deleteNumber[i][0]][2] < 0):
                # Добавляем пришельца для расчёта
                config.endGameScoreCalc[config.invadersObject[deleteNumber[i][0]][4] * 3] += 1

                # Удаляем информационный объект
                del config.invadersObject[deleteNumber[i][0]]

                # Засчитываем убийство пришельца
                config.killEnemy += 1

                if (config.killEnemy >= config.nextPlayerRocket):
                    config.nextPlayerRocket *= 2
                    config.maxPlayerRocket += 1
                    appentTextToUpLine("Ракета добавлена!", "START", (255, 0, 150), random.randint(5, 7), 1)

        config.playSound("ENEMY_KILL")
        del config.playerRocketObjects[deleteNumber[i][1]]

    # Удаляем вышедшие за экран ракеты
    i = 0
    while (i < len(config.playerRocketObjects)):
        if (getY(config.playerRocketObjects[i]) < 0):
            config.score -= 50
            if (config.score < 0):
                config.score = 0
            del config.playerRocketObjects[i]
        else:
            i += 1

# Вывод текстур взрыва
def drawExplosion():
    i = 0
    while (i < len(config.explosionObjects)):
        obj = config.explosionObjects[i]
        # Проигрываем взрыв если только кадр №0
        if (obj[2] == 0):
            config.playSound("EXPLOSION_ALIEN")
        screen.blit(config.explosionTexture[obj[2]], (getX(obj), getY(obj)))
        obj[2] += 1
        if (obj[2] >= len(config.explosionTexture)):
            del config.explosionObjects[i]
        else:
            i += 1

# Бомба попала в игрока
def killPlayerBomb():
    config.playSound("PLAYER_DEATH")

    # Игрока в центр!
    config.resetPlayer()
    # Уменьшаем жизнь
    config.lives -= 1

    # Уничтожаем все летящие бомбы пришельцев
    if (len(config.invadersBombObject) > 0):
        del config.invadersBombObject[:]

    # Уничтожаем все выпущенные ракеты
    if (len(config.playerRocketObjects) > 0):
        del config.playerRocketObjects[:]

    # За гибель ставим 1 ракету
    config.maxPlayerRocket = 1
    config.nextPlayerRocket = 1
    config.killEnemy = 0
    appentTextToUpLine("Вы погибли", "START", (255, 255, 255), 2, 1)

# Выводим бомбы пришельцев
def drawBombInvaders():
    deleteBomb = []
    killPlayer = False
    for i in range(len(config.invadersBombObject)):
        obj = config.invadersBombObject[i]
        screen.blit(config.invadersBombTexture[obj[4]], (getX(obj), getY(obj)))
        obj[4] += 1
        if (obj[4] >= len(config.invadersBombTexture)):
            obj[4] = 0

        obj[0] += obj[2]
        obj[2] *= config.invadersBombStopHorizontalSpeed
        obj[1] += obj[3]
        obj[3] *= config.invadersSpeedBombScale

        # Проверяем на столкновение с игроком
        if (getY(obj) >= config.playerY):
            if (getX(obj) > config.playerX - config.SQUARE_SIZE
                and getX(obj) < config.playerX + config.SQUARE_SIZE * 2):
                config.explosionObjects.append([getX(obj) - 64, getY(obj) - 64, 0])
                killPlayer = True
                deleteBomb.append(i)

        # Индексы тех бомб, которые вышли за пределы экрана по Y,
        # добавляем для удаления
        if (getY(obj) > config.HEIGHT + config.SQUARE_SIZE):
            deleteBomb.append(i)

    # Удаляем вышедшие за пределы экрана бомбы по индексам
    for i in deleteBomb:
        if (i < len(config.invadersBombObject)):
            del config.invadersBombObject[i]

    if (killPlayer):
        killPlayerBomb()

# Выводим текстуру игрока
def drawPlayer():
    screen.blit(config.playerTexture, (int(config.playerX), int(config.playerY)))

# Прорисовываем инопланетян
def drawInvaders():
    # Произошло ли смещение вниз?
    dropDown = False

    for obj in config.invadersObject:
        # Отрисовываем инопланетянина
        screen.blit(config.invadersTexture[obj[2] * 2 + int(config.frame)], (getX(obj), getY(obj)))
        if (countFPS % 50 == 0):
            # obj[3] хранит значение скорости
            obj[0] += obj[3] # config.invadersSpeed

            if (getX(obj) >= config.WIDTH - config.SQUARE_SIZE
                or getX(obj) <= 0):
                dropDown = True

            if (getY(obj) > config.maxYInvaders):
                config.maxYInvaders = getY(obj)

    if (config.maxYInvaders > 350):
        if (countFPS % 700 == 0):
            config.playSound("ALARM")

    # Если пришельцы "придавили" игрока, зайдя за нижнюю точку
    if (config.maxYInvaders > 400):
        config.lives = -1

    # Кадр для отрисовки инопланетянина
    config.frame += 0.05
    if (config.frame >= 2):
        config.frame = 0

    # Если соприкосновение с границами экрана произошло
    if (dropDown):
        config.playSound("SIDEKICK")

        # Спускаем инопланетную армаду вниз
        for obj in config.invadersObject:
            obj[3] = -obj[3]
            obj[0] += obj[3]
            obj[3] *= config.invadersSpeedScale
            if (obj[3] > config.maxInvadersSpeed):
                obj[3] = config.maxInvadersSpeed
            # Спускаем инопланетян на значение 0.8 от SQUARE_SIZE вниз
            obj[1] += int(config.SQUARE_SIZE * 0.8)

# Удаляем всё
def nextLevelReset():
    global countFPS

    # Изменяем состояние игры
    config.gameState = config.NEXTLEVEL

    # Приостанавливаем воспроизведение музыки
    config.playSound("BACKGROUND_MUSIC_PAUSE")

    # Добавляем общий счётчик ракет
    config.nextLevelData[9] = config.maxPlayerRocket
    config.screenScore = 0

    if (len(config.playerRocketObjects) > 0):
        del config.playerRocketObjects[:]
    if (len(config.invadersBombObject) > 0):
        del config.invadersBombObject[:]
    if (len(config.superInvaderObject) > 0):
        del config.superInvaderObject[:]

    del config.textFloatOnScreen[:]
    appentTextToUpLine("ВЫ ПРОХОДИТЕ НА СЛЕДУЮЩИЙ УРОВЕНЬ!", "START", (200, 200, 100), 5, 1)

    # Добавляем рекламный случайный баннер
    if (random.randint(0, 100) < 25):
        config.advertising.append([config.bannerName[random.randint(0, len(config.bannerName) - 1)],
                                   0, 0, 220, 0])
    countFPS = 0

# Прорисовываем объекты игры
def drawGame():
    global countFPS

    # Рисуем фоновый космос
    screen.blit(config.backGround, (0, 0))

    # Если не осталось инопланетян
    if (len(config.invadersObject) == 0):
        nextLevelReset()
        return 0

    # Принятие решения о запуске ракеты
    l = len(config.invadersObject) - 1
    if (l > 0):
        if (random.randint(0, 5000) < l):
            n = random.randint(0, l)

            # Список по формату: [x, y, Горизонтальная скорость, Вертикальная скорость, Номер кадра]
            # 50% вероятности, что ракета полетит влево или вправо
            calcSpeed = abs(2 + int(config.invadersObject[n][3]) * 2)
            horizontalSpeed = random.randint(1, calcSpeed) // 10
            if (random.randint(0, 9) < 5):
                horizontalSpeed = -horizontalSpeed

            config.invadersBombObject.append([getX(config.invadersObject[n]),
                                              getY(config.invadersObject[n]),
                                              horizontalSpeed,
                                              config.invadersSpeedBomb,
                                              0])
            config.playSound("BOMB_START")


    # Принятие решения о запуске СУПЕР-ПРИШЕЛЬЦА
    if (config.level > 3
        and random.randint(0, 100000 // config.level) < 10):
        config.superInvaderObject.append([0,
                                          config.SQUARE_SIZE + random.randint(0, config.SQUARE_SIZE * 2),
                                          random.randint(5, 15) / 10,
                                          1,
                                          0])

    # СУПЕР-пришелец стреляет суперскоростной ракетой
    if (len(config.superInvaderObject) > 0
        and (random.randint(0, 50000 // config.level) < 50)):
        n = random.randint(0, len(config.superInvaderObject) - 1)
        config.invadersBombObject.append([getX(config.superInvaderObject[n]),
                                          getY(config.superInvaderObject[n]),
                                          0,
                                          config.invadersSpeedBomb * 3,
                                          0])
        config.playSound("BOMB_START")



    drawInvaders()
    drawPlayer()
    drawPlayerRockets()
    drawBombInvaders()
    if (len(config.superInvaderObject) > 0):
        drawSuperInvaders()

    drawBrick()
    if (countFPS % 3 == 0):
        checkHitRocketsAndBomb()

    drawExplosion()
    drawFloatText()
    drawInfoLine()

    if (config.lives < 0):
        config.lives = 0
        goEndGame()


# Сброс объектов в начальное состояние
def reset():
    # Список объектов-инопланетян
    del config.invadersObject[:]

    # Список объектов-СУПЕР-инопланетян
    del config.superInvaderObject[:]

    # Сброс координат игрока
    config.resetPlayer()

    # Вычисляем ширину и высоту блока инопланетян
    countWidth = 1 + int(config.level * 0.5)
    countHeight = 1 + int(config.level * 0.18)

    # Проверяем, чтобы не было слишком много
    if (countWidth > 20):
        countWidth = 20
    if (countHeight > 8):
        countHeight = 8

    # Коэффициент - дистанция между столбцами в рядах инопланетян
    distanceCoeff = 1.1
    startX = config.WIDTH // 2 - countWidth * (config.SQUARE_SIZE * distanceCoeff) // 2
    startY = config.SQUARE_SIZE * 2

    # Считаем ранги в массе инопланетян
    allInvaders = countWidth * countHeight

    # Проценты от общего количества для разных цветов пришельцев
    percentRed = config.level / 100
    if (percentRed > 1):
        percentRed = 1
    percentYellow = config.level / 100 * 2
    if (percentYellow > 1):
        percentYellow = 1

    red = int(allInvaders * percentRed)
    yellow = int((allInvaders - red) * percentYellow)
    green = int(allInvaders - red - yellow)

    # Компенсируем, если расчёты не дали нужное число
    green += allInvaders - (green + yellow + red)

    rangInvaders = [0 for i in range(green)]
    rangInvaders += [1 for i in range(yellow)]
    rangInvaders += [2 for i in range(red)]

    config.nextLevelData[0] = green
    config.nextLevelData[3] = yellow
    config.nextLevelData[6] = red

    # Перемешиваем список
    random.shuffle(rangInvaders)
    countRang = 0

    # Создаём список с данными о пришельцах
    for i in range(countWidth):
        for j in range(countHeight):

            rang = rangInvaders[countRang]
            countRang += 1

            # Объекты: [Координата X, Координата Y, Ранг, Скорость]
            config.invadersObject.append([startX + i * config.SQUARE_SIZE * 1.1,
                                         startY + j * config.SQUARE_SIZE * 1.1,
                                         rang,
                                         config.invadersSpeed,
                                         rang])

    # Максимальная нижняя точка инопланетян (последний пришелец)
    config.maxYInvaders = getY(config.invadersObject[len(config.invadersObject) - 1])

    countBrick = config.level // 5
    if (countBrick > 20):
        countBrick = 20

    distanceBrick = config.WIDTH // (countBrick + 1)

    # Формат данных каждого блока: [x, y, Признак отображения]
    config.brickObject = []

    for i in range(countBrick):
        for j in range(4):
            config.brickObject.append([distanceBrick * (1 + i) + j * 8 - 16,
                                       config.HEIGHT - config.SQUARE_SIZE * 3,
                                       True])

        for j in range(6):
            config.brickObject.append([distanceBrick * (1 + i) + j * 8 - 24,
                                       config.HEIGHT - config.SQUARE_SIZE * 3 + 8,
                                       True])

# Следующий уровень
def nextLevel(isMenu):
    global countFPS

    # Сбрасываем кадры
    countFPS = 0

    # Увеличиваем номер уровня
    config.level += 1

    # Управление количеством ракет для запуска
    config.maxPlayerRocket = 1
    config.nextPlayerRocket = 1
    config.killEnemy = 0

    # Вычисляем скорость пришельцев для уровня
    # Скорость: количество клеток, на которые перемещается
    # пришелец за один кадр
    config.invadersSpeed = 20 + config.level / 5
    if (config.invadersSpeed > config.maxInvadersSpeed):
        config.invadersSpeed = config.maxInvadersSpeed

    # Состояние игры: ИГРА в том случае, если
    # не нужно показывать меню. Как, например,
    # в самом начале игры
    if (isMenu):
        config.gameState = config.MENU
    else:
        config.gameState = config.GAME

# Старт игры с заданными параметрами
def startNewGame(l, s, isMenu):
    config.playSound("BACKGROUND_MUSIC_UNPAUSE")
    config.level = l
    config.score = s

    # Когда игра стартует с открытым меню, то "моргать" первым пунктом "Начать заново"
    config.blinkMenu = isMenu

    nextLevel(isMenu)
    reset()


# ПОЛНЫЙ сброс игры
def fullReset(l, s, isMenu):
    # Играем фоновую музыку
    if (not isMenu):
        config.playSound("BACKGROUND_MUSIC_PLAY")

    # Удаляем и сбрасываем всё
    del config.invadersBombObject[:]
    del config.playerRocketObjects[:]
    del config.textFloatOnScreen[:]
    del config.explosionObjects[:]

    # Сбрасываем жизни
    config.lives = config.defaultLives

    config.playerName = ""

    config.endGameScoreCalc = [0, 0, True, 0, 0, True, 0, 0, True, 0, 0, True, "Reseved", False, 0, 0, True]
    config.resetNextLevelData()

    # Стартуем с состоянием меню "isMenu"
    startNewGame(l, s, isMenu)

def main():
    global screen, playGame, eventPygame, countFPS

    # Формирование и расположение окна по центру
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.mixer.pre_init(22050, -16, 2, 512)
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Космовойны")
    pygame.display.set_icon(pygame.image.load("icon/icon.ico"))

    # Определение текста
    config.setFont()

    # Настройка ФПС
    clock = pygame.time.Clock()
    countFPS = 0

    # Загрузка текстур
    config.loading()

    # Старт игры
    fullReset(0, 0, True)

    # Главный цикл игры
    playGame = True

    while playGame:

        # Счётчик кадров
        countFPS += 1
        if (countFPS > 1000000):
            countFPS = 0

        eventPygame = pygame.event.get()
        for event in eventPygame:
            # Закрытие окна
            if (event.type == pygame.QUIT):
                config.saveSetup()
                playGame = False
            # Проверяем, нажата ли левая кнопка и бахаем
            elif (event.type == pygame.MOUSEBUTTONDOWN
                  and event.button == 1
                  and config.gameState == config.GAME):
                if (not config.mouseShoot):
                    # Чтобы выстрелы не шли друг за другом
                    config.mouseShoot = True
                    pressPlayerKeys("SHOOT")
            # Меню по правой кнопке мыши
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not config.blinkMenu):
                if (config.gameState == config.GAME or config.gameState == config.MENU):
                    config.playSound("MENU")
                    if (config.gameState == config.MENU):
                        config.gameState = config.GAME
                    else:
                        config.gameState = config.MENU
            # Разблокировка выстрела
            elif (event.type == pygame.MOUSEBUTTONUP or
                    event.type == pygame.MOUSEMOTION):
                config.mouseShoot = False
            # Нажатие Escape
            elif (event.type == pygame.KEYDOWN
                  and (config.gameState == config.GAME or config.gameState == config.MENU)):
                if (event.key == pygame.K_ESCAPE
                        and (config.gameState == config.GAME or config.gameState == config.MENU) and not config.blinkMenu):

                    config.playSound("MENU")
                    if (config.gameState == config.GAME):
                       config.gameState = config.MENU
                    else:
                       config.gameState = config.GAME
                if (event.key == pygame.K_SPACE and config.gameState == config.GAME):
                    pressPlayerKeys("SHOOT")

        # --------------- ЭКРАН ИГРЫ - ВСЁ ДВИЖЕТСЯ И ШЕВЕЛИТСЯ
        if (config.gameState == config.GAME):
            # Проверяем управление: мышь или клавиатура
            if (config.mousePlay):
                # Работаем с позицией мыши
                x, y = pygame.mouse.get_pos()
                if (x < config.playerX + config.SQUARE_SIZE // 2):
                    pressPlayerKeys("LEFT")
                if (x > config.playerX + config.SQUARE_SIZE * 1.5):
                    pressPlayerKeys("RIGHT")
            else:
                # Работаем с клавиатурой
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_LEFT]):
                    pressPlayerKeys("LEFT")
                if (keys[pygame.K_RIGHT]):
                    pressPlayerKeys("RIGHT")
            # Прорисовываем элементы игры
            drawGame()
        # --------------- ЭКРАН МЕНЮ
        elif (config.gameState == config.MENU):
            # Прорисовываем элементы меню
            drawMenu()
        # --------------- ЭКРАН ПЕРЕКЛЮЧЕНИЯ НА СЛЕДУЮЩИЙ УРОВЕНЬ
        elif (config.gameState == config.NEXTLEVEL):
            # Экран переключения на следующий уровень
            if (len(config.explosionObjects) == 0):
                drawNextLevel()
            else:
                drawInfoLine()
                drawExplosion()
        # --------------- ЭКРАН КОНЦА ИГРЫ
        elif (config.gameState == config.ENDGAME):
            # Экран переключения на сцену конца игры
            if (len(config.explosionObjects) == 0):
                drawEndGame()
            else:
                drawInfoLine()
                drawExplosion()
        # --------------- Таблица очков в финале игры
        elif (config.gameState == config.CHECKSCORE):
            drawFinalRecord()
        # --------------- Ожидание и сброс после ввода ника игроком
        elif (config.gameState == config.WAITPRESSRMB):
            waitPressRMB()

        pygame.display.update()
        clock.tick(config.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
