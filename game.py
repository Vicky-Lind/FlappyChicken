import pygame

def main():
    game = Game()
    game.run()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = False
        self.init_graphics()
        self.init_objects()

    def init_graphics(self):
        self.bird_frame = 0
        bird_imgs = [
            pygame.image.load(f"images/chicken/flying/frame-{i}.png")
            for i in [1, 2, 3, 4]
        ]
        self.bird_imgs = [
            pygame.transform.rotozoom(x, 0, 1/16).convert_alpha()
            for x in bird_imgs
        ]

        bg_imgs = [
            pygame.image.load(f"images/background/layer_{i}.png")
            for i in [1, 2, 3]
        ]
        self.bg_imgs = [
            pygame.transform.rotozoom(x, 0, 600/x.get_height()).convert_alpha()
            for x in bg_imgs
        ]
        self.bg_width = [x.get_width() for x in self.bg_imgs]
        
    def init_objects(self):
        self.bird_y_speed = 0
        self.bird_pos = (200, 000)
        self.bird_lift = False
        self.bg_pos = [0, 0, 0]

    def run(self):
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self.handle_events()
            self.handle_game_logic()
            self.update_screen()

            # Limit to 60fps
            clock.tick(60)
            
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.bird_lift = True
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.bird_lift = False
    
    def handle_game_logic(self):
        self.bg_pos[0] -= 0.25
        self.bg_pos[1] -= 0.5
        self.bg_pos[2] -= 2

        bird_y = self.bird_pos[1]
        
        if self.bird_lift:
            # Make bird jump (0.5 px)
            self.bird_y_speed -= 1
            self.bird_frame += 1
        else:
            # Gravity (adds fall speed in every picture)
            self.bird_y_speed += 0.2
            
        bird_y += self.bird_y_speed
        self.bird_pos = (self.bird_pos[0], bird_y)
    
    def update_screen(self):
        # Paint background
        #self.screen.fill((230, 230, 255))

        # Draw the parallax (3 layers)
        for i in [0, 1, 2]:
            # Draw the first bg "set"
            self.screen.blit(self.bg_imgs[i], (self.bg_pos[i], 0))
            # If the drawn set does not fill the entire screen then..
            if self.bg_pos[i] + self.bg_width[i] < 800:
                # .. Then draw the same set next to the previous
                self.screen.blit(self.bg_imgs[i], (self.bg_pos[i] + self.bg_width[i], 0))
            # If the bg has already been moved by that width..
            if self.bg_pos[i] < -self.bg_width[i]:
                # ..Then start from start
                self.bg_pos[i] += self.bg_width[i]

        # Draw chicken
        angle = -90 * 0.04 * self.bird_y_speed
        angle = max(min(angle, 60), -60)

        bird_img_i = self.bird_imgs[(self.bird_frame // 3) % 4]
        bird_img = pygame.transform.rotozoom(bird_img_i, angle, 1)
        
        self.screen.blit(bird_img, self.bird_pos)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()