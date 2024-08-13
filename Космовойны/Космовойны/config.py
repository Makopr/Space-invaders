import pygame

# Загрузка текстур и прочего
def loading():
    global backGround, bgMenu, backendgame, invadersTexture, soundMove, \
        playerTexture, playerRocketTexture, explosionTexture, \
        invadersBombTexture, infoLineTexture, superInvaderTexture, \
        brickTexture, bannerName

    # Фон игры и фон меню
    backGround = pygame.image.load("image/background.jpg")
    bgMenu = pygame.image.load("image/bgmenu.jpg")
    backendgame = pygame.image.load("image/backendgame.jpg")

    # Фон для информационной строки
    infoLineTexture = pygame.image.load("image/infoline.png")

    # Рекламные баннеры
    bannerName.append(pygame.image.load("image/banner01.png"))
    bannerName.append(pygame.image.load("image/banner02.png"))

    # Формирование списка с текстурами СУПЕР-инопланетянина
    superInvaderTexture = []
    superInvaderTexture.append(pygame.image.load("image/super_inv01.png"))
    superInvaderTexture.append(pygame.image.load("image/super_inv02.png"))
    superInvaderTexture.append(pygame.image.load("image/super_inv03.png"))
    superInvaderTexture.append(pygame.image.load("image/super_inv04.png"))

    # Формирование списка с текстурами инопланетян
    invadersTexture = []
    invadersTexture.append(pygame.image.load("image/inv01.png"))
    invadersTexture.append(pygame.image.load("image/inv01_move.png"))
    invadersTexture.append(pygame.image.load("image/inv02.png"))
    invadersTexture.append(pygame.image.load("image/inv02_move.png"))
    invadersTexture.append(pygame.image.load("image/inv03.png"))
    invadersTexture.append(pygame.image.load("image/inv03_move.png"))

    # Формирование списка с текстурами снарядов инопланетян
    invadersBombTexture = []
    invadersBombTexture.append(pygame.image.load("image/bomb_invaders/bomb_invaders01.png"))
    invadersBombTexture.append(pygame.image.load("image/bomb_invaders/bomb_invaders02.png"))
    invadersBombTexture.append(pygame.image.load("image/bomb_invaders/bomb_invaders03.png"))
    invadersBombTexture.append(pygame.image.load("image/bomb_invaders/bomb_invaders04.png"))

    # Загрузка текстуры космического корабля игрока
    playerTexture = pygame.image.load("image/player.png")

    # Формирование списка с текстурами пользовательской ракеты
    playerRocketTexture = []
    playerRocketTexture.append(pygame.image.load("image/player_rocket/rocket01.png"))
    playerRocketTexture.append(pygame.image.load("image/player_rocket/rocket02.png"))
    playerRocketTexture.append(pygame.image.load("image/player_rocket/rocket03.png"))
    playerRocketTexture.append(pygame.image.load("image/player_rocket/rocket04.png"))

    explosionTexture = []
    explosionTexture.append(pygame.image.load("image/expl/expl01.png"))
    explosionTexture.append(pygame.image.load("image/expl/expl02.png"))
    explosionTexture.append(pygame.image.load("image/expl/expl03.png"))
    explosionTexture.append(pygame.image.load("image/expl/expl04.png"))
    explosionTexture.append(pygame.image.load("image/expl/expl05.png"))
    explosionTexture.append(pygame.image.load("image/expl/expl06.png"))
    explosionTexture.append(pygame.image.load("image/expl/expl07.png"))
    explosionTexture.append(pygame.image.load("image/expl/expl08.png"))

    brickTexture = pygame.image.load("image/brick.png")

    # =========== ЗВУКИ ================
    soundMove = []
    # Удар о борт
    soundMove.append(pygame.mixer.Sound("sound/sidekick.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[0], 0.4)

    # Выстрел игрока
    soundMove.append(pygame.mixer.Sound("sound/player_rocket.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[1], 0.5)

    # Меню
    soundMove.append(pygame.mixer.Sound("sound/menu.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[2], 0.5)

    # Взрыв пришельца
    soundMove.append(pygame.mixer.Sound("sound/expl.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[3], 1)

    # Пришелец убит совсем
    soundMove.append(pygame.mixer.Sound("sound/enemy_kill.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[4], 0.2)

    # Запуск бомбы пришельцем
    soundMove.append(pygame.mixer.Sound("sound/bomb_start.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[5], 0.7)

    # В пользователя попала бомба
    soundMove.append(pygame.mixer.Sound("sound/player_death.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[6], 0.8)

    # Добавлена жизнь
    soundMove.append(pygame.mixer.Sound("sound/adding_live.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[7], 0.6)

    # Сирена
    soundMove.append(pygame.mixer.Sound("sound/sirena.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[8], 0.2)

    # Очки добавлены
    soundMove.append(pygame.mixer.Sound("sound/plusscore.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[9], 0.9)

    # Следующий уровень
    soundMove.append(pygame.mixer.Sound("sound/nextlevel.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[10], 0.3)

    # Клик при добавлении очков за инопланетян
    soundMove.append(pygame.mixer.Sound("sound/tick.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[11], 0.4)

    # Экран с финалом
    soundMove.append(pygame.mixer.Sound("sound/theend.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[12], 0.8)

    # Рекордное количество очков
    soundMove.append(pygame.mixer.Sound("sound/tablerecord.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[13], 0.9)

    # Звук клавиатуры
    soundMove.append(pygame.mixer.Sound("sound/keypress.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[14], 0.8)

    # Тревога
    soundMove.append(pygame.mixer.Sound("sound/alarm.ogg"))
    pygame.mixer.Sound.set_volume(soundMove[15], 0.8)

# Как воспроизводить звук?
# Вызвать playSound с "командой", которая проверяется в условии.
# В зависимости от "команды" (event) воспроизводится звук
def playSound(event):
    if (soundInGame):
        if (event == "SIRENA"):
            soundMove[8].play(2)
        else:
            if (event == "SIDEKICK"):
                soundMove[0].play()
            elif (event == "PLAYER_SHOOT"):
                soundMove[1].play()
            elif (event == "MENU"):
                soundMove[2].play()
            elif (event == "EXPLOSION_ALIEN"):
                soundMove[3].play()
            elif (event == "ENEMY_KILL"):
                soundMove[4].play()
            elif (event == "BOMB_START"):
                soundMove[5].play()
            elif (event == "PLAYER_DEATH"):
                soundMove[6].play()
            elif (event == "BONUS"):
                soundMove[7].play()
            elif (event == "PLUSSCORE"):
                soundMove[9].play()
            elif (event == "NEXTLEVEL"):
                soundMove[10].play()
            elif (event == "TICK"):
                soundMove[11].play()
            elif (event == "THEEND"):
                soundMove[12].play()
            elif (event == "TABLERECORD"):
                soundMove[13].play()
            elif (event == "PRESSKEY"):
                soundMove[14].play()
            elif (event == "ALARM"):
                soundMove[15].play()

    if (event == "NONE"):
        for obj in soundMove:
            pygame.mixer.Sound.stop(obj)

    if (event == "BACKGROUND_MUSIC_PLAY"):
        if (musicInGame):
            pygame.mixer.music.load("sound/music.ogg")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    if (event == "BACKGROUND_MUSIC_PAUSE"):
        if (musicInGame):
            pygame.mixer.music.pause()
    elif (event == "BACKGROUND_MUSIC_UNPAUSE"):
        if (musicInGame):
            pygame.mixer.music.unpause()

# Установка текста
def setFont():
    global text, text16, text20, text32, text80, \
           menu1, menu2, menu3On, menu3Off,menu4On, menu4Off,menu5Mouse, menu5Keyboard, menu6, \
           bgColorMenu1, bgColorMenu2, bgColorMenu3, bgColorMenu4, bgColorMenu5, bgColorMenu6
    text = pygame.font.Font("font/oldfont.ttf", 25)
    text16 = pygame.font.Font("font/scores.ttf", 16)
    text20 = pygame.font.Font("font/oldfont.ttf", 20)
    text32 = pygame.font.Font("font/oldfont.ttf", 32)
    text80 = pygame.font.Font("font/oldfont.ttf", 80)

    menu1 = text.render("Начать заново", 1, (37, 37, 37))
    menu2 = text.render("Продолжить", 1, (37, 37, 37))
    menu3On = text.render("Звук: ВКЛ", 1, (37, 37, 37))
    menu3Off = text.render("Звук: ВЫКЛ", 1, (37, 37, 37))
    menu4On = text.render("Музыка: ВКЛ", 1, (37, 37, 37))
    menu4Off = text.render("Музыка: ВЫКЛ", 1, (37, 37, 37))
    menu5Mouse = text.render("Мышь", 1, (37, 37, 37))
    menu5Keyboard = text.render("Клавиатура", 1, (37, 37, 37))
    menu6 = text.render("Выход", 1, (37, 37, 37))

    bgColorMenu1 = defaultBgColor
    bgColorMenu2 = defaultBgColor
    bgColorMenu3 = defaultBgColor
    bgColorMenu4 = defaultBgColor
    bgColorMenu5 = defaultBgColor
    bgColorMenu6 = defaultBgColor

# Запись рекордов игры
def saveRecords(scoresToFile):
    try:
        f = open("scores.dat", "w", encoding="utf-8")
        for sc in scoresToFile:
            f.write(f"{sc[0]} {sc[1]} {sc[2]}\n")
        f.close()
    except:
        print("Что-то пошло не так.")

# Загрузка рекордов игры
def loadRecords():
    global records
    records = []
    try:
        f = open("scores.dat", "r", encoding="utf-8")
        for sc in f.readlines():
            newSc = sc.replace("\n", "")
            newSc = newSc.split(" ")

            # Формат рекордов: НИК УРОВЕНЬ ОЧКИ
            if (len(newSc[0]) > 20):
                newSc[0] = newSc[0][0:20]
            elif (newSc[0] == ""):
                newSc[0] = defaultName

            # Преобразовываем число (это номер уровня)
            newSc[1] = int(newSc[1])
            if (newSc[1] > 200):
                newSc[1] = 200
            elif (newSc[1] < 0):
                newSc[1] = 0

            # Преобразовываем число (это количество очков)
            newSc[2] = int(newSc[2])
            if (newSc[2] > 1000000):
                newSc[2] = 1000000
            elif (newSc[2] < 0):
                newSc[2] = 0
            records.append(newSc)
        f.close()
    except:
        print("Файла не существует")

    if (len(records) != 10):
        records = []
        for i in range(10):
            records.append([defaultName, 0, 0])
        saveRecords(records)

# Загрузка настроек из файла setup.dat
def loadSetup():
    global soundInGame, musicInGame, mousePlay
    soundInGame = True
    musicInGame = True
    mousePlay = False
    try:
        f = open("setup.dat", "r", encoding="utf-8")
        s = f.readline()
        f.close()
        # Выражение True if (s[0] == "1") else False
        # тернарный оператор
        soundInGame = True if (s[0] == "1") else False
        musicInGame = True if (s[1] == "1") else False
        mousePlay = True if (s[2] == "1") else False
    except:
        saveSetup()

# В файле одна строка, состоящая из двух символов
# Каждый символ может принимать 1 или 0, Истину или Ложь
# Первая единица - звук, вторая - музыка
# 00 - выключить все звуки
# 11 - все звуки включены
# 01 - звук выключен, музыка включена
# 10 - звук включен, музыка выключена
def saveSetup():
    s = "1" if (soundInGame) else "0"
    s += "1" if (musicInGame) else "0"
    s += "1" if (mousePlay) else "0"
    try:
        f = open("setup.dat", "w", encoding="utf-8")
        f.write(s)
        f.close()
    except:
        print("Файл не создан, печаль.")

# Сброс координат игрока
def resetPlayer():
    global playerX, playerY, playerSpeed
    playerX = WIDTH // 2 - SQUARE_SIZE
    playerY = HEIGHT - SQUARE_SIZE * 1.25
    playerSpeed = playerSpeedDefault

# Сброс настроек для отображения окна между уровнями
def resetNextLevelData():
    global nextLevelData, counterScoreUnit, newRecord
    nextLevelData = [0, 0, True, 0, 0, True, 0, 0, True, 0, 0, True, 4, False, 0, 0, True]
    counterScoreUnit = [0, 0, 0, 0, 0]
    newRecord = -1

# =========== НАСТРОЙКИ И ОПРЕДЕЛЕНИЕ ПЕРЕМЕННЫХ =============
# Ширина и высота окна
WIDTH = 800
HEIGHT = 480

# Размер текстуры инопланетянина
SQUARE_SIZE = 32

# Экран pygame
screen = None

# Частота кадров в секунду
FPS = 60

# Коды состояний игры
MENU = 0
GAME = 1
NEXTLEVEL = 2
ENDGAME = 3
CHECKSCORE = 4
WAITPRESSRMB = 5

# Состояние игры:
gameState = None

# Фоновые изображения игры и меню
backGround = None
bgMenu = None

# Цвет обычного и подсвеченного пунктов меню
defaultBgColor = (230, 230, 230)
selectBgColor = (220, 0, 0)

# Загрузка настроек из файла
loadSetup()

# Баннер: [Изображение, Прошло кадров, Альфа-канал, Пауза (кадров)]
advertising = []
bannerName = []

# ============ ИНОПЛАНЕТЯНЕ ==============
# Текстуры инопланетян
invadersTexture = None

# Кадр
frame = 0

# Скорость инопланетян
invadersSpeed = None
invadersSpeedScale = 1.15
maxInvadersSpeed = 50

# Список с информационными объектами пришельцев
# Формат: [Координата X, Координата Y, Ранг, Скорость, Ранг для расчёта в финале]
invadersObject = []

# Максимальная нижняя точка инопланетной армады
maxYInvaders = None

# ============ СУПЕР-ПРИШЕЛЕЦ =====================
superInvaderTexture = None
# Формат: [x, y, Скорость по горизонтали, Ускорение, Кадр]
superInvaderObject = []


# ============ СНАРЯДЫ ПРИШЕЛЬЦЕВ =====================
invadersBombTexture = None

# Список для хранения координат бомб противника
# по формату: [x, y, Горизонтальная скорость, Вертикальная скорость, Номер кадра]
invadersBombObject = []
invadersSpeedBomb = 0.3
invadersSpeedBombScale = 1.036
invadersBombStopHorizontalSpeed = 0.995

# ============ ИГРОК =====================
playerTexture = None
playerX = None
playerY = None
playerSpeed = None
playerSpeedDefault = 2

# Текстура ракеты
playerRocketTexture = None

# Объекты: список по формату [x, y, кадр, скорость]
playerRocketObjects = []
playerRocketSpeed = 0.5
playerRocketSpeedScale = 1.02

# Максимальное количество выстрелов
maxPlayerRocket = 1

# Сколько нужно убить пришельцев для +1 ракеты?
nextPlayerRocket = 1

# Убито пришельцев
killEnemy = 0

# Ник по умолчанию
playerName = ""
defaultName = "Makopr"
# Допустимые символы
characterSet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstufvwxyz0123456789!-_"
# Для мерцания курсора
blink = [30, 0]
# Мерцать ли первым пунктом меню?
blinkMenu = True


# ============ ВЗРЫВ =====================
explosionTexture = None
explosionObjects = []

# ============ УРОВЕНЬ =====================
level = 1
score = 0
defaultLives = 3
lives = defaultLives

# Количество очков, начисляемых при смене уровня
greenScore = 100
yellowScore = 200
redScore = 400
blueScore = 750
rocketScore = 500

# Добавление жизней после очков:
addingLiveStep = 10000
addingLiveStepScale = 2


# ============ ВСПЛЫВАЮЩИЕ НАДПИСИ =====================
# Формат ["Текст", координата по X, (Цвет), Скорость, Ускорение]
textFloatOnScreen = []

# ============ КИРПИЧИ =====================
brickTexture = None
brickObject = None

# ============ ПЕРЕКЛЮЧЕНИЕ НА СЛЕДУЮЩИЙ УРОВЕНЬ =====================
# Формат списка: [0 - кол-во зелёных инопланетян, 1 - очки за них, 2 - считаем (анимация?),
#                 3 - кол-во жёлтых инопланетян, 4 - очки за них, 5 - считаем (анимация?),
#                 6 - кол-во красных инопланетян, 7 - очки за них, 8 - считаем (анимация?),
#                 9 - кол-во оставшихся ракет? 10 - очки за них, 11 - считаем (анимация?),
#                 12 - счётчик для смены цифр, 13 - отображаем его?]
#                 14 - кол-во синих ХУХЪ, 15 - очки за них, 16 - считаем? (анимация)

nextLevelData = []

# Счётчик количества для расчёта очков при смене уровня
# [Зелёные, Жёлтые, Красные, Ракеты]
counterScoreUnit = []

# Список для хранения ОБЩЕГО количества инопланетян, уничтоженных за всё время игры
# И общего количества потраченных ракет для штрафов
# Формат списка: [0 - кол-во зелёных, 1 - очки за них, 2 - считаем? (анимация),
#                 3 - кол-во жёлтых, 4 - очки за них, 5 - считаем? (анимация),
#                 6 - кол-во красных, 7 - очки за них, 8 - считаем? (анимация)]
#                 9 - кол-во ракет, 10 - очки за них, 11 - считаем (анимация?),
#                 12 - резерв, 13 - закончился ли счёт?
#                 14 - кол-во синих ХУХЪ, 15 - очки за них, 16 - считаем? (анимация)

endGameScoreCalc = []


# Сбрасываем значения
resetNextLevelData()


# Сколько позиций с числом очков за инопланетян отрисовываем
screenScore = 0

# Блокируем двойное нажатие мыши
mouseShoot = False

# Если рекорд, то какое место в списке?
newRecord = None

# ЧИТ
cheat = False

loadRecords()
