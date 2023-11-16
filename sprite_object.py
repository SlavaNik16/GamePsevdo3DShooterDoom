import pygame

import Level
import Setting
import interaction
import player
from Setting import *
from collections import deque #Импортируем очередь из модуля коллекции, она позволяет очень быстро просматривать массив, с помощью ritate
from ray_casting import mapping
from numba.core import types
from numba.typed import Dict
from numba import int32



#Класс в котором будут хранится типы спрайтов
class Sprites:
    def __init__(self):
        #типы спрайтов будем распологать в словаре
        self.sprite_parameters = {
            'sprite_barrel': {#Ключем будет название спрайтов
                'Name': 'Barrier ', #его имя
                'health': 3, #жизни спрайта
                'hd_ratio': 3 / Setting.bar_lenght, #коэффициент для прямоугольника
                'damage_mon': 0.0, #какой урон отнимает спрайт
                'speed': 0, #Скорость монстра
                'sprite': pygame.image.load('sprites/barrei/base/0.png').convert_alpha(), #кортинка самого спрайта
                'viewing_angles': None,#Переменованный параметр статик
                'shift': 1.8, #Сдвиг
                'scale': (0.4, 0.4), #Масштаб
                'side': 50, #Размер
                'animation': deque( #Анимация спрайта
                    [pygame.image.load(f'sprites/barrei/anim/{i}.png').convert_alpha() for i in range(12)]), #проматывает 12 фотографий
                'death_animation': deque([pygame.image.load(f'sprites/barrei/death/{i}.png')
                                          .convert_alpha() for i in range(4)]), #анимация смерти спрайта
                'is_dead': None, #Жив ли объект
                'dead_shift': 2.6, #сдвиг спрайта после его гибели
                'animation_dist': 800, #Какое расстояние должно быть от игрока до спрайта, чтобы началась анимация
                'animation_speed': 10, #Скорость анимации
                'blocked': True, #Нельзя пройти спрайта насквозь
                'flag': 'decor', #тип спрайта: декор
                'obj_action': [], #что делает объект при виде игрока
                'score': 10,
            },
            'sprite_pin': {
                'Name': None,
                'health': 500,
                'hd_ratio': 500 / Setting.bar_lenght,
                'damage_mon': 0.0,
                'speed': 0,
                'sprite': pygame.image.load('sprites/pin/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.6,
                'scale': (0.6, 0.6),
                'side': 30,
                'animation': deque([pygame.image.load(f'sprites/pin/anim/{i}.png').convert_alpha() for i in range(8)]),
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': None,
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'decor',
                'obj_action': [],
                'score': 0,
            },
            'sprite_flame': {
                'Name': None,
                'health': 500,
                'hd_ratio': 500 / Setting.bar_lenght,
                'damage_mon': 5.0,
                'speed': 0,
                'sprite': pygame.image.load('sprites/flame/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.7,
                'scale': (0.6, 0.6),
                'side': 30,
                'animation': deque(
                    [pygame.image.load(f'sprites/flame/anim/{i}.png').convert_alpha() for i in range(16)]),
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 1.8,
                'animation_dist': 1800,
                'animation_speed': 5,
                'blocked': None,
                'flag': 'decor',
                'obj_action': [],
                'score': 0,
            },
            'npc_devil': {
                'Name': 'Diablo  ',
                'health': 500,
                'hd_ratio': 500 / Setting.bar_lenght,
                'damage_mon': 10.0,
                'speed': 0.7,
                'sprite': [pygame.image.load(f'sprites/devil/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.0,
                'scale': (2.1, 1.1),
                'side': 30,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/devil/death/{i}.png')
                                           .convert_alpha() for i in range(6)]),
                'is_dead': None,
                'dead_shift': 0.6,
                'animation_dist': None,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque(
                    [pygame.image.load(f'sprites/devil/anim/{i}.png').convert_alpha() for i in range(9)]),#анимация движение монстра за игроком
                'score': 200,
            },
            'sprite_door_v':{
                'Name': 'Door    ',
                'health': 30,
                'hd_ratio': 30 / Setting.bar_lenght,
                'damage_mon': 0.0,
                'speed': 0,
                'sprite': [pygame.image.load(f'sprites/doors/door_v/{i}.png').convert_alpha() for i in range(16)],
                'viewing_angles': True,
                'shift': 0.1,
                'scale': (2.6, 1.2),
                'side': 100,
                'animation': [],
                'death_animation': [1],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'door_v',
                'obj_action': [],
                'score': 1,
            },
            'sprite_door_h': {
                'Name': 'Door    ',
                'health': 30,
                'hd_ratio': 30 / Setting.bar_lenght,
                'damage_mon': 0.0,
                'speed': 0,
                'sprite': [pygame.image.load(f'sprites/doors/door_h/{i}.png').convert_alpha() for i in range(16)],
                'viewing_angles': True,
                'shift': 0.1,
                'scale': (2.6, 1.2),
                'side': 100,
                'animation': [],
                'death_animation': [1],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'door_h',
                'obj_action': [],
                'score': 1,
            },
            'npc_soldier0': {
                'Name': 'Spetsnaz',
                'health': 30,
                'hd_ratio': 30 / Setting.bar_lenght,
                'damage_mon': 0.5,
                'speed': 1,
                'sprite': [pygame.image.load(f'sprites/npc/soldier0/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.8,
                'scale': (0.4, 0.6),
                'side': 30,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/npc/soldier0/death/{i}.png')
                                         .convert_alpha() for i in range(6)]),
                'is_dead': None,
                'dead_shift': 1.7,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(f'sprites/npc/soldier0/action/{i}.png')
                                    .convert_alpha() for i in range(4)]),
                'score': 5,
            },
            'npc_soldier1': {
                'Name': 'Zombie  ',
                'health': 30,
                'hd_ratio': 20 / Setting.bar_lenght,
                'damage_mon': 0.5,
                'speed': 1,
                'sprite': [pygame.image.load(f'sprites/npc/soldier1/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.8,
                'scale': (0.4, 0.6),
                'side': 50,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/npc/soldier1/death/{i}.png')
                                         .convert_alpha() for i in range(11)]),
                'is_dead': None,
                'dead_shift': 1.7,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(f'sprites/npc/soldier1/action/{i}.png')
                                    .convert_alpha() for i in range(4)]),
                'score': 5,
            },
            'npc_devil1': {
                'Name': 'Killer',
                'health': 120,
                'hd_ratio': 120 / Setting.bar_lenght,
                'damage_mon': 7,
                'speed': 1.5,
                'sprite': [pygame.image.load(f'sprites/npc/devil1/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.8,
                'scale': (0.4, 0.6),
                'side': 50,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/npc/devil1/death/{i}.png')
                                         .convert_alpha() for i in range(11)]),
                'is_dead': None,
                'dead_shift': 1.7,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(f'sprites/npc/devil1/action/{i}.png')
                                    .convert_alpha() for i in range(6)]),
                'score': 50,
            },
            'small_kit': {
                'Name': 'HP',
                'health': None,
                'hd_ratio': None,
                'damage_mon': None,
                'speed': 0,
                'sprite': [pygame.image.load(f'sprites/bonus/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.8,
                'scale': (0.6, 0.6),
                'side': 10,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 1.7,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': False,
                'flag': 'bonusHP',
                'obj_action': [],
                'score': 0,
            },

        }


        #создаем карту с расположение спрайта и с его указанием ключа

        self.list_of_objects = [
            SpriteObject(self.sprite_parameters['sprite_door_v'], (4.5,7.5)),
            SpriteObject(self.sprite_parameters['npc_soldier0'], (10, 10)),
            SpriteObject(self.sprite_parameters['npc_soldier1'], (10, 10)),
            SpriteObject(self.sprite_parameters['npc_devil1'], (10, 10)),
            SpriteObject(self.sprite_parameters['small_kit'], (12, 12)),


        ]

        self.list_of_objects1 = [
            SpriteObject(self.sprite_parameters['npc_soldier0'], (15, 15)),
            SpriteObject(self.sprite_parameters['npc_soldier1'], (1.27, 11.5)),
            SpriteObject(self.sprite_parameters['small_kit'], (12, 12)),
        ]

    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in Setting.list_object], default=(float('inf'), 0)) #Возвращает близайший спрайт, если много спрайтов
    #оказалось под выстрелом

    @property
    def blocked_doors(self):#создаем функцию которая будет возвращать словарь всех закрытых дверейsssss
        blocked_doors = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        for obj in Setting.list_object: #если объект является дверью
            if obj.flag in {'door_h', 'door_v'} and obj.blocked:
                i, j = mapping(obj.x, obj.y) #располагаем двери на позиции
                blocked_doors[(i, j)] = 0
        return blocked_doors


