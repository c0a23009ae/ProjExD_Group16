import pygame
import sys

# Pygameの初期化
pygame.init()

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
YELLOW = (255, 255, 0)  # SET用の植物

# 画面の作成
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plants vs Zombies 風ゲーム")

# フォントの設定
font = pygame.font.Font(None, 36)

# ゾンビクラスの定義
class Zombie:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        self.speed = speed
        self.alive = True

    def move(self, obstacles):
        if self.alive:
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle):
                    self.alive = False
                    return
            self.rect.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

# テキストを描画する関数
def draw_text(surface, text, x, y, color):
    rendered_text = font.render(text, True, color)
    surface.blit(rendered_text, (x, y))

# マス目を描画する関数
def draw_grid(surface, width, height, grid_size, offset_y):
    for x in range(0, width, grid_size):
        pygame.draw.line(surface, WHITE, (x, offset_y), (x, height))
    for y in range(offset_y, height, grid_size):
        pygame.draw.line(surface, WHITE, (0, y), (width, y))

# 情報エリアを描画する関数
def draw_info_area(surface, width, height, plant_icon):
    pygame.draw.rect(surface, GRAY, (0, 0, width, height))
    draw_text(surface, "score: 0", 20, 20, BLACK)
    draw_text(surface, "SET", 200, 20, BLACK)
    surface.blit(plant_icon, (250, 20))  # SETエリアに植物のアイコンを表示

# メインのゲームループ
def main():
    clock = pygame.time.Clock()

    # ゾンビを1体生成
    zombie = Zombie(SCREEN_WIDTH, INFO_AREA_HEIGHT + GRID_SIZE * 2, 2)

    # 障害物（植物）を格納するリスト
    plants = []

    # 植物のアイコンを定義（SETエリア用）
    plant_icon = pygame.Surface((GRID_SIZE, GRID_SIZE))
    plant_icon.fill(YELLOW)  # SETエリアの植物は黄色

    dragging = False  # ドラッグ中かどうかを判定
    plant_drag_rect = plant_icon.get_rect(topleft=(250, 20))  # ドラッグ用の植物

    # ゲームループ
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ドラッグ開始
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if plant_drag_rect.collidepoint(event.pos):  # SETエリアの植物をクリック
                    dragging = True

            # ドラッグ中の処理
            elif event.type == pygame.MOUSEMOTION and dragging:
                plant_drag_rect.center = event.pos  # マウスの位置に追従

            # ドラッグ終了（植物を配置）
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                dragging = False
                mouse_x, mouse_y = event.pos
                if mouse_y > INFO_AREA_HEIGHT:  # 情報エリア外に配置
                    grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE
                    grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE
                    plants.append(pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE))

                # ドラッグ位置を初期化
                plant_drag_rect.topleft = (250, 20)

        # 背景の描画
        screen.fill(GREEN)

        # 情報エリアとSETエリアの描画
        draw_info_area(screen, SCREEN_WIDTH, INFO_AREA_HEIGHT, plant_icon)

        # マス目の描画
        draw_grid(screen, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, INFO_AREA_HEIGHT)

        # 植物の描画
        for plant in plants:
            pygame.draw.rect(screen, BLUE, plant)

        # ドラッグ中の植物の描画
        if dragging:
            screen.blit(plant_icon, plant_drag_rect.topleft)

        # ゾンビの動きと描画
        zombie.move(plants)
        zombie.draw(screen)

        # 画面の更新
        pygame.display.update()
        clock.tick(60)

# メイン関数の実行
if __name__ == "__main__":
    main()