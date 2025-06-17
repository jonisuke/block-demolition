import pygame
import sys
import random

# ゲームの設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 25  # 画像のサイズに合わせて調整
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BLOCK_WIDTH = 50  # ブロックのサイズを調整
BLOCK_HEIGHT = 30
BLOCK_ROWS = 10   # ブロックの行数を倍に
BLOCK_COLS = 20   # ブロックの列数を倍に

# ゲーム初期化
pygame.init()
pygame.mixer.init()  # サウンドの初期化
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("コーギーコーナー")

clock = pygame.time.Clock()

# 画像と音声の読み込み
ball_image = pygame.image.load('corgi-sprite.png')
ball_image = pygame.transform.scale(ball_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))
ball_rect = ball_image.get_rect()

# 音声の読み込み
hit_sound = pygame.mixer.Sound('hit.wav')  # ブロックを壊した時の音
hit_sound.set_volume(0.5)  # 音量を調整

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# ゲーム初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ブロック崩し")
clock = pygame.time.Clock()

# パドルの設定
class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - 50
        self.speed = 8

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

# ボールの設定
class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.reset()

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 70
        self.speed_x = 4 * random.choice([-1, 1])  # 少し遅くする
        self.speed_y = -4

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # 壁との衝突判定
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.speed_x *= -1
        if self.y <= self.radius:
            self.speed_y *= -1

    def draw(self):
        ball_rect.center = (self.x, self.y)
        screen.blit(ball_image, ball_rect)

# ブロックの設定
class Block:
    def __init__(self, x, y):
        self.width = BLOCK_WIDTH
        self.height = BLOCK_HEIGHT
        self.x = x
        self.y = y
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.active = True

    def draw(self):
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# ゲームの初期化
# ゲーム状態の定義
GAME_STATE_TITLE = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (0, 150, 0)
        self.hover_color = (0, 200, 0)
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def init_game():
    global paddle, ball, blocks
    paddle = Paddle()
    ball = Ball()
    blocks = []
    
    # ブロックの配置
    for row in range(BLOCK_ROWS):
        for col in range(BLOCK_COLS):
            x = col * (BLOCK_WIDTH + 5) + 50
            y = row * (BLOCK_HEIGHT + 5) + 50
            blocks.append(Block(x, y))
            
    return GAME_STATE_PLAYING

# ブロックとの衝突判定
def check_collision():
    global blocks
    
    # パドルとの衝突
    if (paddle.x <= ball.x <= paddle.x + paddle.width and
        paddle.y - ball.radius <= ball.y <= paddle.y + paddle.height):
        ball.speed_y *= -1
        hit_sound.play()

    # ブロックとの衝突
    for block in blocks:
        if not block.active:
            continue
            
        if (block.x <= ball.x <= block.x + block.width and
            block.y <= ball.y <= block.y + block.height):
            block.active = False
            ball.speed_y *= -1
            hit_sound.play()
            return True
    return False

# タイトル画面表示
def show_title_screen():
    screen.fill(BLACK)
    
    # タイトルテキスト
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("コーギーコーナー", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
    screen.blit(title_text, title_rect)
    
    # スタートボタン
    start_button = Button(
        SCREEN_WIDTH//2 - 150,
        SCREEN_HEIGHT//2,
        300,
        80,
        "START"
    )
    start_button.draw(screen)
    
    # インストラクション
    font = pygame.font.Font(None, 36)
    instruction_text = font.render("コーギーを動かしてブロックを壊そう！", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
    screen.blit(instruction_text, instruction_rect)
    
    pygame.display.flip()
    return start_button

# ゲームオーバー画面表示
def show_game_over_screen(score):
    screen.fill(BLACK)
    
    # ゲームオーバーテキスト
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("GAME OVER", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
    screen.blit(game_over_text, game_over_rect)
    
    # スコア表示
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(score_text, score_rect)
    
    # リトライ/タイトルボタン
    retry_button = Button(
        SCREEN_WIDTH//4 - 125,
        SCREEN_HEIGHT * 2//3,
        250,
        80,
        "RETRY"
    )
    retry_button.draw(screen)
    
    title_button = Button(
        SCREEN_WIDTH * 3//4 - 125,
        SCREEN_HEIGHT * 2//3,
        250,
        80,
        "TITLE"
    )
    title_button.draw(screen)
    
    pygame.display.flip()
    return retry_button, title_button

# ゲームオーバー画面表示
def show_game_over_screen(score):
    screen.fill(BLACK)
    
    # ゲームオーバーテキスト
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("GAME OVER", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
    screen.blit(game_over_text, game_over_rect)
    
    # スコア表示
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(score_text, score_rect)
    
    # リトライ/タイトルボタン
    retry_button = Button(
        SCREEN_WIDTH//4 - 100,
        SCREEN_HEIGHT * 2//3,
        200,
        50,
        "RETRY"
    )
    retry_button.draw(screen)
    
    title_button = Button(
        SCREEN_WIDTH * 3//4 - 100,
        SCREEN_HEIGHT * 2//3,
        200,
        50,
        "TITLE"
    )
    title_button.draw(screen)
    
    pygame.display.flip()
    return retry_button, title_button

# ゲームループ
def game_loop():
    game_state = GAME_STATE_TITLE
    score = 0
    
    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == GAME_STATE_TITLE:
                    start_button = show_title_screen()
                    if start_button.is_clicked(event.pos):
                        game_state = init_game()
                        score = 0
                elif game_state == GAME_STATE_GAME_OVER:
                    retry_button, title_button = show_game_over_screen(score)
                    if retry_button.is_clicked(event.pos):
                        game_state = init_game()
                        score = 0
                    elif title_button.is_clicked(event.pos):
                        game_state = GAME_STATE_TITLE

        if game_state == GAME_STATE_PLAYING:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move("left")
            if keys[pygame.K_RIGHT]:
                paddle.move("right")

            ball.move()
            if check_collision():
                score += 10

            # ゲームオーバー判定
            if ball.y > SCREEN_HEIGHT:
                game_state = GAME_STATE_GAME_OVER

            # 全てのブロックを破壊した場合
            if all(not block.active for block in blocks):
                game_state = GAME_STATE_GAME_OVER

            # 描画
            paddle.draw()
            ball.draw()
            for block in blocks:
                block.draw()

            # スコア表示
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {score}', True, WHITE)
            screen.blit(score_text, (10, 10))

        elif game_state == GAME_STATE_TITLE:
            show_title_screen()
        elif game_state == GAME_STATE_GAME_OVER:
            show_game_over_screen(score)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
