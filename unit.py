from random import randint, randrange
import settings

# 各キャラクターのオブジェクトのクラス  
class Ship:   
 def __init__(self):
    self.ship_x = 80
    self.ship_y = 105
    self.ship_hp = settings.P_SHIP_MAX_HP
    self.ship_st = settings.P_SHIP_MAX_ST

 # 移動制御 
 def update(self, x, y):
    self.ship_x = x # 横軸
    self.ship_y = y # 縦軸
     
class Shot:
 def __init__(self):
    self.pos_x = 0
    self.pos_y = 0
    self.exists = True
 def update(self, x, y):
    self.pos_x = x
    self.pos_y = y
 def shot_del(self):
    self.exists = False

class Slash:
 def __init__(self):
    self.pos_x = 0
    self.pos_y = 0
    self.exists = True
 def update(self, x, y):
    self.pos_x = x
    self.pos_y = y
 def slash_del(self):
    self.exists = False

class Enemy:
 """
 引数のバリエーション数値で生成する敵を決定
 """
 def __init__(self, v):
    self.ene_x = 0
    self.ene_y = 8
    self.motion = 0
    self.ene_c = randint(0, 2)
    self.variation = v
    self.ene_h = 4
 def update(self, x, y):
    self.ene_x = x  
    self.ene_y = y
 def ene_del(self):
    self.exists = False
    
class Enemy2:
 def __init__(self, v):
    self.ene_x = randint(20, 125)
    self.ene_y = 8
    self.motion = 0
    self.ene_c = randint(0, 2)
    self.variation = v
 def update(self, x, y):
    self.ene_x = x
    self.ene_y = y

class Enemy3:
 def __init__(self, v):
    self.ene_x = randint(20, 125)
    self.ene_y = 8
    self.motion = 0
    self.ene_c = randint(0, 2)
    self.variation = v
 def update(self, x, y):
    self.ene_x = x
    self.ene_y = y

class Bomb:
 def __init__(self, x, y):
    self.bomb_x = x
    self.bomb_y = y
    self.bomb_t = 0       
    
class Boss:
 def __init__(self):
    self.boss_x = 0
    self.boss_y = 0
    self.boss_h = 0 # hp 
    self.boss_m = 0
 def update(self, x, y, hp):
    self.boss_x = x
    self.boss_y = y  
    self.boss_h = hp        
 def move(self, x, y):
    self.boss_x = x
    self.boss_y = y  