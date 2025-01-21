import pygame
import sys

# ゲームの初期化
pygame.init()

# ゲームのウィンドウサイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("バウンスボール！ AI戦")

# 色の定義
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# プレイヤーの設定
paddle_width = 100
paddle_height = 15
paddle_speed = 10
player_x = (SCREEN_WIDTH - paddle_width) // 2
player_y = SCREEN_HEIGHT - paddle_height - 20

# AIの設定
ai_x = (SCREEN_WIDTH - paddle_width) // 2
ai_y = 20
ai_speed = 7  # AIのパッド移動速度

# ボールの設定
ball_radius = 10
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed_x = 4
ball_speed_y = -4

# ゲームの設定
score_player = 0
score_ai = 0
font = pygame.font.SysFont(None, 36)

# フレームレートの設定
clock = pygame.time.Clock()

# プレイヤーの描画
def draw_paddle(x, y, color):
    pygame.draw.rect(screen, color, (x, y, paddle_width, paddle_height))

# ボールの描画
def draw_ball(x, y):
    pygame.draw.circle(screen, RED, (x, y), ball_radius)

# スコアの描画
def draw_score():
    score_text = font.render(f"Player: {score_player}  AI: {score_ai}", True, WHITE)
    screen.blit(score_text, (20, 20))

# ボールの移動
def move_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, score_player, score_ai

    # ボールの移動
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # ボールが画面の左端または右端に当たると反射
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= SCREEN_WIDTH:
        ball_speed_x = -ball_speed_x

    # ボールが画面の上端に当たると反射
    if ball_y - ball_radius <= 0:
        ball_speed_y = -ball_speed_y

    # ボールがプレイヤーのパッドに当たると反射
    if player_x <= ball_x <= player_x + paddle_width and player_y <= ball_y + ball_radius <= player_y + paddle_height:
        ball_speed_y = -ball_speed_y

    # ボールがAIのパッドに当たると反射
    if ai_x <= ball_x <= ai_x + paddle_width and ai_y <= ball_y - ball_radius <= ai_y + paddle_height:
        ball_speed_y = -ball_speed_y

    # プレイヤーがボールを落とした場合（AIの得点）
    if ball_y + ball_radius >= SCREEN_HEIGHT:
        score_ai += 1
        reset_ball()

    # AIがボールを落とした場合（プレイヤーの得点）
    if ball_y - ball_radius <= 0:
        score_player += 1
        reset_ball()

# ボールのリセット
def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_speed_x = 4
    ball_speed_y = -4

# AIの動き
def move_ai():
    global ai_x
    if ai_x + paddle_width // 2 < ball_x:
        ai_x += ai_speed
    elif ai_x + paddle_width // 2 > ball_x:
        ai_x -= ai_speed

    # AIのパッドが画面外に出ないようにする
    if ai_x < 0:
        ai_x = 0
    if ai_x + paddle_width > SCREEN_WIDTH:
        ai_x = SCREEN_WIDTH - paddle_width

# 勝者の表示
def display_winner():
    global score_player, score_ai
    if score_player >= 3:
        winner_text = font.render("WIN", True, WHITE)
    else:
        winner_text = font.render("YOU LOSE", True, WHITE)
    screen.blit(winner_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(1000)  # 1秒待機
    
    # 再チャレンジを尋ねる
    retry_text = font.render("Press 'Y' to Retry or 'N' to Quit", True, WHITE)
    screen.blit(retry_text, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

    # 再チャレンジの入力を待つ
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # 'Y'を押した場合、ゲームをリセット
                    reset_game()
                    waiting_for_input = False
                elif event.key == pygame.K_n:  # 'N'を押した場合、ゲーム終了
                    pygame.quit()
                    sys.exit()

# ゲームをリセットする関数
def reset_game():
    global score_player, score_ai, ball_x, ball_y, player_x, ai_x
    score_player = 0
    score_ai = 0
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    player_x = (SCREEN_WIDTH - paddle_width) // 2
    ai_x = (SCREEN_WIDTH - paddle_width) // 2

# メインゲームループ
async def main():
    while True:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                await asyncio.sleep(0)

        # ゲーム終了判定
        if score_player >= 3 or score_ai >= 3:
            display_winner()

        # キー入力
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= paddle_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - paddle_width:
            player_x += paddle_speed

        # AIの動き
        move_ai()

        # ボールの移動と衝突判定
        move_ball()

        # 画面更新
        screen.fill(BLACK)

        # プレイヤーとAIの描画
        draw_paddle(player_x, player_y, BLUE)  # プレイヤー
        draw_paddle(ai_x, ai_y, RED)  # AI

        # ボールの描画
        draw_ball(ball_x, ball_y)

        # スコアの描画
        draw_score()

        # 画面更新
        pygame.display.flip()

        # フレームレート
        clock.tick(60)

# `pygbag` 用にゲームを実行
if __name__ == "__main__":
    import pygbag
    pygbag.run(main)
