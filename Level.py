import pygame

import sprite_object
from sprite_object import *
import map1
import map2
import player
from map1 import *
from map2 import *

def world_map():
    world_map = map1.world_map
    if (Setting.levelUp == 2):
        world_map = map2.world_map
    return world_map

def WORDLD_WIDTH():
    WORLD_WIDTH = map1.WORLD_WIDTH
    if (Setting.levelUp == 2):
        WORLD_WIDTH = map2.WORLD_WIDTH
    return WORLD_WIDTH

def WORDLD_HEIGHT():
    WORLD_HEIGHT = map1.WORLD_HEIGHT
    if (Setting.levelUp == 2):
        WORLD_HEIGHT = map2.WORLD_HEIGHT
    return WORLD_HEIGHT


def mini_map():
    mini_map = map1.mini_map
    if (Setting.levelUp == 2):
        mini_map = map2.mini_map
    return mini_map

def collision_walls():
    collision_walls = map1.collision_walls
    if (Setting.levelUp == 2):
        collision_walls = map2.collision_walls
    return collision_walls






