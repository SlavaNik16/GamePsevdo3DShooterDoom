
from _ast import Lambda
import pygame

import Level
import Setting
import interaction
import map1
import map2
import player
import sprite_object
from Setting import *
from ray_casting import ray_casting
from map1 import *
from collections import deque
from random import randrange
import sys
import pyautogui

#В этом классе мы будет рисовать/отрисовывать все в игре
class Drawing:
    def __init__(self, sc, sc_map, player, clock): #Здесь мы будем отображать нашу поверхность
        self.sc = sc
        self.sc_map = sc_map
        self.player = player
        self.clock = clock
        self.font = pygame.font.SysFont('Arial', 35, bold = True) #Меняем шрифт , чтобы отрисовывать текст на экране
        #создаем словарь текстур для загрузки текстуры
        self.font_win = pygame.font.Font('font/font.ttf', 144)
        self.textures = { 0: pygame.image.load('img/Vrata.png').convert(),
                          1: pygame.image.load('img/wall3.png').convert(),
                          2: pygame.image.load('img/wall4.png').convert(),
                          3: pygame.image.load('img/wall5.png').convert(),
                          4: pygame.image.load('img/wall6.png').convert(),
                          5: pygame.image.load('img/door_exit.png').convert(),
                          's': pygame.image.load('img/sky2.png').convert()}
        #menu
        self.menu_trigger = True
        self.menu_picture = pygame.image.load('img/bg.jpg').convert()
        self.panel_picture = pygame.image.load('img/panel.png').convert_alpha()
        self.shop_picture = pygame.image.load('img/shop.png').convert_alpha()

        #Face
        self.center_norm = pygame.image.load('img/avatar/center_norm.png').convert_alpha()
        self.left_norm = pygame.image.load('img/avatar/left_norm.png').convert_alpha()
        self.rigth_norm = pygame.image.load('img/avatar/right_norm.png').convert_alpha()

        #icons
        self.Catr_On = pygame.image.load('img/icons/Catr_On.png').convert_alpha()
        self.Catr_Off = pygame.image.load('img/icons/Catr_Off.png').convert_alpha()

        self.Las_On = pygame.image.load('img/icons/Las_On.png').convert_alpha()
        self.Las_Off = pygame.image.load('img/icons/Las_Off.png').convert_alpha()


        #weapon 1
        self.weapon_shot_animation = deque([pygame.image.load(f'sprites/weapon/shot/{i}.png').convert_alpha() for i in
                                            range(20)])  # Делаем анимацию  оружия
        self.weapon_base_sprite = pygame.image.load('sprites/weapon/base/0.png').convert_alpha()  # Рисуем оружие
        self.weapon_rect = self.weapon_base_sprite.get_rect()  # Также рисуем квадрат для удобного определения позиции
        self.weapon_pos = (HALF_WIDTH - self.weapon_rect.width // 2, HEIGHT - self.weapon_rect.height)  # позиция квадрата
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_speed = 4
        self.shot_animation_count = 3
        self.shot_animation_trigger = True
        #weapon 2
        self.weapon_shot_animation2 = deque([pygame.image.load(f'sprites/weapon2/anim/{i}.png').convert_alpha() for i in range(4)])
        self.weapon_base_sprite2 = pygame.image.load('sprites/weapon2/base/0.png').convert_alpha()
        self.weapon_rect2 = self.weapon_base_sprite2.get_rect()
        self.weapon_pos2 = (HALF_WIDTH - self.weapon_rect2.width // 2, HEIGHT - self.weapon_rect2.height - 50)
        self.shot_length2 = len(self.weapon_shot_animation2)
        self.shot_length_count2 = 0
        self.shot_animation_speed2 =35
        self.shot_animation_count2 = 5
        # weapon 2 Prisel
        self.weapon_shot_animation2_prisel =deque([pygame.image.load(f'sprites/weapon2/base/prisel/anim/{i}.png').convert_alpha() for i in range(4)])
        self.weapon_base_sprite2_prisel = pygame.image.load('sprites/weapon2/base/prisel/0.png').convert_alpha()
        self.weapon_rect2_prisel = self.weapon_base_sprite2_prisel.get_rect()
        self.weapon_pos2_prisel = (HALF_WIDTH - self.weapon_rect2_prisel.width // 2, HEIGHT - self.weapon_rect2_prisel.height)
        self.shot_length2_prisel = len(self.weapon_shot_animation2_prisel)
        self.shot_length_count2_prisel = 0
        self.shot_animation_speed2_prisel = 4
        self.shot_animation_count2_prisel = 3




        self.shot_sound = pygame.mixer.Sound('sound/shotgun.wav')  #Загружаем звук выстрела
        #sfx parameters
        self.sfx = deque([pygame.image.load(f'sprites/weapon/sfx/{i}.png').convert_alpha() for i in range(9)])#Разрыв пули анимация
        self.sfx_length_count = 3
        self.sfx_length = len(self.sfx)
        #sfx 2
        self.sfx2 = deque([pygame.image.load(f'sprites/weapon2/sfg/{i}.png').convert_alpha() for i in range(2)])
        self.sfx_length_count2 = 1
        self.sfx_length2 = len(self.sfx2)




    #Функция отрисовывает фон игры
    def bacground(self, angle):
        sky_offset = -10 * math.degrees(angle) % WIDTH #вычисляем смещение по текстуре, путем нахождения остатка от деления угла в градусов и ширины
        self.sc.blit(self.textures['s'], (sky_offset, 0)) #рисуем участок неба в зависимости от смещения
        self.sc.blit(self.textures['s'], (sky_offset - WIDTH, 0))
        self.sc.blit(self.textures['s'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.sc, LEATHER, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    #Отрисовка главной проекции экрана
    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True): # сортируем стены и спрайты по глубине.Начинаем отрисовку с дальних объектов
            # Реализуем в свое время алгоритм Z-буфера
            # 1 Отсекаем ложные значения для спрайтов
            # 2 Распоковываем кортеж - упорядоченный последовательный элемент типа данных
            # 3 Наносим объекты на главную поверхность
            if obj[0]:
                _, object, object_pos = obj
            self.sc.blit(object, object_pos)


    def fps(self, clock): #Например FPS
        display_fps = str((int) (clock.get_fps())) #получаем информацию о количестве кадров в сек
        render = self.font.render(display_fps, 0, DARKORANGE) #определяем цвет и размещаем его в
        self.sc.blit(render,FPS_POS) #правом верхнем углу нашего окна

    #функция отрисовывает мини карту
    def mini_map(self, player):
        mini_map = Level.mini_map()
        self.sc_map.fill(BLACK) #мини карту делаем черной
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE # позиции игрока на карте (уменьшая его в столько то раз (5))
        #Рисуем мини карту
        pygame.draw.line(self.sc_map, YELLOW, (map_x, map_y), (map_x + 12 * math.cos(player.angle),
                                                map_y + 12 * math.sin(player.angle)), 2) #рисуем желтые линии на карте(как взгляд игрока)
        pygame.draw.circle(self.sc_map, RED, (int(map_x), int(map_y)), 5) #рисуе круг, как игрока на мини карте и разукаршиваем его в красный

        for x, y in mini_map: #делаем цикл, чтобы всю черную карту окружить темно коричневым цветом(или другим)
            pygame.draw.rect(self.sc_map, DARKBROWN, (x, y, MAP_TILE, MAP_TILE))
        self.sc.blit(self.sc_map, MAP_POS)

    def player_weapon(self, shots):
        if self.player.shot and Setting.ArmsShotgun1 > 0:  #Если человек нажал левую кнопку мыши, то сработает условие
            self.shot_projection = min(shots)[1] // 2 #определяем кто к нам находится ближе(стена или спрайт)
            self.bullet_sfx()
            shot_sprite = self.weapon_shot_animation[0]
            self.sc.blit(shot_sprite, self.weapon_pos)  #В зависимости от параметра нажатой клавиши
            self.shot_animation_count += 1  #будем проигрывать спрайты с установочной анимации
            if not self.shot_length_count and Setting.sound_cout_shotgun == 1:  # Звук будет производится в момент старта выстрела
                self.shot_sound.play()
                Setting.sound_cout_shotgun = 0
            if self.shot_animation_count == self.shot_animation_speed:  #Также, только другим методом
                self.weapon_shot_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_length_count += 1
                self.shot_animation_trigger = False
                Setting.sound_cout_shotgun = 1
            if self.shot_length_count == self.shot_length:  #Когда все анимационные спрайты закончатся
                Setting.ArmsShotgun1 -= 1
                self.player.shot = False  #Отключаем атрибут выстрела
                self.shot_length_count = 0
                self.sfx_length_count = 0
                self.shot_animation_trigger = True
        else:
             self.sc.blit(self.weapon_base_sprite, self.weapon_pos) #В конце анимации атрисовываем только базовую картинку

    def player_weapon2(self, shots):
        if self.player.shot and Setting.ArmsShotgun2 > 0:  #Если человек нажал левую кнопку мыши, то сработает условие
            self.shot_projection = min(shots)[1] // 2 #определяем кто к нам находится ближе(стена или спрайт)
            self.bullet_sfx2()
            shot_sprite = self.weapon_shot_animation2[0]
            self.sc.blit(shot_sprite, self.weapon_pos2)  #В зависимости от параметра нажатой клавиши
            self.shot_animation_count2 += 1  #будем проигрывать спрайты с установочной анимации
            if not self.shot_length_count2 and Setting.sound_cout_сannonLaser == 1:  # Звук будет производится в момент старта выстрела
                self.shot_sound.play()
                Setting.sound_cout_сannonLaser = 0
            if self.shot_animation_count2 == self.shot_animation_speed2:  #Также, только другим методом
                self.weapon_shot_animation2.rotate(-1)
                self.shot_animation_count2 = 0
                self.shot_length_count2 += 1
                self.shot_animation_trigger = False
                Setting.sound_cout_сannonLaser = 1
            if self.shot_length_count2 == self.shot_length2:  #Когда все анимационные спрайты закончатся
                Setting.ArmsShotgun2 -= 1
                self.player.shot = False  #Отключаем атрибут выстрела
                self.shot_length_count2 = 0
                self.sfx_length_count2 = 0
                self.shot_animation_trigger = True
        elif Setting.wep == 2.0:
             self.sc.blit(self.weapon_base_sprite2, self.weapon_pos2)
        elif Setting.wep == 2.5 and Setting.ArmsShotgun2 > 0:
             if self.player.shot:
                 self.shot_projection = min(shots)[1] // 2  # определяем кто к нам находится ближе(стена или спрайт)
                 self.bullet_sfx2()
                 shot_sprite = self.weapon_shot_animation2_prisel[0]
                 self.sc.blit(shot_sprite, self.weapon_pos2)  # В зависимости от параметра нажатой клавиши
                 self.shot_animation_count2_prisel += 1  # будем проигрывать спрайты с установочной анимации
                 if self.shot_animation_count2_prisel == self.shot_animation_speed2:  # Также, только другим методом
                     self.weapon_shot_animation2_prisel.rotate(-1)
                     self.shot_animation_count2_prisel = 0
                     self.shot_length_count2_prisel += 1
                     self.shot_animation_trigger = False
                 if self.shot_length_count2_prisel == self.shot_length2_prisel:  # Когда все анимационные спрайты закончатся
                     self.player.shot = False  # Отключаем атрибут выстрела
                     self.shot_length_count2_prisel = 0
                     self.sfx_length_count2 = 0
                     self.shot_animation_trigger = True
             else:
                 self.sc.blit(self.weapon_base_sprite2_prisel, self.weapon_pos2_prisel)


    def bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length: #если количество пули меньше чем длина анимации
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.sc.blit(sfx, (HALF_WIDTH - sfx_rect.w // 2, HALF_HEIGHT - sfx_rect.h // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)

    def bullet_sfx2(self):
        if self.sfx_length_count2 < self.sfx_length2:
            sfx2 = pygame.transform.scale(self.sfx2[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx2.get_rect()
            self.sc.blit(sfx2, (HALF_WIDTH - sfx_rect.w // 2, HALF_HEIGHT - sfx_rect.h // 2))
            self.sfx_length_count2 += 0.5
            self.sfx2.rotate(-1)


    def basic_health(self):
        #hp monsters
        bs = pygame.Surface((170,50)) #создаем прямоугольник
        bs.set_alpha(155) #делаем его полупрозрачным
        bs.fill((0,255,255)) #разукрашиваем его
        text = pygame.font.Font('font/font.ttf',24).render(Setting.Name, 1, BLACK) #берем формат и создаем текст
        pygame.draw.rect(self.sc, (255, 0, 0), (650,10, Setting.cur / Setting.hp_rat, 25), ) #создаем школу здоровья для монстров
        pygame.draw.rect(self.sc, (255, 255, 255), (650, 10, Setting.bar_lenght, 25), 4)
        self.sc.blit(bs,(850,40))  #рисуем прямоугольник на таких то координатах
        self.sc.blit(text, (880, 40)) #рисуем текст на координатах
        #score
        score = pygame.font.Font('font/font.ttf', 24).render('Score: '+str(Setting.score), 1, DARKORANGE)
        self.sc.blit(score, (5, 5))
        #Stamina
        pygame.draw.rect(self.sc, (255, 165, 0), (5, 50, Setting.stamina, 25), )  # создаем школу здоровья для монстров
        pygame.draw.rect(self.sc, (255, 255, 255), (5, 50, Setting.max_stamine, 25), 4)


    def panel(self):
        height = 80
        width = 1200
        panel = pygame.transform.scale(self.panel_picture, (width,height))
        self.sc.blit(panel, (0,HEIGHT - 80))
        #hp
        text1 = pygame.font.Font('font/font.ttf', 45).render(str(Setting.hil), 1, RED)
        text1_hp = pygame.font.Font('font/font.ttf', 25).render('HP', 1, GREEN)
        self.sc.blit(text1, (45, HEIGHT - 95))
        self.sc.blit(text1_hp, (75, HEIGHT - 40))
        #avatar
        if Setting.face == 0:
            self.center = pygame.transform.scale(self.center_norm, (80,90))
            self.sc.blit(self.center, (525, HEIGHT - 85))
        if Setting.face == 1:
            self.left = pygame.transform.scale(self.left_norm, (80, 90))
            self.sc.blit(self.left, (525, HEIGHT - 85))
        if Setting.face == 2:
            self.rigth = pygame.transform.scale(self.rigth_norm, (80, 90))
            self.sc.blit(self.rigth, (525, HEIGHT - 85))

        #Weapon
        w = 35
        h = 35
        textArms = pygame.font.Font('font/font.ttf', 25).render('ARMS', 1, DARKORANGE)
        self.sc.blit(textArms, (685, HEIGHT - 40))
        if Setting.wep == 1:
            self.On =  pygame.transform.scale(self.Catr_On, (w,h))
            self.sc.blit(self.On, (230, HEIGHT - 75))

            textArms1 = pygame.font.Font('font/font.ttf', 35).render(str(Setting.ArmsShotgun1)+' / '+ str(Setting.ArmsShotgun1Max), 1, (184, 134, 11))
            self.sc.blit(textArms1, (650, HEIGHT - 90))
            self.Off = pygame.transform.scale(self.Las_Off, (w,h))
            self.sc.blit(self.Off, (270, HEIGHT - 75))


        if Setting.wep == 2 or Setting.wep == 2.5:
            self.Off = pygame.transform.scale(self.Catr_Off, (w,h))
            self.sc.blit(self.Off, (230, HEIGHT - 75))

            self.On = pygame.transform.scale(self.Las_On, (w,h))
            self.sc.blit(self.On, (270, HEIGHT - 75))
            textArms2 = pygame.font.Font('font/font.ttf', 35).render(str(Setting.ArmsShotgun2) + ' / ' + str(Setting.ArmsShotgun2Max), 1, (184, 134, 11))
            self.sc.blit(textArms2, (650, HEIGHT - 90))





    def Lose(self):
        pygame.mixer.music.stop()
        render = self.font_win.render('YOU LOSE!!!',1, (randrange(40,120),0,0))  #Это будет черный прямоугольник с меняющимися цветами и с поздравлением
        rect = pygame.Rect(0,0,1000,300)
        rect.center =  HALF_WIDTH, HALF_HEIGHT
        pygame.draw.rect(self.sc, BLACK, rect, border_radius=50)  #Рисуем
        self.sc.blit(render, (rect.centerx - 450, rect.centery - 140))
        pygame.display.flip()
        self.clock.tick(15)


    def win(self):
        render = self.font_win.render('YOU WIN!!!',1, (randrange(40,120),0,0))  #Это будет черный прямоугольник с меняющимися цветами и с поздравлением
        rect = pygame.Rect(0,0,1000,300)
        rect.center =  HALF_WIDTH, HALF_HEIGHT
        pygame.draw.rect(self.sc, BLACK, rect, border_radius=50)  #Рисуем
        self.sc.blit(render, (rect.centerx - 430, rect.centery - 140))
        pygame.display.flip()
        self.clock.tick(15)

    def menu(self): #Делаем меню
        x = 0
        pygame.mouse.set_visible(True)
        #Делаем шрифты
        button_font = pygame.font.Font('font/font.ttf',72)
        label_font = pygame.font.Font('font/font1.otf',400)
        #Создаем надпись и кнопки
        start = button_font.render('START',1,pygame.Color('lightgray'))
        button_start = pygame.Rect(0,0,400,150)
        button_start.center = HALF_WIDTH, HALF_HEIGHT

        exit = button_font.render('EXIT', 1,pygame.Color('lightgray'))
        button_exit = pygame.Rect(0,0,400,150)
        button_exit.center = HALF_WIDTH, HALF_HEIGHT+200

        self.menu_trigger = True

        #При нажатие выход все выключается
        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #Добавляем картинку
            self.sc.blit(self.menu_picture, (0,0), (x % WIDTH, HALF_HEIGHT, WIDTH, HEIGHT))
            x+=1
            #Добавляем кнопки
            pygame.draw.rect(self.sc, BLACK, button_start, border_radius=25, width=10)
            self.sc.blit(start, (button_start.centerx - 130, button_start.centery - 70))

            pygame.draw.rect(self.sc, BLACK, button_exit, border_radius=25, width=10)
            self.sc.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
            #Делаем название игры
            color = randrange(40)
            label = label_font.render('RUNNIN',1,(color,color,color))
            self.sc.blit(label,(15,-30))

            #Получаем позицию мышки и проверяем нажатие на кнопки
            mouse_pos = pygame.mouse.get_pos() #Получаем координаты мыши и состояние нажатых клавиш
            mouse_clicl = pygame.mouse.get_pressed() #Есил мы нажимаем на мышку
            if button_start.collidepoint(mouse_pos): #Во первых кнопка будет полностью закрашена
                pygame.draw.rect(self.sc, BLACK, button_start, border_radius=25)
                self.sc.blit(start, (button_start.centerx - 130, button_start.centery - 70))
                if mouse_clicl[0]: #Во вторых мы перемещаемся по назначению
                    self.menu_trigger = False
                    Setting.Condition = 0
                    if Setting.Name_Count > 0:
                        name = pyautogui.prompt('Введите свое имя:', 'Настройки')
                        if name == None or name == '':
                           Setting.Name_player = 'Anonim'
                        else:
                            Setting.Name_player = name
                        Setting.Name_Count = 0
                    pygame.mouse.set_visible(False)
            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.sc, BLACK, button_exit, border_radius=25 )
                self.sc.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
                if mouse_clicl[0]:  # Во вторых мы перемещаемся по назначению
                    pygame.quit()
                    sys.exit()
            #Делаем чтобы установить количество кадров в секунду
            pygame.display.flip()
            self.clock.tick(20)

    def shop(self):  # Делаем магазин

        width = 195
        height = 65
        pygame.mouse.set_visible(True)
        #dir
        conditions = pygame.Surface((WIDTH/2 - 10, HEIGHT - height - 20))
        conditions.set_alpha(50)
        conditions.fill(BLACK)

        directory_conditions = pygame.Surface((WIDTH/2 - 10, HEIGHT - height - 20))
        directory_conditions.set_alpha(50)
        directory_conditions.fill(BLACK)
        #создание кнопок и текста
        textBack = pygame.font.Font('font/font.ttf', 20).render('Назад', 1, pygame.Color('BLACK'))
        textBackKey = pygame.font.Font('font/font.ttf', 20).render('E', 1, pygame.Color('BLACK'))

        button_Back_Off = pygame.image.load('img/button/button_Off.png')
        button_Back_Off_transform = pygame.transform.scale(button_Back_Off, (width,height))

        button_Back_On = pygame.image.load('img/button/button_On.png')
        button_Back_On_transform = pygame.transform.scale(button_Back_On, (width, height))

        buttonBack = pygame.Rect( WIDTH - width,HEIGHT-height, width,height) #создание мышко основы кнопки
        # -------------------------------------------------------------------------------------------------
        button_dir_Condotion_Off = pygame.image.load('img/button/button_directory_conditions_Off.png')
        button_dir_Condotion_Off_transform = pygame.transform.scale(button_dir_Condotion_Off, (width-15, height-15))

        button_dir_Condotion_Off_sek = pygame.image.load('img/button/button_directory_conditions_Off_sek.png')
        button_dir_Condotion_Off_sek_transform = pygame.transform.scale(button_dir_Condotion_Off_sek, (width-15, height-15))

        button_dir_Condotion_On = pygame.image.load('img/button/button_directory_conditions_On.png')
        button_dir_Condotion_On_transform = pygame.transform.scale(button_dir_Condotion_On, (width-15, height-15))

        buttonDirCon_Power= pygame.Rect(WIDTH/2+3, 0, width -15, height -15)
        buttonDirCon_Shop = pygame.Rect(WIDTH / 2 + 3 + (width), 0, width -15, height -15)
        buttonDirCon_Donate = pygame.Rect(WIDTH / 2 + (width + 3 + width), 0, width -15, height -15)
        #-------------------------------------------------------------------------------------------------
        button_power_Off = pygame.image.load('img/button/button_power_off.png')
        button_power_Off_transform = pygame.transform.scale(button_power_Off, (width, height))
        button_power_On = pygame.image.load('img/button/button_power_on.png')
        button_power_On_transform = pygame.transform.scale(button_power_On, (width, height))
        buttonPowerHP = pygame.Rect(WIDTH / 2 + 3, height + 10, width, height)

        #rang
        button_rang_off = pygame.image.load('img/button/button_rang_off.png')
        button_rang_off_transform = pygame.transform.scale(button_rang_off, (width,height))
        button_rang_on = pygame.image.load('img/button/button_rang_on.png')
        button_rang_on_transform = pygame.transform.scale(button_rang_on, (width, height))

        #rang avatar
        wid = WIDTH / 2 - width
        heig = HEIGHT // 1.7 + 40
        people0 = pygame.image.load('img/avatar/people0.png')
        people0_transform = pygame.transform.scale(people0, (wid,heig))
        people1 = pygame.image.load('img/avatar/people1.png')
        people1_transform = pygame.transform.scale(people1, (wid, heig))
        people2 = pygame.image.load('img/avatar/people2.png')
        people2_transform = pygame.transform.scale(people2, (wid, heig))
        people3 = pygame.image.load('img/avatar/people3.png')
        people3_transform = pygame.transform.scale(people3, (wid, heig))
        people4 = pygame.image.load('img/avatar/people4.png')
        people4_transform = pygame.transform.scale(people4, (wid, heig))
        people5 = pygame.image.load('img/avatar/people5.png')
        people5_transform = pygame.transform.scale(people5, (wid, heig))
        people6 = pygame.image.load('img/avatar/people6.png')
        people6_transform = pygame.transform.scale(people6, (wid, heig))
        people7 = pygame.image.load('img/avatar/people7.png')
        people7_transform = pygame.transform.scale(people7, (wid, heig))
        people8 = pygame.image.load('img/avatar/people8.png')
        people8_transform = pygame.transform.scale(people8, (wid, heig))
        people9 = pygame.image.load('img/avatar/people9.png')
        people9_transform = pygame.transform.scale(people9, (wid, heig))

        buttonRang = pygame.Rect(WIDTH / 6 , HEIGHT - height*3, width,height)
        while Setting.Condition == 1 or Setting.Condition == 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        Setting.Condition = 0
                        pygame.mouse.set_visible(False)
                    if Setting.direct[0] == 1 and Setting.talent_points > 0:
                        if event.key == pygame.K_1 and Setting.direct[0] == 1:
                            Setting.talent_points -= 1
                            Setting.Damage_Rais += 2
                            Setting.Condition = 0
                            Setting.Condition_Update = 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    try:
                     if Setting.direct[0] == 1 and Setting.talent_points > 0 and buttonPowerHP.collidepoint(mouse_pos):
                         if event.button == 1:
                            Setting.Damage_Rais += 2
                            Setting.talent_points -= 1
                            Setting.Condition = 0
                            Setting.Condition_Update = 1
                     if event.button == 1:
                         if buttonRang.collidepoint(mouse_pos) and Setting.rang_player_count > 0:
                             Setting.rang_player += 1
                             Setting.rang_player_count -= 1
                    except:
                        continue

            self.sc.blit(self.shop_picture, (0, 0), (HALF_WIDTH, HALF_HEIGHT - 250, WIDTH, HEIGHT))

            self.sc.blit(button_Back_Off_transform, (WIDTH - width, HEIGHT - height))
            self.sc.blit(textBack, (WIDTH - width + 75, HEIGHT - height + 12))
            self.sc.blit(textBackKey, (WIDTH - width + 20, HEIGHT - height + 12))

            text_rang = pygame.font.Font('font/font.ttf',20).render('Ранг', 1, BLACK)
            text_rang_count = pygame.font.Font('font/font.ttf', 30).render(str(Setting.rang_player), 1, BLACK)
            self.sc.blit(button_rang_off_transform, (WIDTH / 6 , HEIGHT - height*3))

            #dir
            self.sc.blit(conditions, (10, 20))
            self.sc.blit(directory_conditions, (WIDTH / 2 + 5, 20))

            self.sc.blit(button_dir_Condotion_Off_transform, (WIDTH / 2 + 3, 0))
            text_power = pygame.font.Font('font/font.ttf',20).render('Мощь', 1, BLACK)
            self.sc.blit(button_dir_Condotion_Off_transform, (WIDTH / 2 + 3 + (width), 0))
            text_shop = pygame.font.Font('font/font.ttf', 20).render('Магазин', 1, BLACK)
            self.sc.blit(button_dir_Condotion_Off_transform, (WIDTH / 2 + (width + 3 + width), 0))
            text_donate = pygame.font.Font('font/font.ttf', 20).render('Донат', 1, BLACK)


            #field mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicl = pygame.mouse.get_pressed()
            if buttonBack.collidepoint(mouse_pos):
                self.sc.blit(button_Back_On_transform, (WIDTH - width, HEIGHT - height))
                if mouse_clicl[0]:
                    Setting.Condition = 0
                    pygame.mouse.set_visible(False)
                    Setting.shop = False
                    Setting.direct = [0,0,0]
            elif buttonDirCon_Power.collidepoint(mouse_pos):
                self.sc.blit(button_dir_Condotion_Off_sek_transform, (WIDTH/2 + 3, 0))
                if mouse_clicl[0]:
                    Setting.direct = [1, 0, 0]
            elif buttonDirCon_Shop.collidepoint(mouse_pos):
                self.sc.blit(button_dir_Condotion_Off_sek_transform, (WIDTH / 2 + (width + 3), 0))
                if mouse_clicl[0]:
                   Setting.direct = [0, 1, 0]
            elif buttonDirCon_Donate.collidepoint(mouse_pos):
                self.sc.blit(button_dir_Condotion_Off_sek_transform, (WIDTH / 2 + (width + 3 + width),0))
                if mouse_clicl[0]:
                    Setting.direct = [0, 0, 1]
            elif buttonRang.collidepoint(mouse_pos):
                self.sc.blit(button_rang_on_transform, (WIDTH / 6 , HEIGHT - height*3))


            #Directory Function


            if Setting.direct[0] == 1:
                self.sc.blit(button_dir_Condotion_On_transform, (WIDTH / 2 + 3, 0))
                self.sc.blit(button_power_Off_transform, (WIDTH / 2 + 3, height + 10))
                text_Damage = pygame.font.Font('font/font.ttf', 18).render('Урон', 1, BLACK)
                text_Damage_raising = pygame.font.Font('font/font.ttf', 15).render(str(Setting.Damage_Rais) + '(+'+str(Setting.Damage_Step)+')', 1, RED)
                text_DamageKey = pygame.font.Font('font/font.ttf', 20).render('1', 1, BLACK)
                if buttonPowerHP.collidepoint(mouse_pos) and Setting.talent_points > 0:
                    self.sc.blit(button_power_On_transform, (WIDTH / 2 + 3, height + 10))

                self.sc.blit(text_Damage, (WIDTH / 2 + (width / 2 - 5), height + 15))
                self.sc.blit(text_Damage_raising, (WIDTH / 2 + (width / 2 - 10), height + 40))
                self.sc.blit(text_DamageKey, (WIDTH / 2 + 30, height + 25))
            elif Setting.direct[1] == 1:
                self.sc.blit(button_dir_Condotion_On_transform, (WIDTH / 2 + 3 + width, 0))
            elif Setting.direct[2] == 1:
                self.sc.blit(button_dir_Condotion_On_transform, (WIDTH / 2 + (width + 3 + width), 0))


            self.sc.blit(textBack, (WIDTH - width + 75, HEIGHT - height + 12))
            self.sc.blit(textBackKey, (WIDTH - width + 20, HEIGHT - height + 12))
            #directory power
            self.sc.blit(text_power, (WIDTH / 2 + width / 3, height / 10))



            #rang update
            self.sc.blit(text_rang, (WIDTH / 6   + width / 2  + 5 , HEIGHT - height*3 + 18))
            self.sc.blit(text_rang_count, (WIDTH / 6  + width / 4 - 5, HEIGHT - height * 3))
            if Setting.rang_player == 0:
               self.sc.blit(people0_transform, (width, height + 30))
            elif Setting.rang_player == 1:
                self.sc.blit(people1_transform, (width, height + 30))
            elif Setting.rang_player == 2:
                self.sc.blit(people2_transform, (width, height + 30))
            elif Setting.rang_player == 3:
                self.sc.blit(people3_transform, (width, height + 30))
            elif Setting.rang_player == 4:
                self.sc.blit(people4_transform, (width, height + 30))
            elif Setting.rang_player == 5:
                self.sc.blit(people5_transform, (width, height + 30))
            elif Setting.rang_player == 6:
                self.sc.blit(people6_transform, (width, height + 30))
            elif Setting.rang_player == 7:
                self.sc.blit(people7_transform, (width, height + 30))
            elif Setting.rang_player == 8:
                self.sc.blit(people8_transform, (width, height + 30))
            elif Setting.rang_player == 9:
                self.sc.blit(people9_transform, (width, height + 30))

            #Характеристики
            text_HP = pygame.font.Font('font/font.ttf', 30).render('HP: ' + str(Setting.hil), 1, RED)
            self.sc.blit(text_HP, (20, HEIGHT / 8))
            text_DMG = pygame.font.Font('font/font.ttf', 30).render('DMG: ' + str(Setting.damage), 1, RED)
            self.sc.blit(text_DMG, (20, HEIGHT / 6))

            self.sc.blit(text_shop, ((WIDTH / 2 + width + 60) , height / 10))
            self.sc.blit(text_donate, (WIDTH / 2 + (width + width + 60), height / 10))

            # Name Player
            col = randrange(120, 160)
            text_Name_Player = pygame.font.Font('font/font.ttf', 60).render(Setting.Name_player, 1, (col, 0,0))
            self.sc.blit(text_Name_Player, (width - 20, height / 6 - 10))

            #elif buttonPower.collidepoint(mouse_pos):
            #self.sc.blit(button_power_On_transform, (width, height))

            pygame.display.flip()
            self.clock.tick(20)

