import pygame

import Level
import Setting

from sprite_object import *
from Setting import *
from numba import njit

@njit(fastmath = True)
#Проверка попадания луча в карту
def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE ) * TILE

@njit(fastmath = True)
#Функция которая возвращает список параметров , как дальность от стены и область расположения
def ray_casting(player_pos, player_angle, world_map, WW,WH):
    casted_walls = []  #Создаем список для фирмирование текстур во 2 функции
    ox, oy = player_pos #Определяем начальные координаты луча
    texture_v, texture_h = 1, 1 # Задаем дефолтные номера для горизонтальных и вертикальных стен
    xm, ym = mapping(ox, oy) #а также координаты левого верхняго угла
    cur_angle = player_angle - HALF_FOV #Находим линию нашего луча
    for ray in range(NUM_RAYS): #делаем цикл по все лучам
        sin_a = math.sin(cur_angle) #Вычисляем углы этих направлений лучей
        sin_a = sin_a if sin_a else 0.000001
        cos_a = math.cos(cur_angle)
        cos_a = cos_a if cos_a else 0.000001
        #Алгоритм прохождение лучей по вертикалям или горизонталям, для более сильной оптимизации
        #verticals
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1) #тернарный оператор
        # if cos_a >= 0: #косинус луча определяет в какую сторону идти по вертекалям, если >=0 , то берем правые от нас вертикали
        #     x = xm + TILE #определяем текущую вертикаль
        #    dx = 1 #вспомогательная переменная, при помощи которой будем получать вспомогательную вертикаль
        # else: # иначе левые
        #    x = xm
        #    dx = -1
        #с помощью цикла пробегаем по всем вертикалям в цикле(т.е по ширине экрана)
        for i in range(0, WW, TILE):
            depth_v = (x - ox) / cos_a #находим расстояние по вертикали
            yv = oy + depth_v * sin_a #и координату y(вертикали))
            tile_v =  mapping(x + dx, yv)
            if tile_v in world_map: #проводим проверка столкновения со стеной
                texture_v = world_map[tile_v] # определяем номер текстуры, когда натыкаемся на припятствие
                break #если докоснулись стены прекращаем
            x += dx * TILE # переходим к следующей вертикали

        #horizontals
        #Если sin a >= 0 то проверяем верхние вертикали, если нет но нижние
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, WH, TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * TILE

        # projection
        #выбераем какая из точек пересечения (вертикальная или горизантальная) ближе
        #можно взять код из определение размера проекции и препятсвия

        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h) #определяем смещение на текстуре, а также его номер текстуры
        offset = int(offset) % TILE #вычислем смещение путем нахождение остатка от квадртата карты
        #Убираем эффект рыбьего глада(возникает в результате евклидового расстояния)
        depth *= math.cos(player_angle - cur_angle) #Наше расстояние нужно умножить на сos угла разницы(основного направления и направлении текущего луча)
        depth = max(depth, 0.00001) #избегаем ошибки игры деления на 0
        proj_height = int(PROJ_COEFF / depth) #Вычисляем проекционную высоту стены

        #Для каждого луча мы заносим дальность до стены, сдвиг по текстуре, проекционная высота, номер текстуры
        casted_walls.append((depth, offset, proj_height, texture))
        cur_angle += DELTA_ANGLE #Изменение угла для очередного луча
    return casted_walls

def ray_casting_walls(player, textures):
    world_map = Level.world_map()
    WORLD_WIDTH = Level.WORDLD_WIDTH()
    WORLD_HEIGHT = Level.WORDLD_HEIGHT()

    casted_walls = ray_casting(player.pos, player.angle, world_map, WORLD_WIDTH, WORLD_HEIGHT)
    wall_shot = casted_walls[CENTER_RAY][0], casted_walls[CENTER_RAY][2] #Расположение пули оружия
    walls = []  #Список расчета позиция по текстуре
    for ray, casted_values in enumerate(casted_walls):
        depth, offset, proj_height, texture = casted_values

        if proj_height > HEIGHT:  #когда проекционная высота стены больше высоты экрана
            coeff = proj_height / HEIGHT  #Берем еще меньший коэффициент
            texture_height = TEXTURE_HEIGHT / coeff  #и уменьшаем во сколько то раз, как будет высота экрана
            #выделяем под поверхностью из нашей текстуры в виде квадрата, в котором начальные координаты
            #равны вычисленному смещению  текстуры
            wall_colum = textures[texture].subsurface(offset * TEXTURE_SCALE,
                                                     HALF_TEXTURE_HEIGHT - texture_height // 2,
                                                     TEXTURE_SCALE,texture_height)
            #масштубируем выделенную часть текстуры
            wall_colum = pygame.transform.scale(wall_colum, (SCALE, HEIGHT))
            wall_pos = (ray * SCALE, 0)
        else:
            wall_colum = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall_colum = pygame.transform.scale(wall_colum, (SCALE, proj_height))
            wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)#вычисляем главную поверхность, в зависимости от нумераций луча
        walls.append((depth, wall_colum, wall_pos))
    return walls, wall_shot
