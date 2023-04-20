import pygame
import os

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Pang")

clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

# 배경
background = pygame.image.load(os.path.join(image_path, "background.png"))
# 스테이지
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_height = stage.get_rect().height
# 플레이어
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image_path, "character.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.rect.width
        self.height = self.rect.height
        self.rect.left = (screen_width/2) - (self.width/2)
        self.rect.top = screen_height - self.height - stage_height
        self.to_x_LEFT = 0
        self.to_x_RIGHT = 0
        self.speed = 5
# 무기
weapons = []
class Weapon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image_path, "weapon.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.width = self.rect.width
        self.rect.left
        self.rect.top
        self.speed = 10
# 공
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")).convert_alpha(),
    pygame.image.load(os.path.join(image_path, "balloon2.png")).convert_alpha(),
    pygame.image.load(os.path.join(image_path, "balloon3.png")).convert_alpha(),
    pygame.image.load(os.path.join(image_path, "balloon4.png")).convert_alpha()]
ball_speed_y = [-18, -15, -12, -9]
balls = []
class Ball(pygame.sprite.Sprite):
    def __init__(self, ball_type, left, top, to_x, to_y):
        pygame.sprite.Sprite.__init__(self)
        self.type = ball_type
        self.image = ball_images[self.type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.rect.left = left
        self.rect.top = top
        self.to_x = to_x
        self.to_y = to_y
        self.init_spd_y = ball_speed_y[self.type]

game_font = pygame.font.Font(None, 50)
total_time = 100
start_ticks = pygame.time.get_ticks()
game_result = "Game Over"

balls.append(Ball(0, 50, 50, 3, -6))
weapon_to_remove = -1
ball_to_remove = -1

player = Player()
running = True
while running:
    dt = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 키보드 조작
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.to_x_LEFT -= player.speed
            elif event.key == pygame.K_RIGHT:
                player.to_x_RIGHT += player.speed
            elif event.key == pygame.K_SPACE:
                weapon = Weapon()
                weapon.rect.left = (player.rect.left + player.width/2 - weapon.width/2)
                weapon.rect.top = player.rect.top
                weapons.append(weapon)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                player.to_x_RIGHT = 0
    # 플레이어 위치 정의, rect 정보 갱신
    player.rect.left += player.to_x_LEFT + player.to_x_RIGHT
    if player.rect.left < 0:
        player.rect.left = 0
    elif player.rect.left > screen_width - player.width:
        player.rect.left = screen_width - player.width
    # 무기 위치 조정, rect 정보 갱신
    for weapon_idx, weapon in enumerate(weapons):
        weapon.rect.top -= weapon.speed
        if weapon.rect.top <= 0:
            del weapons[weapon_idx]
    # 공 위치 정의, rect 정보 갱신
    for ball in balls:
        if ball.rect.left < 0 or ball.rect.left > screen_width - ball.width:
            ball.to_x *= -1
        if ball.rect.top >= screen_height - stage_height - ball.height:
            ball.to_y = ball.init_spd_y
        else:
            ball.to_y += 0.5
        ball.rect.left += ball.to_x
        ball.rect.top += ball.to_y
    #충돌처리
    for ball_idx, ball in enumerate(balls):
        if pygame.sprite.collide_mask(player, ball):
            running = False
            break
        for weapon_idx, weapon in enumerate(weapons):
            if pygame.sprite.collide_mask(weapon, ball):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx
                if ball.type < 3:
                    divided_ball_width = ball_images[ball.type+1].get_rect().width
                    divided_ball_height = ball_images[ball.type+1].get_rect().height
                    balls.append(Ball(ball.type+1, ball.rect.left+ball.rect.width/2-divided_ball_width/2, \
                        ball.rect.top+ball.rect.height/2-divided_ball_height/2, -3, -6))
                    balls.append(Ball(ball.type+1, ball.rect.left+ball.rect.width/2-divided_ball_width/2, \
                        ball.rect.top+ball.rect.height/2-divided_ball_height/2, 3, -6))
                break
        else:
            continue
        break    
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    if weapon_to_remove > -1:
        del weapons[weapon_idx]
        weapon_to_remove = -1

    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False
    # 화면 갱신
    screen.blit(background, (0, 0))
    for weapon in weapons:
        screen.blit(weapon.image, weapon.rect.topleft)
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(player.image, player.rect.topleft)
    for ball in balls:
        screen.blit(ball.image, ball.rect.topleft)
    # 타이머
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms=>s
    timer = game_font.render("Time : {}".format(round(total_time - elapsed_time, 1)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))
    if total_time - elapsed_time <=0:
        game_result = "Time Over"
        running = False

    pygame.display.update()
# 게임 종료 화면 표시
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()
pygame.time.delay(2000)

pygame.quit()