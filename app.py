from random import randint, randrange
import unit
import pyxel as p
import settings

PIC_H = settings.PIC_H
PIC_W = settings.PIC_W

class APP:
 def __init__(self):
    self.game_start = False
    self.game_over = False
    self.game_clear = False
    self.ship_motion_count = 0
    self.boss = unit.Boss()
    # ボスの出現スコア制御
    self.boss_appears = settings.BOSS_ARRIVAL_COUNT
    self.boss_flug = False
    self.boss_count = 1
    self.boss_hp = 50
    self.score = 0
    self.shots = []
    self.slash = []
    self.warning_flg = True
    self.warning_count = 0
    self.atc_flg = False
    self.atc_count = 0
    self.enemys = []
    self.bombs = []
    self.damage_flg = 0
    self.p_ship = unit.Ship()

    p.init(settings.WINDOW_W, settings.WINDOW_H, caption="DRAGON'S HUNT")
    # ドット絵を読み込む
    p.load("assets/img.pyxres")

    p.mouse(False)
    # ゲームを動かす
    p.run(self.update, self.draw)

 def update(self):
    # システムコントロール
    # ボタンに以下の役割を割り当て
    if p.btnp(p.KEY_Q):
        # 終了
        p.quit()
        
    if p.btnp(p.KEY_T):
        # タイトル画面へ
        self.game_start = False
        self.retry()

    if p.btnp(p.KEY_S):
        # ゲームスタート
        self.game_start = True
        self.retry()

    # 自機の更新
    # game_overがfalseであるかぎりship_move()で自機を動かす
    if self.game_over == False:
        self.ship_move()

    # game_clearがfalseならゲームはクリアされていないので、
    # 当たり判定のチェックと敵を動かす関数を呼び出す。
    if self.game_clear == False:
        self.hit_chk()
        self.ene_move()
        self.boss_move()

    # 敵撃破時の爆発の管理
    if len(self.bombs) > 1:
        del self.bombs[0]
    if len(self.bombs) == 1:
        if p.frame_count % 15 == 0:
            del self.bombs[0]

 def retry(self): #リトライ時のリセット関数
    self.game_over = False
    self.game_clear = False
    self.boss_flug = False
    self.boss_count = 1
    self.boss_enemys = []
    self.boss_hp = 50
    self.score = 0
    self.shots = []
    self.slash = []
    self.atc_flg = False
    self.warning_flg = True
    self.warning_count = 0
    self.atc_count = 0
    self.enemys = []
    self.bombs = []
    self.p_ship = unit.Ship()

 def draw(self):
    p.cls(0)
    # フィールド描画
    if self.boss_count == 1:
        #bltm(x, y, tm, u, v, w, h, [colkey])
        p.bltm(0, 9, 0, 0, 16, 23, 17) #洞窟
    if self.boss_count == 2:
        p.bltm(0, 9, 0, 0, 32, 23, 17) #火山
    if self.boss_count == 3:
        p.bltm(0, 9, 0, 0, 48, 23, 17) #氷の洞窟
    if self.boss_count == 4:
        p.bltm(0, 9, 0, 0, 64, 23, 17) #毒沼
    if self.boss_count == 5:
        p.bltm(0, 9, 0, 0, 80, 23, 17) #山脈
    if self.boss_count == 6:
        p.bltm(0, 9, 0, 0, 96, 23, 17) #城

    # 爆発の描写
    for i in self.bombs:
        if i.bomb_t < 15:
            p.blt(i.bomb_x, i.bomb_y, 0, 112, 0, -PIC_W, PIC_H, 6)

    # ヘッダーの描写
    p.text(1, 2, "SCORE:" + str(self.score), 5)
    p.text(48, 2, "HP:" + str(self.p_ship.ship_hp), 12)
    p.text(74, 2, "ST:" + str(self.p_ship.ship_st), 11)
    p.text(155, 2, "STAGE:" + str(self.boss_count), 9)

    if self.boss_flug == True:
        p.text(121, 2, "BOSS:" + str(self.boss.boss_h), 8)
        if self.warning_flg == True:
            # ボス出現時の表示
            p.text(55, 50, "!! W A R N I N G !!", p.frame_count % 16)
            self.warning_count = self.warning_count + 1
            if self.warning_count > 50:
                self.warning_flg = False

    # 自機の描画
    if self.game_over == False:

        # ダメージを受けた時の自機の描画
        if self.damage_flg == 1:
            p.blt(self.p_ship.ship_x, self.p_ship.ship_y, 0, 80, 16, -PIC_W, PIC_H, 6)
            self.damage_flg = 0

        else:
            # モーション処理
            # 連続で画像を切り替えて動いているようにみせる
            if self.ship_motion_count == 0:
                p.blt(self.p_ship.ship_x, self.p_ship.ship_y, 0, 96, 0, -PIC_W, PIC_H, 6)
                if p.frame_count % 5 == 0:
                    self.ship_motion_count = 1
            
            elif self.ship_motion_count == 1:
                p.blt(self.p_ship.ship_x, self.p_ship. ship_y, 0, 96, 16,-PIC_W, PIC_H, 6)
                if p.frame_count % 5 == 0:
                    self.ship_motion_count = 2
            
            elif self.ship_motion_count == 2:
                p.blt(self.p_ship.ship_x, self.p_ship.ship_y, 0, 96, 32, -PIC_W, PIC_H, 6)
                if p.frame_count % 5 == 0:
                    self.ship_motion_count = 0

    else:
        # やられた時
        p.blt(self.p_ship.ship_x, self.p_ship.ship_y, 0, 128, 0, -PIC_W, PIC_H, 6)

    # 弾の描画
    for i in self.shots:
        if i.exists == True:
            p.blt(i.pos_x, i.pos_y - 10, 0, 144, 0, PIC_W, PIC_H, 6)

    # 近接攻撃の描画
    if self.atc_flg == True:
        p.blt(self.p_ship.ship_x -16, self.p_ship.ship_y - 12, 0, 160, 0, 48, 16, 6)
        self.atc_count = self.atc_count + 1
        # 斬撃は5フレーム経ったら消す
        if self.atc_count > 5:
            self.atc_count = 0
            self.slash = []
            self.atc_flg = False

    # ボスの描画
    if self.boss_flug == True:
        # blt(x, y, img, u, v, w, h, [colkey])
        if self.boss_count == 1:
            p.blt(self.boss.boss_x, self.boss.boss_y, 0, 0, 16, 48, 16, 6)
        if self.boss_count == 2:
            p.blt(self.boss.boss_x, self.boss.boss_y, 0, 0, 48, 48, 16, 6)
        if self.boss_count == 3:
            p.blt(self.boss.boss_x, self.boss.boss_y, 0, 0, 80, 48, 16, 6)
        if self.boss_count == 4:
            p.blt(self.boss.boss_x, self.boss.boss_y, 0, 0, 128, 48, 24, 6)
        if self.boss_count == 5:
            p.blt(self.boss.boss_x, self.boss.boss_y, 0, 64, 112, 48, 16, 6)
        if self.boss_count == 6:
            p.blt(self.boss.boss_x, self.boss.boss_y, 0, 64, 80, 48, 32, 6)
        
    # 敵の描画とボスの攻撃
    for i in self.enemys:
        if self.boss_flug == False:
            # 雑魚敵の生成
            if self.boss_count == 1:
                if i.motion == 0:
                    # 緑ドラゴン
                    p.blt(i.ene_x, i.ene_y, 0, 0, 0, -PIC_W, PIC_H, 6)
                else:
                    # 敵をアニメーションさせるために分岐
                    p.blt(i.ene_x, i.ene_y, 0, 16, 0, -PIC_W, PIC_H, 6)

            if self.boss_count == 2:
                if i.motion == 0:
                    # 赤ドラゴン
                    p.blt(i.ene_x, i.ene_y, 0, 0, 32, -PIC_W, PIC_H, 6)
                else:
                    p.blt(i.ene_x, i.ene_y, 0, 16, 32, -PIC_W, PIC_H, 6)

            if self.boss_count == 3:
                if i.motion == 0:
                    # 青ドラゴン
                    p.blt(i.ene_x, i.ene_y, 0, 0, 64, -PIC_W, PIC_H, 6)
                else:
                    p.blt(i.ene_x, i.ene_y, 0, 16, 64, -PIC_W, PIC_H, 6)

            if self.boss_count == 4:
                if i.motion == 0:
                    # 骨ドラゴン
                    p.blt(i.ene_x, i.ene_y, 0, 0, 112, -PIC_W, PIC_H, 6)
                else:
                    p.blt(i.ene_x, i.ene_y, 0, 16, 112, -PIC_W, PIC_H, 6)

            if self.boss_count == 5:
                if i.motion == 0:
                    # 雷ドラゴン
                    p.blt(i.ene_x, i.ene_y, 0, 64, 128, -PIC_W, PIC_H, 6)
                else:
                    p.blt(i.ene_x, i.ene_y, 0, 80, 128, -PIC_W, PIC_H, 6)

            if self.boss_count == 6:
                if i.motion == 0:
                    # 邪悪ドラゴン
                    p.blt(i.ene_x, i.ene_y, 0, 0, 96, -PIC_W, PIC_H, 6)
                else:
                    p.blt(i.ene_x, i.ene_y, 0, 16, 96, -PIC_W, PIC_H, 6)
        else:
            # ボスの攻撃エフェクト
            if self.boss_count == 1:
                p.blt(i.ene_x, i.ene_y, 0, 48, 16, 16, 16, 6)  
            if self.boss_count == 2:
                p.blt(i.ene_x, i.ene_y, 0, 48, 48, 16, 16, 6)  
            if self.boss_count == 3:
                p.blt(i.ene_x, i.ene_y, 0, 48, 80, 16, 16, 6)  
            if self.boss_count == 4:
                p.blt(i.ene_x, i.ene_y, 0, 48, 128, 16, 16, 6)
            if self.boss_count == 5:
                p.blt(i.ene_x, i.ene_y, 0, 112, 112, 16, 16, 6)
            if self.boss_count == 6:
                p.blt(i.ene_x, i.ene_y, 0, 112, 80, 16, 16, 6)

    # ゲームスタート画面
    if self.game_start == False:
        # 画面真っ暗に
        p.cls(0)
        # 文字を画面に描画
        p.text(30, 30, "D R A G O N' S  H U N T", 7)
        p.text(30, 60, "SPACE_KEY or V_KEY = ATTAK", 7)
        p.text(30, 70, "ARROW_KEY = MOVE", 7)
        p.text(30, 90, "S = GAME START", 7)
        p.text(30, 100, "Q = QUIT", 7)

    if self.game_over == True and self.game_start == True:
        p.text(60, 50, "G A M E  O V E R", 8)
        p.text(70, 70, "S = RETRY", 8)
        p.text(70, 80, "T = TITLE", 8)

    # ゲームクリア画面
    if self.game_clear == True:
        p.cls(0)
        p.text(50, 50, "G A M E  C L E A R", p.frame_count % 16)
        p.text(55, 70, "Congratulations!!", 7)
        p.text(70, 80, "T = TITLE", 7)
     
 def ship_move(self): 
    # 機体を前進させる
    if p.btn(p.KEY_UP):
        if self.p_ship.ship_y > 30:
            self.p_ship.update(self.p_ship.ship_x, self.p_ship.ship_y - 2)

    # 機体を後進させる
    if p.btn(p.KEY_DOWN):
        if self.p_ship.ship_y < 112:
            self.p_ship.update(self.p_ship.ship_x, self.p_ship.ship_y + 2)

    # 機体を右移動させる
    if p.btn(p.KEY_RIGHT):
        if self.p_ship.ship_x < 160:
            self.p_ship.update(self.p_ship.ship_x + 3, self.p_ship.ship_y)

    # 機体を左移動させる
    if p.btn(p.KEY_LEFT):
        if self.p_ship.ship_x > 5:
            self.p_ship.update(self.p_ship.ship_x - 3, self.p_ship.ship_y)

    if not self.p_ship.ship_st == 0:
        # 遠距離攻撃の設定
        # btnp(key, [hold], [period])
        # そのフレームにkeyが押されたらTrue、holdとperiodを指定すると、holdフレーム以上ボタンを押し続けた際に
        # periodフレーム間隔でTrueが返る
        if p.btnp(p.KEY_SPACE, 10, 10):
            if self.p_ship.ship_st - settings.P_SHIP_ST_SHOOT_DECREASE >= 0: 
                self.p_ship.ship_st = self.p_ship.ship_st - settings.P_SHIP_ST_SHOOT_DECREASE
                new_shot = unit.Shot()
                new_shot.update(self.p_ship.ship_x, self.p_ship.ship_y)
                self.shots.append(new_shot)

        # 斬撃の設定
        if p.btnp(p.KEY_V, 20, 10):
            if self.p_ship.ship_st - settings.P_SHIP_ST_SLASH_DECREASE >= 0: 
                self.p_ship.ship_st = self.p_ship.ship_st - settings.P_SHIP_ST_SLASH_DECREASE
                new_slash = unit.Slash()
                new_slash.update(self.p_ship.ship_x , self.p_ship.ship_y)
                self.slash.append(new_slash)
                self.atc_flg = True

    # HPが最大以外の時に回復し続けるようにする
    if not self.p_ship.ship_hp == settings.P_SHIP_MAX_HP:
        # 4~5秒に2ぐらい回復
        if p.frame_count % 120 == 0:
            # HPの回復
            self.p_ship.ship_hp = self.p_ship.ship_hp + settings.P_SHIP_RECOVERY_COUNT_HP

    # STが最大以外の時に回復し続けるようにする
    if not self.p_ship.ship_st == settings.P_SHIP_MAX_ST:
        if p.frame_count % 5 == 0:
            # STの回復
            self.p_ship.ship_st = self.p_ship.ship_st + settings.P_SHIP_RECOVERY_COUNT_ST

 def ene_move(self):
    if self.boss_flug == False:
        # 経過フレームで敵が沸くのを制御
        if p.frame_count % 20 == 0:
            # ステージ1
            if self.boss_count == 1:
                # 敵を生成する処理
                new_enemy = unit.Enemy(1)
                # どこに座標に描画するか(画面左側)
                new_enemy.ene_x = randrange(7, 65, 16)
                self.enemys.append(new_enemy)
                new_enemy = unit.Enemy2(1)
                # 画面右側
                new_enemy.ene_x = randrange(70, 164, 16)
                self.enemys.append(new_enemy)

            # ステージ2
            elif self.boss_count == 2:
                new_enemy = unit.Enemy(2)
                new_enemy.ene_x = randrange(7, 65, 16)
                self.enemys.append(new_enemy)
                new_enemy = unit.Enemy2(2)
                new_enemy.ene_x = randrange(70, 164, 16)
                self.enemys.append(new_enemy)

            # ステージ3
            elif self.boss_count == 3:
                new_enemy = unit.Enemy(3)
                new_enemy.ene_x = randrange(7, 65, 16)
                self.enemys.append(new_enemy)
                enemy_v = randint(2, 3)
                new_enemy = unit.Enemy2(enemy_v)
                new_enemy.ene_x = randrange(70, 164, 16)
                self.enemys.append(new_enemy)

            # ステージ4
            elif self.boss_count == 4:
                enemy_v = randint(1, 3)
                new_enemy = unit.Enemy(enemy_v)
                new_enemy.ene_x = randrange(7, 65, 16)
                self.enemys.append(new_enemy)
                enemy_v = randint(2, 3)
                new_enemy = unit.Enemy2(enemy_v)
                new_enemy.ene_x = randrange(70, 164, 16)
                self.enemys.append(new_enemy)

            # ステージ5
            elif self.boss_count == 5:
                enemy_v = randint(1, 3)
                new_enemy = unit.Enemy(enemy_v)
                new_enemy.ene_x = randrange(7, 65, 16)
                self.enemys.append(new_enemy)
                enemy_v = randint(2, 3)
                new_enemy = unit.Enemy2(enemy_v)
                new_enemy.ene_x = randrange(70, 164, 16)
                self.enemys.append(new_enemy)

            # ステージ6
            elif self.boss_count == 6:
                enemy_v = randint(1, 3)
                new_enemy = unit.Enemy(enemy_v)
                new_enemy.ene_x = randrange(7, 65, 16)
                self.enemys.append(new_enemy)
                enemy_v = randint(2, 3)
                new_enemy = unit.Enemy2(enemy_v)
                new_enemy.ene_x = randrange(70, 164, 16)
                self.enemys.append(new_enemy)

    # ボス攻撃
    else:
        if self.boss_count == 1:
            # 経過時間からatkが割り切れたら攻撃
            atk_speed = 20
            if p.frame_count % atk_speed == 0:
                new_enemy = unit.Enemy(9)
                new_enemy.ene_x = self.boss.boss_x + 5
                new_enemy.ene_y = self.boss.boss_y + 8
                # 敵の攻撃は当たり判定の無い敵とする                   
                self.enemys.append(new_enemy)

        if self.boss_count == 2:
            atk_speed = 30
            if p.frame_count % atk_speed == 0:
                new_enemy = unit.Enemy(9)
                new_enemy.ene_x = self.boss.boss_x + 0
                new_enemy.ene_y = self.boss.boss_y + 8                      
                self.enemys.append(new_enemy)
                new_enemy = unit.Enemy(9)
                new_enemy.ene_x = self.boss.boss_x + 40
                new_enemy.ene_y = self.boss.boss_y + 8   
                self.enemys.append(new_enemy)

        if self.boss_count == 3:
            atk_speed = 20
            if p.frame_count % atk_speed == 0:
                new_enemy = unit.Enemy(9)
                new_enemy.ene_x = self.boss.boss_x + 0
                new_enemy.ene_y = self.boss.boss_y + 8                      
                self.enemys.append(new_enemy)
                new_enemy = unit.Enemy(9)
                new_enemy.ene_x = self.boss.boss_x + 35
                new_enemy.ene_y = self.boss.boss_y + 8   
                self.enemys.append(new_enemy)
            
        if self.boss_count == 4:
            atk_speed = 30 - (self.boss_count * 2)
            if p.frame_count % atk_speed == 0:
                new_enemy = unit.Enemy(9)
                new_enemy.ene_x = self.boss.boss_x + 10
                new_enemy.ene_y = self.boss.boss_y + 8                    
                self.enemys.append(new_enemy)
                new_enemy = unit.Enemy(9)
                new_enemy.ene_x = self.boss.boss_x + 20
                new_enemy.ene_y = self.boss.boss_y + 8   
                self.enemys.append(new_enemy)

        if self.boss_count == 5:
            atk_speed = 15
            if p.frame_count % atk_speed == 0:
                # 敵弾生成
                new_enemy = unit.Enemy(9)
                if (self.boss.boss_x <= self.p_ship.ship_x + 8
                    <= self.boss.boss_x + 45):
                    new_enemy.ene_x = self.p_ship.ship_x + 5
                else:
                    # 自機の正面にいないときの攻撃
                    new_enemy.ene_x = self.p_ship.ship_x + 5
                new_enemy.ene_y = self.boss.boss_y + 8                 
                self.enemys.append(new_enemy)
        
        if self.boss_count == 6:
            atk_speed = 9
            if p.frame_count % atk_speed == 0:
                new_enemy = unit.Enemy(9)
                if (self.boss.boss_x <= self.p_ship.ship_x + 8
                    <= self.boss.boss_x + 45):
                    new_enemy.ene_x = self.p_ship.ship_x + 5
                else:
                    new_enemy.ene_x = self.p_ship.ship_x + 5
                new_enemy.ene_y = self.boss.boss_y + 8                      
                self.enemys.append(new_enemy)
    
    enemy_count = len(self.enemys)
    for e in range (enemy_count):
        # 敵のモーション
        enemy_vec1 = randint(0, 3)
        enemy_vec2 = enemy_vec1 % 2
        if self.enemys[e].ene_y < 115:
            ene_chk =self.e_move_chk(e, self.enemys[e].ene_x, self.p_ship.ship_y)
            # 敵のy座標
            if self.enemys[e].variation == 1:
                # 座標に数字を足すことで落下速度を決める
                self.enemys[e].ene_y = self.enemys[e].ene_y + 1.3
                
            elif self.enemys[e].variation == 2:
                self.enemys[e].ene_y = self.enemys[e].ene_y + 1.3
                # 2番の敵はここでx移動をさせる
                if ene_chk == 0:
                    if self.enemys[e].ene_x > self.p_ship.ship_x:
                        self.enemys[e].ene_x=self.enemys[e].ene_x - 0.25
                    else:
                        self.enemys[e].ene_x=self.enemys[e].ene_x + 0.25

            elif self.enemys[e].variation == 3:
                if self.enemys[e].motion == 0:
                    self.enemys[e].ene_y = self.enemys[e].ene_y + 1.4
                    if self.enemys[e].ene_y > self.p_ship.ship_y - 2:
                        self.enemys[e].motion = 1
                else:
                    self.enemys[e].ene_y = self.enemys[e].ene_y - 1.2
                    # 3番の敵はここでx移動をさせる
                    if self.enemys[e].ene_x < self.p_ship.ship_x:
                        if ene_chk == 0:
                            self.enemys[e].ene_x=self.enemys[e].ene_x + 0.4
                    else:
                        if ene_chk == 0:
                            self.enemys[e].ene_x=self.enemys[e].ene_x - 0.4
                    if self.enemys[e].ene_y < self.p_ship.ship_y - 40:
                        if self.boss_count != 7 and self.boss_flug == False:
                            self.enemys[e].motion = 0
                        elif self.enemys[e].ene_y < 0:
                             del self.enemys[e]
                             break
            # ボスの攻撃
            elif self.enemys[e].variation == 9:
                if self.boss_count == 5:
                    self.enemys[e].ene_y = (self.enemys[e].ene_y + 3)
                if self.boss_count == 6:
                    self.enemys[e].ene_y = (self.enemys[e].ene_y + 1.5)
                else:
                    self.enemys[e].ene_y = (self.enemys[e].ene_y + 1.0)
            
            if p.frame_count % 10 == 0 and ene_chk == 0:
                if self.boss_flug == False:
                    # 敵のx座標
                    if self.enemys[e].variation == 1:
                        if enemy_vec2 > 0:
                            self.enemys[e].ene_x = self.enemys[e].ene_x + 4
                            if self.enemys[e].motion == 0:
                                self.enemys[e].motion = 1
                            else:
                                self.enemys[e].motion = 0
                        else:
                            self.enemys[e].ene_x = self.enemys[e].ene_x - 4
                            if self.enemys[e].motion == 0:
                                self.enemys[e].motion = 1
                            else:
                                self.enemys[e].motion = 0
                    elif self.enemys[e].variation == 2:
                        if self.enemys[e].ene_x < self.p_ship.ship_x:
                            if self.enemys[e].motion == 0:
                                self.enemys[e].motion = 1
                            else:
                                self.enemys[e].motion = 0
                        else:
                            if self.enemys[e].motion == 0:
                                self.enemys[e].motion = 1
                            else:
                                self.enemys[e].motion = 0
                    else:
                        continue
                else:
                    continue
        else:
            del self.enemys[e]
            break
    
 def e_move_chk(self, me, x, y):
    enemy_hit = len(self.enemys)
    for e in range(enemy_hit):
        if e == me:
           break
        if ((self.enemys[e].ene_x - 8 <= x + 16) and
            (self.enemys[e].ene_x + 8 <= x -16 )and
            (self.enemys[e].ene_y - 8 <= y + 8)):
               result = 1
               return result
        else:
            result = 0
            return result
     
 def hit_chk(self): #当たり判定関数
    slash_count = len(self.slash)

    # 当たり判定
    slash_hit = len(self.slash)
    if self.boss_flug == False:
        for h in range (slash_hit):
            enemy_hit = len(self.enemys)
            for e in range (enemy_hit):
                # xから左右まで35の斬撃の範囲に触れたら
                if ((self.enemys[e].ene_x - 35 <= self.slash[h].pos_x 
                    <= self.enemys[e].ene_x + 35)and
                    (self.enemys[e].ene_y - 7 <= self.slash[h].pos_y <= 
                    self.enemys[e].ene_y + 25)):
                    # 敵に当たったらその座標に爆発を乗せる
                    new_bomb = unit.Bomb(self.enemys[e].ene_x, self.enemys[e].ene_y)
                    self.bombs.append(new_bomb)

                    del self.enemys[e]
                    if self.boss_flug == False:
                        # 点数の加算処理
                        self.score = self.score + 100
                        break # 敵に当たったらbreak
                else:
                    continue
                break # 敵に当たったらbreak

    shot_count = len(self.shots)
    # 上限を超えた弾を削除
    # 弾の数だけ配列を生成
    for i in range(shot_count):
        # 画面上に存在出来る弾の数ではないかどうか
        if self.shots[i].pos_y > 10:
            # 弾を上方向に進める処理
            # 速度は数値で決定
            self.shots[i].pos_y = self.shots[i].pos_y - 7
        else:
            # 弾の削除
            del self.shots[i]
            break
        # 当たり判定
        shot_hit = len(self.shots)
        if self.boss_flug == False:
            for h in range (shot_hit):
                enemy_hit = len(self.enemys)
                for e in range (enemy_hit):
                    if ((self.enemys[e].ene_x - 8 <= self.shots[h].pos_x 
                        <= self.enemys[e].ene_x + 8)and
                        (self.enemys[e].ene_y - 7 <= self.shots[h].pos_y <= 
                        self.enemys[e].ene_y)):
                        # 敵に当たったらその座標に爆発を乗せる
                        new_bomb = unit.Bomb(self.enemys[e].ene_x, self.enemys[e].ene_y)
                        self.bombs.append(new_bomb)

                        del self.enemys[e]
                        if self.boss_flug == False:
                            # 点数の加算処理
                            self.score = self.score + 100
                            break # 敵に当たったらbreak
                    else:
                        continue
                    break # 敵に当たったらbreak

    # 敵と自機の接触確認
    enemy_atk = len(self.enemys)
    for e in range (enemy_atk):
        # 4か所で接触を検知
        # 1
        if (((self.enemys[e].ene_x + 3 >= self.p_ship.ship_x + 2) and
                (self.enemys[e].ene_x + 3 <= self.p_ship.ship_x + 14) and
                (self.enemys[e].ene_y >= self.p_ship.ship_y) and
                (self.enemys[e].ene_y <= self.p_ship.ship_y + 14))or
                # 2
                (self.enemys[e].ene_x + 12 >= self.p_ship.ship_x + 2) and
                (self.enemys[e].ene_x + 12 <= self.p_ship.ship_x + 14) and
                (self.enemys[e].ene_y >= self.p_ship.ship_y) and
                (self.enemys[e].ene_y <= self.p_ship.ship_y + 14)or
                 # 3
                (self.enemys[e].ene_x + 3 >= self.p_ship.ship_x + 2) and
                (self.enemys[e].ene_x + 3 <= self.p_ship.ship_x + 14) and
                (self.enemys[e].ene_y + 6 >= self.p_ship.ship_y) and
                (self.enemys[e].ene_y + 6 <= self.p_ship.ship_y + 14)or
                # 4
                ((self.enemys[e].ene_x + 12 >= self.p_ship.ship_x + 2) and
                (self.enemys[e].ene_x + 12 <= self.p_ship.ship_x + 14) and
                (self.enemys[e].ene_y + 6 >= self.p_ship.ship_y) and
                (self.enemys[e].ene_y + 6 <= self.p_ship.ship_y + 14))):
                # 自機の受けるダメージ計算
                if self.p_ship.ship_hp > 0: 
                    self.p_ship.ship_hp = self.p_ship.ship_hp - settings.P_SHIP_DAMAGE_COUNT
                    if self.p_ship.ship_hp == 0:
                        self.game_over = True
                    self.damage_flg = 1
                else:
                    self.game_over = True

 def boss_move(self):
    # ボス出現フラグ
    if self.boss_flug == False:
        if self.score != 0:
            # スコアがboss_appearsに当てはまればボス出現
            if self.score in self.boss_appears:
                #ゲームクリアフラグがない場合にボス発生 
                if self.game_clear == False:
                    self.boss_flug = True
                    self.enemys.clear()
                    # ステージ1のボス
                    if self.boss_count == 1:
                        self.boss_hp = 50
                    # ステージ2のボス
                    elif self.boss_count == 2:
                        self.boss_hp = 100
                    # ステージ3のボス
                    elif self.boss_count == 3:
                        self.boss_hp = 150
                    # ステージ4のボス
                    elif self.boss_count == 4:
                        self.boss_hp = 200
                    # ステージ5のボス
                    elif self.boss_count == 5:
                        self.boss_hp = 300
                    # ステージ6のラスボス
                    elif self.boss_count == 6:
                        self.boss_hp = 400
                    self.boss.update(70, 10, self.boss_hp)
                     
    # ボスの動き＆当たり判定
    if self.boss_flug == True:
        # 当たり範囲
        hitbox_x = 40
        hitbox_y = 10
        # ステージ1のボスの動き
        if self.boss_count == 1:
            if self.boss.boss_m == 0:
            # 左の動き
                if self.boss.boss_x > 1:
                    # 移動速度調整
                    self.boss.move(self.boss.boss_x - 1.2, self.boss.boss_y)
                else:
                    # 左端まで行ったら右移動させる
                    self.boss.boss_m = 1
            else:
                # 右の動き
                if self.boss.boss_x < 130:
                    self.boss.move(self.boss.boss_x + 1.2, self.boss.boss_y)
                else:
                    # 右端まで行ったら左移動させる
                    self.boss.boss_m = 0

        # ステージ2のボスの動き
        if self.boss_count == 2:
            if self.boss.boss_m == 0:
                # 左の動き
                if self.boss.boss_x > 1:
                    # 移動速度調整
                    self.boss.move(self.boss.boss_x - 1.5, self.boss.boss_y)
                else:
                    # 左端まで行ったら右移動させる
                    self.boss.boss_m = 1
            if self.boss.boss_m == 1:
                # 右の動き
                if self.boss.boss_x < 130:
                    self.boss.move(self.boss.boss_x + 1.5, self.boss.boss_y)
                else:
                    # 右端まで行ったら左移動させる
                    self.boss.boss_m = 0

        # ステージ3のボスの動き
        if self.boss_count == 3:
            if self.boss.boss_m == 0:
                if self.boss.boss_x > self.p_ship.ship_x - 8:
                    self.boss.move(self.boss.boss_x - 2, self.boss.boss_y)
                elif self.boss.boss_x == self.p_ship.ship_x - 8:
                    # 自機の正面に来たら
                    self.boss.boss_m = 1
                else:
                    self.boss.move(self.boss.boss_x + 1, self.boss.boss_y)
            elif self.boss.boss_m == 1:
                self.boss.move(self.boss.boss_x, self.boss.boss_y)
                self.boss.boss_m = 3
            else:
                self.boss.move(self.boss.boss_x, self.boss.boss_y)
                if self.boss.boss_x < self.p_ship.ship_x:
                    self.boss.boss_m = 0

        # ステージ4のボスの動き
        if self.boss_count == 4:
            if self.boss.boss_m == 0:
                if self.boss.boss_x > self.p_ship.ship_x - 8:
                    self.boss.move(self.boss.boss_x - 1, self.boss.boss_y)
                elif self.boss.boss_x == self.p_ship.ship_x - 8:
                    self.boss.boss_m = 1
                else:
                    self.boss.move(self.boss.boss_x + 1, self.boss.boss_y)
            elif self.boss.boss_m == 1:
                self.boss.move(self.boss.boss_x, self.boss.boss_y)
                self.boss.boss_m = 3
            else:
                self.boss.move(self.boss.boss_x, self.boss.boss_y)
                if self.boss.boss_x < self.p_ship.ship_x:
                    self.boss.boss_m = 0

        # ステージ5のボスの動き
        if self.boss_count == 5:
            if self.boss.boss_m == 0:
                if self.boss.boss_x > self.p_ship.ship_x - 8:
                    self.boss.move(self.boss.boss_x - 1, self.boss.boss_y)
                elif self.boss.boss_x == self.p_ship.ship_x - 8:
                    self.boss.boss_m = 1
                else:
                    self.boss.move(self.boss.boss_x + 1, self.boss.boss_y)
            elif self.boss.boss_m == 1:
                self.boss.move(self.boss.boss_x, self.boss.boss_y)
                self.boss.boss_m = 3
            else:
                self.boss.move(self.boss.boss_x, self.boss.boss_y)
                if self.boss.boss_x < self.p_ship.ship_x:
                    self.boss.boss_m = 0

        # ステージ6のボスの動き
        if self.boss_count == 6:
            if self.boss.boss_m == 0:
                if self.boss.boss_x > self.p_ship.ship_x - 8:
                    self.boss.move(self.boss.boss_x - 1, self.boss.boss_y)
                elif self.boss.boss_x == self.p_ship.ship_x - 8:
                    self.boss.boss_m = 1
                else:
                    self.boss.move(self.boss.boss_x + 1, self.boss.boss_y)
            elif self.boss.boss_m == 1:
                # 自機との距離
                if self.boss.boss_y > self.p_ship.ship_y - 60:
                    self.boss.boss_m = 3
                else:
                    self.boss.move(self.boss.boss_x, self.boss.boss_y + 1)
            else:
                self.boss.move(self.boss.boss_x, self.boss.boss_y - 1)
                if self.boss.boss_y < 10:
                    self.boss.boss_m = 0

        slash_hit = len(self.slash)
        for h in range (slash_hit):
            # 近接攻撃の当たり判定
            if ((self.boss.boss_x - 35 <= self.slash[h].pos_x 
                 <= self.boss.boss_x + 35) and
                (self.boss.boss_y - 7 <= self.slash[h].pos_y 
                 <= self.boss.boss_y + 25)):
                self.boss.boss_h = self.boss.boss_h - 3
                new_bomb = unit.Bomb(self.slash[h].pos_x, self.slash[h].pos_y -16)
                self.bombs.append(new_bomb)

        shot_hit = len(self.shots)
        for h in range (shot_hit):
            # 遠距離攻撃の当たり判定
            if ((self.boss.boss_x - 8 <= self.shots[h].pos_x 
                 <= self.boss.boss_x + hitbox_x) and
                (self.boss.boss_y <= self.shots[h].pos_y 
                 <= self.boss.boss_y + hitbox_y)):
                self.shots[h].shot_del()
                self.boss.boss_h = self.boss.boss_h - 1
                new_bomb = unit.Bomb(self.shots[h].pos_x, self.shots[h].pos_y)
                self.bombs.append(new_bomb)
                
    # ボス消滅
    if self.boss.boss_h <= 0:
        if self.boss_flug == True:
            self.score = self.score + 1000
            p.cls(0)
            self.boss_flug = False
            self.enemys.clear()
            self.boss_count = self.boss_count + 1
            # WARNINGが再び出るようにリセット
            self.warning_count = 0
            self.warning_flg = True      
            if self.boss_count == 7: #6面のボスを倒すとゲームクリア
                self.game_clear = True

 def bomb_del(self): 
    #爆発の寿命制御
    for b in self.bombs:
        b.bomb_t = b.bomb_t + 5


APP()