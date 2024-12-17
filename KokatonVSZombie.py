import pygame as pg
import sys
import random

# Pygameの初期化
pg.init()

# 画面サイズとマス目サイズの設定
SCREEN_WIDTH = 800  # 画面の幅
SCREEN_HEIGHT = 600  # 画面の高さ
GRID_SIZE = 80  # 1つのマスのサイズ
INFO_AREA_HEIGHT = 80  # 上部の情報エリアの高さ

# 色の定義 (RGB形式)
GREEN = (0, 128, 0)  # 背景の緑色
WHITE = (255, 255, 255)  # マス目の線の色
BLACK = (0, 0, 0)  # テキストの色
GRAY = (200, 200, 200)  # 情報エリアの背景色
RED = (255, 0, 0)  # ゾンビの色
BLUE = (0, 0, 255)  # 植物の色


# 画面の作成
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Plants vs Zombies 風ゲーム")

# フォントの設定
font = pg.font.Font(None, 36)

# ゾンビクラスの定義
class Zombie:
    def __init__(self, x, y, speed):
        self.rect = pg.Rect(x, y, GRID_SIZE, GRID_SIZE)  # ゾンビを長方形で表す
        self.speed = speed
        self.alive = True  # 障害物に到達すると停止

    def move(self, obstacles):
        if self.alive:
            # ゾンビが障害物に衝突しているか確認
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle):
                    self.alive = False  # 衝突したら停止
                    return
            # 左に移動
            self.rect.x -= self.speed

    def draw(self, surface):
        pg.draw.rect(surface, RED, self.rect)


# テキストを描画する関数
def draw_text(surface, text, x, y, color):
    rendered_text = font.render(text, True, color)
    surface.blit(rendered_text, (x, y))

# マス目を描画する関数
def draw_grid(surface, width, height, grid_size, offset_y):
    for x in range(0, width, grid_size):
        pg.draw.line(surface, WHITE, (x, offset_y), (x, height))
    for y in range(offset_y, height, grid_size):
        pg.draw.line(surface, WHITE, (0, y), (width, y))

# 情報エリアを描画する関数
def draw_info_area(surface, width, height):
    pg.draw.rect(surface, GRAY, (0, 0, width, height))
    draw_text(surface, "score: 0", 20, 20, BLACK)
    draw_text(surface, "set", 200, 20, BLACK)

# メインのゲームループ
def main():
    clock = pg.time.Clock()

    # 障害物（植物）を格納するリスト
    plants = []

    # ゾンビ(敵)を格納するリスト
    zombies = []

    # ゲームをスタートしてからの時間
    count_ = 0

    # ゲームループ
    while True:
        print(clock)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                # マウスクリックで植物を配置
                mouse_x, mouse_y = event.pos
                if mouse_y > INFO_AREA_HEIGHT:  # 情報エリア以外をクリック可能
                    grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE
                    grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE
                    plant_rect = pg.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE)
                    plants.append(plant_rect)

        # 背景の描画
        screen.fill(GREEN)

        # 情報エリアの描画
        draw_info_area(screen, SCREEN_WIDTH, INFO_AREA_HEIGHT)

        # マス目の描画
        draw_grid(screen, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, INFO_AREA_HEIGHT)

        # 植物の描画
        for plant in plants:
            pg.draw.rect(screen, BLUE, plant)

        # ゾンビの動きと描画
        # zombie.move(plants)
        # zombie.draw(screen)

        if count_ % 100 == 0:  # 何フレームごとにゾンビを配置
            zombies.append(Zombie(SCREEN_WIDTH, INFO_AREA_HEIGHT + GRID_SIZE * random.randint(0, 5), 2))

        for zombie in zombies:
            zombie.move(plants)
            zombie.draw(screen)

        for zombie in zombies:
            # 画面外にゾンビが出たら消す
            if zombie.rect.x + GRID_SIZE < 0:
                zombies.remove(zombie)



        # 画面の更新
        pg.display.update()
        clock.tick(60)

        count_ += 1

# メイン関数の実行
if __name__ == "__main__":
    main()