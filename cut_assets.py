import pygame
import os

pygame.init()
screen = pygame.display.set_mode((500, 500))

base_path = os.path.dirname(__file__) # get the folder that this file in

def get_path(file):
    return os.path.join(base_path, file) # build full path

player_sheet = pygame.image.load(get_path("assets/Player/Bird2-6.png")).convert_alpha()
tile_sheet = pygame.image.load(get_path("assets/Tiles/SimpleStyle1.png")).convert_alpha()
pipe_sheet = pygame.image.load(get_path("assets/Tiles/PipeStyle1.png")).convert_alpha()
background_image = pygame.image.load(get_path("assets/Background/Background9.png")).convert_alpha()

die_sound = pygame.mixer.Sound(get_path("assets/sounds/sfx_hit.wav"))
point_sound = pygame.mixer.Sound(get_path("assets/sounds/sfx_point.wav"))
jump_sound = pygame.mixer.Sound(get_path("assets/sounds/sfx_wing.wav"))

player_hight = 50
player_width = 50
# player frames
player_frames = []
player_frame_width = player_sheet.get_width() // 4

for i in range(4):
    frame = player_sheet.subsurface((i * player_frame_width, 0, player_frame_width, player_sheet.get_height()))
    frame = pygame.transform.scale(frame, (player_hight, player_width))
    player_frames.append(frame)

player_rect = player_frames[0].get_rect(center = (100, 250)) # take 1 frame from list and get rect

# pipe image

pipe_frame_width = pipe_sheet.get_width() // 4
pipe_frame_hight = pipe_sheet.get_height() // 2

pipe_head_up = pipe_sheet.subsurface((0, 0, pipe_frame_width, pipe_frame_hight // 4))
pipe_core = pipe_sheet.subsurface((0, pipe_frame_hight // 4, pipe_frame_width, 40))
pipe_head_down = pipe_sheet.subsurface((0, 60, pipe_frame_width, pipe_frame_hight // 4))

# tile image
tile_width = tile_sheet.get_width() // 2
tile_height = 20

tile = tile_sheet.subsurface((0, tile_sheet.get_height() - 32, tile_width, tile_height))
tile = pygame.transform.scale(tile, (tile_width * 2, tile_height * 2))

