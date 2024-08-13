import pygame

import math

pygame.init()
pygame.display.set_caption("Летающие шары")

width = 800
height = 480
win = pygame.display.set_mode((width, height))
nn = 2

rB = []   # радиус шара
mB = []   # масса 
xB = []   # координата X центра
yB = []   # координата Y центра
aB = []   # направление 
vB = []   # скорость 
cB = []   # цвет

for i in range(nn+1):
    rB.append(25*i)
    mB.append(rB[i] ** 2)
    xB.append(i * 400)
    yB.append(height // 2)
    aB.append(i * math.pi / 3)
    vB.append(2*i)
    cB.append(0)

cB[1] = (255, 0, 0)
cB[2] = (0, 255, 0)

def ProverkaSten():
    for i in range(1, nn + 1):
        if xB[i] <= rB[i] and (aB[i] > math.pi / 2 or aB[i] < -math.pi / 2): # левая стена
            aB[i] = math.pi - aB[i]
        if xB[i] >= width - rB[i] and (aB[i] > -math.pi / 2 and aB[i] < math.pi /2): # правая стена
            aB[i] = math.pi - aB[i]
        if yB[i] <= rB[i] and (aB[i] < 0 and aB[i] > -math.pi): # верхняя стена
            aB[i] = -aB[i]
        if yB[i] >= height - rB[i] and (aB[i] > 0 and aB[i] < math.pi): # нижняя стена
            aB[i] = -aB[i]
        while aB[i] > math.pi: aB[i] -= 2 * math.pi
        while aB[i] < -math.pi: aB[i] += 2 * math.pi

def BallsStolkn():
    for i in range(1, nn + 1):
        for j in range(i + 1, nn + 1):
            # Расстояние между шарами
            Rast = ((xB[i] - xB[j]) ** 2 + (yB[i] - yB[j]) ** 2) ** 0.5
            if Rast <= rB[i] + rB[j]:
                xB1new = xB[i] + vB[i] * math.cos(aB[i])
                yB1new = yB[i] + vB[i] * math.sin(aB[i])
                xB2new = xB[j] + vB[j] * math.cos(aB[j])
                yB2new = yB[j] + vB[j] * math.sin(aB[j])
                # Новое расстояние
                RastNew = ((xB1new - xB2new) ** 2 + (yB1new - yB2new) ** 2) ** 0.5
                if Rast > RastNew: # столкновение при сближении
                    # Угол поворота луча от центра шара на центр,
                    # с которым произошло столкновение
                    BB = math.atan((yB[j] - yB[i]) / (xB[j] - xB[i]))
                    if (xB[j] - xB[i]) < 0:
                        BB += math.pi
                        while BB > math.pi / 2: BB -=2 * math.pi
                        while BB < -math.pi / 2: BB += 2* math.pi
                    # Угол от луча до направления движения
                    W1 = aB[i] - BB
                    W2 = aB[j] - BB

                    # Проекция скорости на луч и на перпендекуляр
                    # к нему до столкновения
                    Vw1 = vB[i] * math.cos(W1)
                    Vw2 = vB[j] * math.cos(W2)
                    Vwt1 = vB[i] * math.sin(W1)
                    Vwt2 = vB[j] * math.sin(W2)

                    # Проекция скорости на луч после столкновения
                    # (проекция скорости на препендикуляр к оси W не изменяется)
                    Vw1 = (2 * mB[j] * vB[j] * math.cos(W2) + (mB[i]-
                        mB[j]) * vB[i] * math.cos(W1)) / (mB[i] + mB[j])
                    Vw2 = (2 * mB[i] * vB[i] * math.cos(W1) + (mB[j] -
                        mB[i]) * vB[j] * math.cos(W2)) / (mB[i] + mB[j])

                    # Скорости после столкновения
                    vB[i] = (Vw1 ** 2 + Vwt1 ** 2) ** 0.5
                    vB[j] = (Vw2 ** 2 + Vwt2 ** 2) ** 0.5

                    # Угол от луча до направления движения после столкновения
                    W1 = math.atan(Vwt1/Vw1)
                    if Vw1 < 0: W1 += math.pi
                    W2 = math.atan(Vwt2/Vw2)
                    if Vw2 < 0: W2 += math.pi

                    # Новое результирующее направление движения после столкновения
                    aB[i] == BB + W1
                    while aB[i] > math.pi: aB[i] -= 2 * math.pi
                    while aB[i] < -math.pi: aB[i] += 2 * math.pi
                    aB[j] = BB + W2
                    while aB[j] > math.pi: aB[j] -= 2 * math.pi
                    while aB[j] < -math.pi: aB[j] += 2 * math.pi
    
var_ = True

while var_:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            var_ = False

    win.fill((255, 255, 255))

    # Движение шаров
    for i in range(1, nn + 1):
        xB[i] += vB[i] * math.cos(aB[i])
        yB[i] += vB[i] * math.sin(aB[i])
        pygame.draw.circle(win, cB[i], (xB[i], yB[i]), rB[i])

    pygame.time.delay(24)
    pygame.display.update()

    # Столкновение со стеной
    ProverkaSten()

    # Столкновения шаров
    BallsStolkn()
                
pygame.quit()
