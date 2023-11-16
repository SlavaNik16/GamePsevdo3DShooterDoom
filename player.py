import Level
import Setting
import drawing
import interaction
import map1
import sprite_object
from Setting import * #Импортируем все, что находится в классе Setting
import pygame #Импортируем нашу библиотеку
import math



class Player:
    def __init__(self, sprites):
        self.One = True
        self.x, self.y = player_pos #Координаты игрока
        self.angle = player_angle #Кординаты взгляда
        self.sprites = sprites
        self.sensitivity = 0.004 #Чувствительность мыши
        #collision parameters
        self.side = 50 #сторона квадрата, как игрок
        self.rect = pygame.Rect(*player_pos, self.side, self.side) #делаем невидимый квадрат у вокруг игрока

        #weapon
        self.shot = False

        self.previous_time = pygame.time.get_ticks() # начало времени выстрела дробовика


    @property     # Добавляем свойство
    def pos(self):
        return (self.x, self.y) #Возвращает позицию игрока (его x и y)

    @property
    def collision_list(self):  #Объединяем в этой функции список стен со списком спрайтов
        collision_walls = Level.collision_walls()

        if Setting.levelUp == 1 and Setting.one == 1:
            Setting.list_object = self.sprites.list_of_objects
            Setting.one = 2
        elif (Setting.levelUp == 2 and Setting.one == 2):
            interaction.Interaction.clear_world_Up
            Setting.one = 3
            Setting.list_object = self.sprites.list_of_objects1

        return  collision_walls + [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  Setting.list_object if obj.blocked]  #Учитываем размер, позиции и параметры блокировки спрайтов

    def defect_collision(self, dx, dy): #функция которая будет принимать передвижение на 1 шаг по обоим осям
        next_rect = self.rect.copy() #Берем копию нашего тикущего положения
        next_rect.move_ip(dx, dy) #Затем переместим на координаты dx и dy
        hit_indexes = next_rect.collidelistall(self.collision_list) #Далее сформулируем индекс стен, с которам
        #столкнулся игрок с помощью меттода collidelistall(проверка на пересечение прямоугольников), так же с спрайтами

        if len(hit_indexes):
            delta_x, delta_y = 0, 0 #Далее будем находить сторону с которой столкнулись
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0: #и в зависимости каким углом мы столкнулись
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10: #мы будем полностью останавливатся
                dx, dy = 0, 0
            elif delta_x > delta_y:
                 dy = 0
            elif delta_y > delta_x:
                 dx = 0
        self.x += dx
        self.y += dy
        #print(self.x, self.y)
        if (Setting.levelUp == 2 and self.One):
            self.x = 500
            self.y = 900
            self.One = False
        elif (Setting.levelUp == 3 and not self.One):
            self.One = True

    # Метод будет отслеживать нажатие клавиш и менять соответствующие  значения атрибутов
    #
    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.rect.center = self.x, self.y #центр квадрата делаем вокруг игрока
        self.angle %= DOUBLE_PI #придется оставлять угол взгляда игрока  в пределах 2 pi



    def keys_control(self):
        sin_a = math.sin(self.angle) #Находим cin угла нашего взгляда
        cos_a = math.cos(self.angle) #Находим cos угла нашего взгляда
        keys = pygame.key.get_pressed() #Обращаемся к клавиатуре(Получаем код клавиш)
        # Если человек нажал на клавиатуре клавишу Escape, то мы выходим
        if keys[pygame.K_ESCAPE]:
           Setting.Condition = 2

        if keys[pygame.K_e]:
            if Setting.shop == False:
                Setting.Condition = 1 #Состояние окна магазина
                Setting.shop = True

        # Если человек нажал на клавиатуре клавишу W, то мы идем направо, но на 3д уровне
        if keys[pygame.K_1]:
           Setting.wep = 1.0

        if keys[pygame.K_2]:
           Setting.wep = 2.0

        if keys[pygame.K_w]:
            dx = Setting.player_speed * cos_a   #Получаем координаты dx и dy (что соответствует правому шагу)
            dy = Setting.player_speed * sin_a
            Setting.face = 0
            self.defect_collision(dx, dy) #Вызывать проверку кнопки будем, как только нажмем на кнопку
        if keys[pygame.K_s]:
            dx = -Setting.player_speed * cos_a
            dy = -Setting.player_speed * sin_a
            Setting.face = 0
            self.defect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = Setting.player_speed * sin_a
            dy = -Setting.player_speed * cos_a
            Setting.face = 1
            self.defect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -Setting.player_speed * sin_a
            dy = Setting.player_speed * cos_a
            Setting.face = 2
            self.defect_collision(dx, dy)
        # Если человек нажал на клавиатуре клавишу Left, то мы меняем зрение влево
        if keys[pygame.K_LEFT]:
             self.angle -= 0.02
        # Если человек нажал на клавиатуре клавишу Right, то мы меняем зрение вправо
        if keys[pygame.K_RIGHT]:
             self.angle += 0.02


        for event in pygame.event.get(): #Проверяем все события на прежмет
            if event.type == pygame.MOUSEBUTTONDOWN:#Выстрел левой кнопкой мыши
                if event.button == 1 and not self.shot:
                   self.current_time = pygame.time.get_ticks()
                   self.shot = True
                   Setting.shot = True
                if event.button == 3 and Setting.wep == 2.5:
                    Setting.wep = 2.0
                elif event.button == 3 and Setting.wep == 2.0:
                    Setting.wep = 2.5
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    Setting.run = True
                    Setting.player_speed = 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    Setting.run = False
                    Setting.player_speed = 1
                if event.key == pygame.K_e:
                    Setting.shop = False

        #Создание выносливости
        if Setting.run:
            Setting.stamina -= 0.3
            if Setting.stamina <= 0:
                Setting.stamina = 0
                Setting.player_speed = 1
        elif Setting.run == False:
            Setting.stamina += 0.2
            if Setting.stamina >= Setting.max_stamine:
                Setting.stamina = Setting.max_stamine

    def mouse_control(self): # Управление мышкой
        if pygame.mouse.get_focused() and Setting.Condition_Update != 1: # Когда курсор мыши будет в окне игры
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH # Мы вычисляем разницу между положением текущей координаты x мыши и центром(середины) экрана
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))# Затем с каждым циклом будем переносить указатель в центр экрана
            self.angle += difference * self.sensitivity # Затем будем прибавлять угол игрока(меняем взгляд) относительно того, какая чувствительность мыши и его разница в движении
