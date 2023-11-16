#Импортируем
import Setting
import player
from Setting import *
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32

def level(self):
    world_map[(Setting.playerPosMap_width , Setting.playerPosMap_height)] = 0


_ = False # Взята переменная для удобства проектирования
matrix_map = [ #Создаем карту в цифровом ввиде
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, 2, _, _, _, 1, 1, 1, _, _, _, _, 1, 1, 1, _, _, _, _, _, 1],
    [1, _, _, _, 2, _, _, _, _, 1, _, _, _, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, _, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, 3, _, _, _, _, _, _, _, _, _, 5],
    [1, 1, 1, 1, 1, _, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, 1, 1],
    [1, _, _, _, 3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 3, _, _, _, _, 1, _, _, _, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, _, _, _, 3, _, _, _, 1, 1, 1, _, _, _, _, 1, 1, 1, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Определяем новые значения для размера мира(нужны дальше для работы лучей)

WORLD_WIDTH = len(matrix_map[0]) * TILE
WORLD_HEIGHT = len(matrix_map) * TILE
world_map = Dict.empty(key_type = types.UniTuple(int32, 2), value_type = int32) #будет держать координаты стен в структуре данных типа словарь
mini_map = set() #структура для мини карты
collision_walls = []; #делаем список стен

#Делаем цикл, где
# цифра отвечает за номер текстуры
# а элементы строк координата x
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            mini_map.add((i * MAP_TILE, j * MAP_TILE)) #добавляем мини карту
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            # Заносим в словарь только стены.
            if char == 0:
                 world_map[(i * TILE, j * TILE)] = 0
            elif char == 1:  #все ключи словаря будут координаты стен
                 world_map[(i * TILE, j * TILE)] = 1 #значение -это номера текстур
            elif char == 2:
                 world_map[(i * TILE, j * TILE)] = 2
            elif char == 3:
                 world_map[(i * TILE, j * TILE)] = 3
            elif char == 4:
                 world_map[(i * TILE, j * TILE)] = 4
            elif char == 5:
                 world_map[(i * TILE, j * TILE)] = 5
                 Setting.playerPosMap_width = i * TILE
                 Setting.playerPosMap_height = j * TILE


