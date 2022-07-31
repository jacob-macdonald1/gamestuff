import sys
import pygame as pg
import time
from pygame.locals import *

pg.init()
display = pg.display.set_mode((1300, 700))
pg.display.set_caption("Jump-Jump Bean")


class Main(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((40, 40))
        self.image.fill("red")

        self.rect = self.image.get_rect()
        self.rect.center = (21, 679)

        self.move_right = False
        self.move_left = False
        self.isJump = False
        self.jumpCount = 10

        self.gone = False

    def jump(self):
        scaling_factor = 0.5
        if self.isJump:
            if self.jumpCount >= -10:
                reverse = 1
                if self.jumpCount < 0:
                    reverse = -1
                self.rect.y -= self.jumpCount ** 2 * \
                               scaling_factor * reverse
                self.jumpCount -= 1
            else:
                self.rect.y += 5
                self.isJump = False
                self.jumpCount = 10

    def platform1(self):
        self.p1_rect = pg.draw.rect(display, "blue", pg.Rect(350, 575, 350, 20))
        self.collide1 = pg.Rect.colliderect(self.p1_rect, self.rect)
        if self.collide1:
            self.rect.y = self.p1_rect.y - 35
        else:
            self.rect.y += 7

    def platform2(self):
        self.p2_rect = pg.draw.rect(display, "white", pg.Rect(0, 690, 1300, 30))
        self.collide2 = pg.Rect.colliderect(self.p2_rect, self.rect)
        if self.collide2:
            self.rect.y = self.p2_rect.y - 40

    def right(self):
        if self.move_right:
            self.rect.x += 10

    def left(self):
        if self.move_left:
            self.rect.x -= 10


class Bean_Bean(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.image = pg.Surface((18, 35))
        self.image.fill("green")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.gone = False
        self.eat_sound = pg.mixer.Sound("eat_sound.wav")

    def bean_eat(self):
        pg.mixer.init(44100)
        if pg.Rect.colliderect(M.rect, self.rect) and not self.gone:
            self.kill()
            pg.mixer.Sound.play(self.eat_sound)
            pg.mixer.music.stop()
            self.gone = True




if __name__ == '__main__':

    M = Main()
    BB = Bean_Bean(655, 555)
    all_sprites = pg.sprite.Group()
    all_sprites.add(BB)


    while True:
        pg.time.Clock().tick(60)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    M.move_left = True
                    M.move_right = False
                if event.key == pg.K_d:
                    M.move_left = False
                    M.move_right = True
                if event.key == pg.K_w:
                    M.isJump = True

            elif event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    M.move_left = False
                if event.key == pg.K_d:
                    M.move_right = False

        display.fill("black")
        M.jump()
        M.left()
        M.right()
        M.platform1()
        M.platform2()
        BB.bean_eat()

        all_sprites.add(M)
        all_sprites.update()
        all_sprites.draw(display)

        pg.display.flip()