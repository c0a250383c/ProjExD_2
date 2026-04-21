import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：真理値タプル（横方向, 縦方向）／ True：画面内，False：画面外
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: 
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    10段階の爆弾Surfaceリストと加速度リストを返す
    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動量タプルをキー、rotozoomしたSurfaceを値とした辞書を返す
    """
    img0 = pg.image.load("fig/3.png") # 左向き
    img1 = pg.transform.flip(img0, True, False) # 右向き
    
    kk_dict = {
        (0, 0):   pg.transform.rotozoom(img1, 0, 0.9),    # 停止
        (+5, 0):  pg.transform.rotozoom(img1, 0, 0.9),    # 右
        (+5, -5): pg.transform.rotozoom(img1, 45, 0.9),   # 右上
        (0, -5):  pg.transform.rotozoom(img1, 90, 0.9),   # 上
        (-5, -5): pg.transform.rotozoom(img0, -45, 0.9),  # 左上
        (-5, 0):  pg.transform.rotozoom(img0, 0, 0.9),    # 左
        (-5, +5): pg.transform.rotozoom(img0, 45, 0.9),   # 左下
        (0, +5):  pg.transform.rotozoom(img1, -90, 0.9),  # 下
        (+5, +5): pg.transform.rotozoom(img1, -45, 0.9),  # 右下
    }
    return kk_dict

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する
    """
    black_out = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_out, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    black_out.set_alpha(150)
    
    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2
    
    cry_img = pg.image.load("fig/8.png")
    cry_rct1 = cry_img.get_rect(); cry_rct1.center = WIDTH // 2 - 200, HEIGHT // 2
    cry_rct2 = cry_img.get_rect(); cry_rct2.center = WIDTH // 2 + 200, HEIGHT // 2
    
    screen.blit(black_out, [0, 0])
    screen.blit(txt, txt_rct)
    screen.blit(cry_img, cry_rct1)
    screen.blit(cry_img, cry_rct2)
    pg.display.update()
    time.sleep(5)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    
    # こうかとん初期設定
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾初期設定
    bb_imgs, bb_accs = init_bb_imgs()
    vx, vy = +5, +5
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    clock = pg.time.Clock()
    tmr = 0
    DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, +5), pg.K_LEFT: (-5, 0), pg.K_RIGHT: (+5, 0)}

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        
        # 爆弾のパラメータ更新
        idx = min(tmr // 500, 9)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_img = bb_imgs[idx]
        # Rectのサイズ更新（当たり判定の拡大）
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        
        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return 

        screen.blit(bg_img, [0, 0]) 
        
        # こうかとん移動処理
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        # 移動量に合わせて画像を切り替え
        if tuple(sum_mv) in kk_imgs:
            kk_img = kk_imgs[tuple(sum_mv)]
            
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # 爆弾移動処理
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