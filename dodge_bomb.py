import os
import sys
import pygame as pg
import random

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

def get_bomb_param(tmr: int) -> tuple[int, pg.Surface]: # 戻り値の型ヒントを修正
    """
    タイマーの値に応じて爆弾の加速度と拡大Surfaceを返す
    引数 tmr：経過時間（タイマー）
    戻り値：(加速度, 拡大Surface)
    """
    accs = [a for a in range(1, 11)] # 加速度1〜10
    imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        imgs.append(bb_img)

    idx = min(tmr // 500, 9) # 500フレーム（約10秒）ごとにレベルアップ
    return accs[idx], imgs[idx]

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 初期爆弾の設定
    vx, vy = +5, +5
    bb_img = pg.Surface((20, 20)) # ダミー（ループ内で更新されるため）
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    clock = pg.time.Clock()
    tmr = 0 # タイマー初期化
    DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, +5), pg.K_LEFT: (-5, 0), pg.K_RIGHT: (+5, 0)}

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        
        # --- 追加機能2：爆弾のパラメータ取得 ---
        acc, bb_img = get_bomb_param(tmr)
        avx, avy = vx * acc, vy * acc # 加速させた速度
        
        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            return 

        screen.blit(bg_img, [0, 0]) 

        # こうかとんの移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # 爆弾の移動（加速版を使用）
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(kk_img, kk_rct)
        # 爆弾のサイズ変更に対応して再描画
        screen.blit(bb_img, bb_rct) 
        
        pg.display.update()
        tmr += 1 # タイマーを加算
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()