#В этом классе будем вычислять  место положения спрайта и его  проекционные характеристики
class SpriteObject:
    def __init__(self, parameters, pos):
        #Инициализируем все атрибуты
        self.object = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift'] #Атрибут сдвига по высоте
        self.scale = parameters['scale'] #Атрибут нужен для масштабируемости картинки
        self.animation = parameters['animation'].copy()
        # ---------------------
        self.death_animation = parameters['death_animation'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']
        # ---------------------
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.flag = parameters['flag']
        self.obj_action = parameters['obj_action'].copy()
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.side = parameters['side']
        self.dead_animation_count = 0
        self.animation_count = 0
        self.npc_action_trigger = False #параметр счетчика
        self.door_open_trigger = False #тригер для открытия дверей
        self.door_prev_pos = self.y if self.flag == 'door_h' else self.x #делеаем значение предыдущей позиции к  двери
        self.delete = False #для удаление объекта
        self.distance_to_sprite = 10000
        self.distance = 10000
        #health
        self.health = parameters['health']
        self.hp_ratio = parameters['hd_ratio']
        if Setting.shot == True:
            Setting.cur = self.health
            Setting.hp_rat = self.hp_ratio
        else:
            Setting.cur = 0
        #Name
        self.name = parameters['Name']
        #damage monsters
        self.damage_mon = parameters['damage_mon']
        self.score = parameters['score']

        self.speed = parameters['speed']



        if self.viewing_angles: #Счетчик анимации
            if len(self.object) == 8:
                # сформируем диапозоны углов для каждого спрайта, так как картинок 8, то на каждый спрайт приходится диапозон в 45 градусов
                self.sprite_angles = [frozenset(range(338, 360)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 360)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)} # использую замороженные множества

    def health_monster(self):  # возвращает нам проекцию спрайта, который находится под огнем
        health = self.health
        return health

    @property
    def is_on_fire(self): #возвращает нам проекцию спрайта, который находится под огнем
        if CENTER_RAY - self.side // 2 < self.current_ray < CENTER_RAY + self.side // 2 and self.blocked:
            return self.distance_to_sprite, self.proj_height #Если спрайт расположен на центральномлуче и немного от него, то это спрайт находится под огнем
        return float('inf'), None

    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, player):
        dx, dy = self.x - player.x, self.y - player.y #находим координаты между игроком и спрайтом

        self.distance = math.sqrt(dx * dx + dy * dy)
        self.distance_to_sprite = math.sqrt(dx * dx + dy * dy) #вычисляем расстояние  до спрайта
        self.theta = math.atan2(dy, dx) #угол, под которым смотрит спрайт на игрока
        gamma = self.theta - player.angle #вычисляем угол между взглядом игрока и спрайтом
        #с помощью условий, находим угол gamma, который будет находится в нужных пределах
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI #при невыполнение условий нужно коректировать прибавляя 2 * pi, в зависимости от расположения игрока
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / DELTA_ANGLE) #находим смещение спрайта относительно центрального луча
        # корректируем расстояние до спрайта, чтобы не было эффекта рыбьего глаза
        self.current_ray = CENTER_RAY + delta_rays
        if self.flag not in {'door_h', 'door_v'}: #для дверей вводим условие, для некоторых вычислений
            self.distance_to_sprite *= math.cos(HALF_FOV - self.current_ray * DELTA_ANGLE)

        fake_ray = self.current_ray + FAKE_RAYS #делаем фейковые лучи и отображаем там спрайта(за пределами экрана)
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.distance_to_sprite > 30:
            self.proj_height = min(int(PROJ_COEFF / self.distance_to_sprite),
                                   DOUBLE_HEIGHT if self.flag not in {'door_h', 'door_v'} else HEIGHT) # вычисляем проекционный рассчет о высоте спрайта
            sprite_width = int(self.proj_height * self.scale[0]) #для адекватного масштабирование спрайта
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2 # Коэффициент масшубирования ширины и высоты спрайта
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift # делаем механизм регулирования спрайта  по высоте

            # logic for doors, npc, decor
            if self.flag in {'door_h', 'door_v'}: #в случае срабатывание тригера для двери
                if self.door_open_trigger:
                    self.open_door() #мы запускае функцию открытие двери
                self.object = self.visible_sprite()
                sprite_object = self.sprite_animation()
            else:
                if self.is_dead and self.is_dead != 'immortal': #Если спрайт умер
                    sprite_object = self.dead_animation() #проигрываем анимацию смерти
                    shift = half_sprite_height * self.dead_shift # меняем сдвиг смерти
                    sprite_height = int(sprite_height / 1.3) #и уменьшаем высоту спрайта
                    #if sprite_object:
                        #self.delete = True
                elif self.npc_action_trigger: #анимация на взаимодействия с игроком
                    sprite_object = self.npc_in_action()
                else: #и включаем начальную анимацию для спрайтов
                    self.object = self.visible_sprite()
                    sprite_object = self.sprite_animation()



            # sprite scale and pos
            # вычесляем позицию спрайта относительно его места(луча)
            sprite_pos = (self.current_ray * SCALE - half_sprite_width, HALF_HEIGHT - half_sprite_height + shift)# совмещаем центр спрайта с его лучом
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height)) # масштабируем спрайт по размеру его проекции
            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def sprite_animation(self):
        if self.animation and self.distance_to_sprite < self.animation_dist: #Если расстояния до спрайта меньше устанновленного значения, то
            sprite_object = self.animation[0] #мы будем отображать на экране спрайт, который первый по очереди
            if self.animation_count < self.animation_speed: #отображать бужем столько раз, сколько заложено в параметре скорости
                self.animation_count += 1
            else:
                self.animation.rotate()#если скорость анимации будет равен количеству, то мы прокручиваем анимацию методом rotate()
                self.animation_count = 0
            return sprite_object
        return self.object

    def visible_sprite(self):

        if self.viewing_angles:
            # Алгоритм выбора правильного спрайта от зрения
            if self.theta < 0: # корректируем угол тета, чтобы он находился в пределах от 0 до 2*pi
                self.theta += DOUBLE_PI
            self.theta = 360 - int(math.degrees(self.theta))

            # Проходимся по списку с углами
            for angles in self.sprite_angles:
                if self.theta in angles: # как только угол попадет  в один из диапозонов
                    return self.sprite_positions[angles] # то нужным спрайтом будет значение по ключю(от этого угла)
        return self.object

    def dead_animation(self):
        if len(self.death_animation):
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0
        return self.dead_sprite

    def npc_in_action(self):
        sprite_object = self.obj_action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.obj_action.rotate()
            self.animation_count = 0
        return sprite_object
    def open_door(self):
        if self.flag == 'door_h':
            self.y -= 50 #с такой скоростью дверь будет уходить в стену
            if abs(self.y - self.door_prev_pos) > TILE: #После того ка дверь пройдет больше расстояние клетки на карте
                self.delete = True #мы ее удаляем
        elif self.flag == 'door_v':
            self.x -= 50
            if abs(self.x - self.door_prev_pos) > TILE:
                self.delete = True


