import pygame
from random import randint

pygame.init()

screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Avoid Poo!!")

clock = pygame.time.Clock()

#배경
background = pygame.image.load("D:/Util/!Source/Python/pygame_basic/background_paper.jpg")
#캐릭터
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("D:/Util/!Source/Python/pygame_basic/dog.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.Rside = self.image
        self.Lside = pygame.transform.flip(self.image, True, False)
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.rect.left = (screen_width/2) - (self.width/2)
        self.rect.top = screen_height - self.height
        self.to_x_LEFT = 0
        self.to_x_RIGHT = 0
        self.speed = 0.6
#똥
class Poo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("D:/Util/!Source/Python/pygame_basic/poo.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.rect.left = randint(0, screen_width - self.width)
        self.rect.top = 0
        self.speed = 0.4
#Game Over
class GG(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("D:/Util/!Source/Python/pygame_basic/game_over.png")
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.rect.centerx = screen_width/2
        self.rect.centery = screen_height/2
class GGtext():
    def __init__(self):
        self.font = pygame.font.Font(None, 60) # 폰트 교체 필요
        self.text = self.font.render(("Game Over"), True, (0, 0, 0))
        self.rect = self.text.get_rect()
        self.rect.centerx = screen_width/2
        self.rect.centery = screen_height/2

player = Player()
poo = Poo()

running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.to_x_LEFT -= player.speed
                player.image = player.Lside
            elif event.key == pygame.K_RIGHT:
                player.to_x_RIGHT += player.speed
                player.image = player.Rside
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                player.to_x_RIGHT = 0

    # 오브젝트 위치 정의, rect 갱신
    player.rect.left += (player.to_x_LEFT + player.to_x_RIGHT) * dt
    if player.rect.left < 0:
        player.rect.left = 0
    elif player.rect.left > screen_width - player.width:
        player.rect.left = screen_width - player.width

    poo.rect.top += poo.speed * dt
    if poo.rect.top > screen_height:
        poo.rect.left = randint(0, screen_width - poo.width)
        poo.rect.top = 0

    # 충돌 처리
    if pygame.sprite.collide_mask(player, poo):
        gg = GG()
        ggt = GGtext()
        screen.blit(gg.image, gg.rect)
        screen.blit(ggt.text, ggt.rect)
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    # 화면 갱신
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect.topleft)
    screen.blit(poo.image, poo.rect.topleft)

    pygame.display.update()

pygame.quit()