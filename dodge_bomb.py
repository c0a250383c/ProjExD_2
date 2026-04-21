import os
import sys
import pygame as pg
import random
import time # 追加

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- 練習問題3：判定関数 ---
def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: tate = False
    return yoko, tate

# --- 追加機能1：ゲームオーバー画面 ---
def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する
    引数 screen：画面Surface
    """
    # 1. 黒い矩形を描画するための空のSurfaceを作り、黒い矩形を描画する
    black_out = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_out, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    # 2. Surfaceの透明度を設定する
    black_out.set_alpha(150)
    
    # 3. 白文字でGame Overと書かれたフォントSurfaceを作成
    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2
    
    # 4. 泣いているこうかとん画像をロードし、配置
    cry_img = pg.image.load("fig/8.png")
    cry_rct1 = cry_img.get_rect()
    cry_rct1.center = WIDTH // 2 - 200, HEIGHT // 2
    cry_rct2 = cry_img.get_rect()
    cry_rct2.center = WIDTH // 2 + 200, HEIGHT // 2
    
    # 描画
    screen.blit(black_out, [0, 0])
    screen.blit(txt, txt_rct)
    screen.blit(cry_img, cry_rct1)
    screen.blit(cry_img, cry_rct2)
    
    pg.display.update() # 5. 画面更新
    time.sleep(5)      # 6. 5秒間停止

def get_bomb_param(tmr: int) -> tuple[int, pg.Surface]:
    accs = [a for a in range(1, 11)]
    imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        imgs.append(bb_img)
    idx = min(tmr // 500, 9)
    return accs[idx], imgs[idx]

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    vx, vy = +5, +5
    bb_img = pg.Surface((20, 20))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    clock = pg.time.Clock()
    tmr = 0
    DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, +5), pg.K_LEFT: (-5, 0), pg.K_RIGHT: (+5, 0)}

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        
        acc, bb_img = get_bomb_param(tmr)
        avx, avy = vx * acc, vy * acc
        
        # --- 衝突判定でgameoverを呼び出す ---
        if kk_rct.colliderect(bb_rct):
            gameover(screen) # 追加
            return 

        screen.blit(bg_img, [0, 0]) 
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: vx *= -1
        if not tate: vy *= -1

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct) 
        
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()