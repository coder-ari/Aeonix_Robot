import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the display    
"""screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))"""
display_info = pygame.display.Info()
screen_width = display_info.current_w
screen_height = display_info.current_h

# Find the secondary display (if any)
num_displays = pygame.display.get_num_displays()

# If there is more than one display, use the secondary display
if num_displays > 1:
    secondary_display_index = 1
else:
    secondary_display_index = 0

# Set up the display on the secondary screen
pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN, display=secondary_display_index)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('Sprite Animation with Key Presses')


sprite_folders = {
    'blink': ('D:/aeonix_grapics/frames/blink', 0.75,2.0),    
    'dir': ('D:/aeonix_grapics/frames/dir', 0.2, 0.0),   
    'talk': ('D:/aeonix_grapics/frames/talk', 0.3, 0.0),
    'up':('D:/aeonix_grapics/frames/up',0.05,2.0),
    'down':('D:/aeonix_grapics/frames/down',0.05,2.0),
    'right':('D:/aeonix_grapics/frames/right',0.05,2.0),
    'left':('D:/aeonix_grapics/frames/left',0.05,2.0)     
}

# Load images from the given folder
def load_images(folder):
    images = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith('.png'):
            images.append(pygame.image.load(os.path.join(folder, filename)))
    return images

# Load all animations with their respective speeds and pause times
animations = {key: (load_images(folder), speed, pause_time) for key, (folder, speed, pause_time) in sprite_folders.items()}

# Define the main sprite class
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, animations, position):
        super().__init__()
        self.animations = animations
        self.current_animation = 'blink'
        self.images, self.animation_speed, self.pause_time = self.animations[self.current_animation]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.current_frame = 0
        self.pausing = False
        self.pause_timer = 0

    def update(self):
        if self.pausing:
            self.pause_timer += 1
            if self.pause_timer >= self.pause_time * 60:  # Convert pause time to frames
                self.pausing = False
                self.pause_timer = 0
        else:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.images):
                self.current_frame = 0
                if self.current_animation == 'blink':
                    self.pausing = True
            self.current_image = int(self.current_frame)
            self.image = self.images[self.current_image]

    def set_animation(self, animation):
        if animation in self.animations and self.current_animation != animation:
            self.current_animation = animation
            self.images, self.animation_speed, self.pause_time = self.animations[self.current_animation]
            self.current_frame = 0
            self.pausing = False
            self.pause_timer = 0

# Create a sprite group and add the sprite
all_sprites = pygame.sprite.Group()
sprite = AnimatedSprite(animations, (0,0))
all_sprites.add(sprite)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                sprite.set_animation('blink')
            elif event.key == pygame.K_p:
                sprite.set_animation('dir')
            elif event.key == pygame.K_t:
                sprite.set_animation('talk')
            elif event.key == pygame.K_w:
                sprite.set_animation('up')
            elif event.key == pygame.K_s:
                sprite.set_animation('down')
            elif event.key == pygame.K_a:
                sprite.set_animation('left')
            elif event.key == pygame.K_d:
                sprite.set_animation('right')

    # Update the sprites
    all_sprites.update()

    # Draw everything
    screen.fill((0, 0, 0))  # Fill the screen with white
    all_sprites.draw(screen)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
