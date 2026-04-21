import os
import sys
import pygame as pg
import random  # 乱数を使うために追加

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # --- 練習問題2：爆弾の作成 ---
    bb_img = pg.Surface((20, 20))           # 20x20の空のSurfaceを作成
    bb_img.set_colorkey((0, 0, 0))          # 黒い部分を透明にする
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) # 赤い円を描く
    bb_rct = bb_img.get_rect()              # 爆弾Rectの抽出
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) # 中心座標を乱数で設定
    vx, vy = +5, +5                         # 爆弾の速度
    # ----------------------------

    clock = pg.time.Clock()
    tmr = 0

    # 辞書はループの外に出しておくと効率が良いです
    DELTA = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        screen.blit(bg_img, [0, 0]) 

        # こうかとんの移動処理
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        screen.blit(kk_img, kk_rct)

        # --- 練習問題2：爆弾の移動と表示 ---
        bb_rct.move_ip(vx, vy)    # 爆弾を速度に合わせて移動
        screen.blit(bb_img, bb_rct) # 爆弾を貼り付け
        # -------------------------------

        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()