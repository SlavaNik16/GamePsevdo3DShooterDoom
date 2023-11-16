import Level
import Setting
import drawing
import time
import map1
import map2
import player
import sprite_object
from Setting import *
from map1 import *
from ray_casting import mapping
import math
import pygame
from numba import njit

@njit(fastmath=True, cache=True)
def ray_casting_npc_player(npc_x, npc_y, blocked_doors, world_map, player_pos):

    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y #находится ли персонаж в прямой области с npc или нет
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = math.sin(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(cur_angle)
    cos_a = cos_a if cos_a else 0.000001

    # verticals
    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // TILE):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in world_map or tile_v in blocked_doors:
            return False
        x += dx * TILE

    # horizontals
    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // TILE):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in world_map or tile_h in blocked_doors: #так же чтобы npc не видели нас через двери
            return False
        y += dy * TILE
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.pain_sound = pygame.mixer.Sound('sound/pain.wav')

    def interaction_objects(self):
        world_map = Level.world_map()
        if self.player.shot and self.drawing.shot_animation_trigger: #находится ли какой нибудь живой объект в области выстрела
            for obj in sorted(Setting.list_object, key=lambda obj: obj.distance_to_sprite):
                if obj.is_on_fire[1] and ( self.player.current_time - self.player.previous_time > 500):
                    self.player.previous_time = self.player.current_time
                    if obj.is_dead != 'immortal' and not obj.is_dead:
                        if ray_casting_npc_player(obj.x, obj.y,
                                                  self.sprites.blocked_doors,
                                                  world_map, self.player.pos): #расположение двери на карте
                            if obj.flag == 'npc' or obj.flag == 'decor': #Если попали по нпс, то будем загружать звук
                               Setting.cur = obj.health #сохраняем здоровье каждого монстра
                               Setting.hp_rat = obj.hp_ratio #сохраняем пропорцию здоровья каждого монстра
                               Setting.Name = obj.name #сохраняем имя того монстра которого мы убиваем
                               obj.health -= Setting.damage #если попал выстрелом, снимаем у монстра здоровье
                               # уменьшаем шкалу здороья
                               if Setting.cur > 0:
                                   Setting.cur -= Setting.damage
                               if Setting.cur <= 0:
                                   Setting.cur = 0
                            # Если здоровье падает до 0, то монстр мертв и воспроизводим крики
                            if Setting.cur == 0:
                               if (obj.flag != 'decor'):
                                   self.pain_sound.play()
                               obj.is_dead = True
                               obj.blocked = None
                               Setting.score += obj.score
                               self.drawing.shot_animation_trigger = False
                    if obj.flag in {'door_h', 'door_v'} and obj.distance_to_sprite < TILE: #условием открытие двери будет выстрел по ней, с расстояние меньше клетки на карте
                        Setting.cur = obj.health  # сохраняем здоровье каждого монстра
                        Setting.hp_rat = obj.hp_ratio  # сохраняем пропорцию здоровья каждого монстра
                        Setting.Name = obj.name
                        obj.health -= Setting.damage
                        if Setting.cur > 0:
                            Setting.cur -= Setting.damage
                        if Setting.cur <= 0:
                            Setting.cur = 0
                        if Setting.cur == 0:
                           obj.door_open_trigger = True
                           obj.blocked = None
                           Setting.score += obj.score
                    break
    def npc_action(self): #делаем взаимодействие c npc
        world_map = Level.world_map()
        for obj in Setting.list_object:
            if obj.flag == 'npc' and not obj.is_dead and obj.flag != 'bonusHP':
                if ray_casting_npc_player(obj.x, obj.y,
                                          self.sprites.blocked_doors,
                                          world_map, self.player.pos): #если нпс находится на прямой видимости с игроком
                    obj.npc_action_trigger = True
                    self.npc_move(obj)
                else:
                    obj.npc_action_trigger = False
            elif obj.flag == 'bonusHP':
                 self.npc_hil(obj)

    def npc_hil(self, obj):
        if obj.distance < TILE-20:
            Setting.hil += 0.5
            obj.delete = True


    def npc_move(self, obj): #движение нпс на игрока
        if obj.distance >= TILE / 2: #Будет двигатся тогда, когда расстояние до него будет больше размера клетки на карте
            dx = obj.x - self.player.pos[0]
            dy = obj.y - self.player.pos[1]
            obj.x = obj.x + obj.speed if dx < 0 else obj.x - obj.speed
            obj.y = obj.y + obj.speed if dy < 0 else obj.y - obj.speed
        else:
            Setting.hil -= obj.damage_mon
            obj.delete = True
            if Setting.hil <= 0:
               Setting.Condition = -1



    def clear_world(self): #Удалем ненужные вещи(открытые двери? убираем тела после смерти)
        deleted_objects = Setting.list_object[:]
        [Setting.list_object.remove(obj) for obj in deleted_objects if obj.delete]

    def clear_world_Up(self):  # Удалем ненужные вещи(открытые двери? убираем тела после смерти)
        Setting.list_object.clear()




#
    def play_music(self): #Добавляем музыку
        pygame.mixer.pre_init(44100,-16,2,2048) #настраиваем музыку
        pygame.mixer.init() #включаем музыку
        pygame.mixer.music.load('sound/theme.mp3') #Ставим производится
        pygame.mixer.music.play(10) #Запускаем до начала главного цикла

    def check_win(self): #Концовка игры
        if not len([obj for obj in self.sprites.list_of_objects if obj.flag == 'npc' and not obj.is_dead]):
            #pygame.mixer.music.stop() #Останавливаем текущую музыку и ставим новую
            #pygame.mixer.music.load('sound/win.mp3')

            if (Setting.levelUp == 1):
                map1.level(self)
                x = round(self.player.pos[0] / 10000, 2)
                y = round(self.player.pos[1] / 10000, 2)
                x *= 10000
                y *= 10000
                #if ((self.player.x >= 2240) and (self.player.x  <= 2275) and (self.player.y  >= 725) and (self.player.y  <= 775)):
                if (Setting.playerPosMap_width == (int)(x) and Setting.playerPosMap_height == (int)(y)):
                    Setting.levelUp = 2
            self.sprites.list_of_objects = Setting.list_object

#
