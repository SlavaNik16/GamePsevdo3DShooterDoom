import pygame
import Setting           #Импортируем все, что находится в папке Setting
import sprite_object
from player import Player #Импортируем класс Player, который находится в папке player
from sprite_object import *
from ray_casting import ray_casting_walls
from drawing import Drawing
from interaction import Interaction


pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT)) #Задаем значение экрана
sc_map = pygame.Surface(MINIMAP_RES) #отрисовываем мини карту на отдельной поверхности уменьшенной в столько то раз
pygame.display.set_caption("GamePsevdo3DShooter")
pygame.display.set_icon(pygame.image.load('img/icons/icon.png'))

sprites = Sprites()
clock = pygame.time.Clock() #Создаем объект Класса clock, для желаемого количества кадров в сек.
player = Player(sprites) #Создаем объект Класса Player
drawing = Drawing(sc, sc_map, player, clock) #создаем обхект класса Drawing
interaction = Interaction(player, sprites, drawing)

drawing.menu()
pygame.mouse.set_visible(False) #Отключаем указатель мыши

#interaction.play_music()


while Setting.Condition == 0:  # Основной цикл игры
    player.movement()  # Вызываем метод, на каждой итерации цикла (вид того, что игрок ходит)
    drawing.bacground(player.angle)  # в построение фона передадим значение угла, чтобы сделать небо динамическим
    walls, wall_shot = ray_casting_walls(player, drawing.textures)  # возвращает номер списка стен

    drawing.world(walls + [obj.object_locate(player) for obj in Setting.list_object])  # передаем список параметров стен и спрайтовf
    drawing.fps(clock)
    if Setting.wep == 1:
        Setting.damage = 10 + Setting.Damage_Rais
        drawing.player_weapon([wall_shot, sprites.sprite_shot])
    elif Setting.wep == 2 or Setting.wep == 2.5:
        Setting.damage = 50 + Setting.Damage_Rais
        drawing.player_weapon2([wall_shot, sprites.sprite_shot])

    drawing.basic_health()
    drawing.panel()
    drawing.mini_map(player)

    interaction.interaction_objects()
    interaction.npc_action()
    interaction.clear_world()
    interaction.check_win()
    if Setting.Condition == 1:
        drawing.shop()
    if Setting.Condition == 2:
        drawing.menu()

    if Setting.Condition_Update == 1:
        Setting.Condition = 1
        Setting.Condition_Update = 0
        drawing.shop()

    pygame.display.flip()  # Обновляем содержимое(так как в цикле, то на каждой итерации)
    clock.tick(FPS)

#if Setting.Condition == -1 :


