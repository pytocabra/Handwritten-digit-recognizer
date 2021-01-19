import pygame


class Pixel:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (255,255,255)
        self.neighbors = []

    def draw_pixel(sefl, window):
        pixel = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(window, self.color, pixel, 0)

    
class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.running = True
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Draw digit")

    def draw_pixels(self, pixel, rows, cols):
        for row in rows:
            for col in cols:
                pass
                

    def event_handler(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.event_handler(event)

            self.window.fill((125,10,255))
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    win = Window(400,400)
    win.run()