import math

#Game setting
from collections import deque

import pygame

WIDTH = 1200 #Ширина
HEIGHT = 800 #Высота
Condition = 0 # -1 - конец игры 0 - игра,  1 - магазин 2 - меню
Condition_Update = 0 #3 - Обновление для Condition 1 - магазин
shop = False # включение и выключение магазина
HALF_WIDTH = WIDTH // 2 #Доп. константа обознащающая половину ширины
HALF_HEIGHT = HEIGHT // 2 #Доп. константа обознащающая половину высоты
PENTA_HEIGHT = 5 * HEIGHT
DOUBLE_HEIGHT = 2 * HEIGHT
FPS = 100 #Нужно для кадров в секунду (чтобы отрегулировать скорость)
TILE = 100 #Размер карты
FPS_POS =  (WIDTH - 65, 5) #Указываем позицию отрисовки FPS на экране

# minimap setting
MINIMAP_SCALE = 10 #Уменьшаем размер в столько то раз(масштабируемый коеффициэнт)
MINIMAP_RES = (WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE) # Вводим числовой коэффициент, чтобы весь мир отобразился на карте
MAP_SCALE =  2 * MINIMAP_SCALE # 1 -> 12 * 8, 2 -> 24 * 16,  3 -> 36 * 24  # Здесь мы увеличили карту в 2 раза
MAP_TILE = TILE // MAP_SCALE #Масшт. коеф. для стороны квадрата
MAP_POS = (WIDTH-120, HEIGHT - HEIGHT //MINIMAP_SCALE ) #позиция мини карты на экране


#ray casting setting
FOV = math.pi / 3  #Область видимости лучей
HALF_FOV = FOV / 2 #Доп. переменная
NUM_RAYS = 300 #Количество лучей (зрение игрока)
MAX_DEPTH = 800 #Максимальное расстояние луча(дальность прорисовки(взгляда))
DELTA_ANGLE = FOV / NUM_RAYS #Угол между нашими лучами
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV)) #Вычисляем дистанцию игрока до нашего экрана
PROJ_COEFF = 3 * DIST * TILE #Проекционный коэффициэент стен
SCALE = WIDTH // NUM_RAYS #Масштабирующий коеффициэнт(чтобы проект не тормозил) (алгоритм строим стены по закрашенным прямоугольникам)

# Sprite setting
DOUBLE_PI = 2 * math.pi #делаем константу
CENTER_RAY = NUM_RAYS // 2 - 1 # и передаем номер центрального луча
FAKE_RAYS = 100 # Создаем фейковые лучи, чтобы устранить недостаток отображения спрайтов по центральному лучу
FAKE_RAYS_RANGE = NUM_RAYS - 1 + 2 * FAKE_RAYS
list_object = []
sum=0

#Texture setting(1200 * 1200)
TEXTURE_WIDTH = 1200 #Ширина текстуры
TEXTURE_HEIGHT = 1200#Высота текстуры
HALF_TEXTURE_HEIGHT = TEXTURE_HEIGHT // 2
TEXTURE_SCALE = TEXTURE_WIDTH // TILE #Масштабируемый коэффициент, чтобы полностью влезла в квадрат карты


#Player setting
Name_player = 'Anonim'
Name_Count = 1
player_pos = (125, 755) #Его позиция в левом верхнем углу
player_angle = 135 #Направления взгляда
player_speed = 1 #Скорость передвижения
hil = 15
talent_points = 10
score = 0
damage = 0
levelUp = 1
stamina = 200
run = False
max_stamine = 200
rang_player = 0
rang_player_count = 9
playerPosMap_width = 0
playerPosMap_height = 0




#Cartridges
ArmsShotgun1 = 25
ArmsShotgun1Max = 50
ArmsShotgun2 = 10
ArmsShotgun2Max = 15

#Sound
sound_cout_shotgun = 1
sound_cout_сannonLaser = 1

#Доп. переменные
one = 1
shot = False


#Monster health
cur = 1
bar_lenght = 480
hp_rat = 1
Name = 'MONSTER'


#WeponNumberCold
wep = 1.0

#Face
face = 0

#dir
direct = [0,0,0]
dir = 0

#Raising
Damage_Rais = 0
Damage_Step = 2

#Colors цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (220, 220, 0)
SANDY = (244, 164, 96)
DARKBROWN = (97, 61, 25)
DARKORANGE = (255, 140 , 0)
LEATHER  = (114, 69, 40)
