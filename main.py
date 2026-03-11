import pygame
import random
from cut_assets import (player_frames, player_rect,
                        pipe_head_up, pipe_core, pipe_head_down,
                        background_image,
                        die_sound, point_sound, jump_sound,
                        tile
                        )
import math

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 600))
dt = 0
score = 0
game_speed = 100
game_over = False
is_running = True
restart = False
is_start = False

background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
bg_x = 0

ground_y = screen.get_height() - tile.get_height()
ground_x = 0

font = pygame.font.SysFont(None, 40, True)

# press spacebar text
press_text = font.render("Press SPACE to start", True, (255, 255, 255))
press_rect = press_text.get_rect(center=(screen.get_width() // 2, 0))
base_y = screen.get_height() // 1.5

restart_text = font.render("R to restart", True, "black")
restart_alpha = 0

# gameover text
over_text = font.render("GAME OVER", True, "red")
over_text_rect = over_text.get_rect(center = (screen.get_width() // 2, screen.get_height() // 2))


class Player():
    def __init__(self):
        self.frames = player_frames
        self.rect = player_rect
        self.index = 0
        self.animation_speed = 10

        self.y_velocity = 0
        self.gravity = 1700
        self.jump_force = -550

    def update(self, dt):
        if is_start:
            self.y_velocity += self.gravity * dt
            self.rect.y += self.y_velocity * dt

        self.index += self.animation_speed * dt
        if self.index >= len(self.frames):
            self.index = 0

    def draw(self, screen):
        screen.blit(self.frames[int(self.index)], self.rect)

player = Player()

pipe_w = 60 
pipe_h = 30 
pipe_head_h = int(pipe_head_down.get_height() * (pipe_w / pipe_head_down.get_width())) # no stretch fomular


pipe_head_up = pygame.transform.scale(pipe_head_up, (pipe_w, pipe_head_h))
pipe_core = pygame.transform.scale(pipe_core, (pipe_w, pipe_h))
pipe_head_down = pygame.transform.scale(pipe_head_down, (pipe_w, pipe_head_h))

class Pipe():
    def __init__(self):
        self.pipe_head_up = pipe_head_up
        self.pipe_core = pipe_core
        self.pipe_head_down = pipe_head_down


        self.time_store = 0
        self.pipe_gap_time = 2

        self.pipes = []
        self.gap_size = 180
        self.gaps = []

    def update(self, dt, screen):
        if not game_over:
            self.time_store += dt
            if self.time_store >= self.pipe_gap_time:
                self.time_store = 0
                pipe_choice = random.randint(1, 10)
                current_pipe =[]

                last_rect = self.pipe_core.get_rect(bottomleft = (screen.get_width(), 0))

                for _ in range(pipe_choice):
                    rect = self.pipe_core.get_rect(topleft = (screen.get_width(), last_rect.bottom))
                    current_pipe.append((self.pipe_core, rect))
                    last_rect = rect

                head_down_rect = self.pipe_head_down.get_rect(topleft = (screen.get_width(), pipe_h * pipe_choice))
                current_pipe.append((self.pipe_head_down, head_down_rect))
                last_rect = head_down_rect

                #gap rect
                gap_rect = pygame.Rect(0, 0, pipe_w, self.gap_size)
                gap_rect.topleft = (screen.get_width(), last_rect.bottom)
                self.gaps.append(gap_rect)

                head_up_rect = self.pipe_head_up.get_rect(topleft = (screen.get_width(), gap_rect.bottom))
                current_pipe.append((self.pipe_head_up, head_up_rect))
                last_rect = head_up_rect

                lower_pipe_count = 12 - pipe_choice
                for _ in range(lower_pipe_count):
                    rect = self.pipe_core.get_rect(topleft = (screen.get_width(), last_rect.bottom))
                    current_pipe.append((self.pipe_core, rect))
                    last_rect = rect

                self.pipes.append(current_pipe)

            # move pipes
            for pipe in self.pipes[:]:
                for image, rect in pipe:
                    rect.x -= game_speed * dt

                # check first rect of that pipe
                if pipe[0][1].right <= 0:
                    self.pipes.remove(pipe)

            #move gaps
            for gap in self.gaps:
                gap.x -= game_speed * dt
            
    def draw(self, screen):
        for pipe in self.pipes:
            for image, rect in pipe:
                screen.blit(image, rect)

    def check_collision(self, bird_rect):
        for pipe in self.pipes:
            for image, rect in pipe:
                if bird_rect.colliderect(rect):
                    return True
        return False

pipe = Pipe()

while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        #key input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.y_velocity = player.jump_force
                is_start = True
                jump_sound.play()

            if event.key == pygame.K_r:
                restart = True

    screen.blit(background_image, (bg_x, 0))
    screen.blit(background_image, (bg_x + background_image.get_width(), 0))

    if not game_over:
        bg_x -= game_speed * dt
        if bg_x <= -background_image.get_width():
            bg_x = 0

        ground_x -= game_speed * dt
        if ground_x <= -tile.get_width():
            ground_x = 0

        player.update(dt)
        player.draw(screen)

        if is_start:
            pipe.update(dt, screen)
            pipe.draw(screen)

            #draw ground
            for i in range(screen.get_width() // tile.get_width() + 2):
                screen.blit(tile, (ground_x + i * tile.get_width(), ground_y))

            score_text = font.render(f"Score : {score}", True, "black")
            score_rect = score_text.get_rect(topleft=(10, 10))

            screen.blit(score_text, score_rect)
            
            for gap in pipe.gaps:
                if player.rect.centerx > gap.centerx:
                    score += 1
                    point_sound.play()
                    pipe.gaps.remove(gap)

            if player.rect.y <= 0 or player.rect.y >= ground_y:
                game_over = True
                print("game over")
                die_sound.play()

            if pipe.check_collision(player.rect):
                game_over = True
                print("game over")
                die_sound.play()

    else: # game over
        player.update(dt)
        player.draw(screen)
        pipe.draw(screen)
        
        for i in range(screen.get_width() // tile.get_width() + 2):
                screen.blit(tile, (ground_x + i * tile.get_width(), ground_y))

        # draw gameover text
        screen.blit(over_text, over_text_rect)

        # reposition score text
        score_rect.center = screen.get_width() // 2, screen.get_height() // 1.75
        screen.blit(score_text, score_rect)

        # restart text
        if restart_alpha < 255:
            restart_alpha += 200 * dt

        text = restart_text.copy()
        text.set_alpha(int(restart_alpha))

        rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()// 1.3))
        screen.blit(text, rect)


    if restart:
        is_start = False
        player.rect.center = (100, 250)
        score = 0
        game_over = False
        restart = False

        restart_alpha = 0

        pipe.pipes.clear()
        pipe.gaps.clear()

    if not is_start:
        offset = 15 * math.sin(pygame.time.get_ticks() * 0.005)
        press_rect.centery = base_y + offset
        screen.blit(press_text, press_rect)

        for i in range(screen.get_width() // tile.get_width() + 2):
                screen.blit(tile, (ground_x + i * tile.get_width(), ground_y))



    pygame.display.flip()

    dt = clock.tick(60) / 1000

# what I learned
#self.pipes[:] = make a shallow copy of the list

#for pipe in self.pipes[:]:
    #if condition:
        #self.pipes.remove(pipe)

#👉 You loop over the copy
#👉 But modify the original safely

#list.remove(pipe) = remove the actual object
#list.pop(i) = remove using index

#for x in list → x = value
#for i in range(...) → i = index

#math.sin(...) = Outputs values between -1 and 1

#colliderect() → touching = True
#contains() → fully inside = True

