import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

    def run(self):
        self.clock = pygame.time.Clock()
        self.running = True
        
        while self.running:
            
            self.screen.fill((255, 255, 255))
            pygame.display.flip()

            # Limit to 60fps
            self.clock.tick(60)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
if __name__ == "__main__":
    main()