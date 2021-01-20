import pygame
import numpy as np
import tensorflow as tf
import tkinter
from tkinter import messagebox


WHITE = (255,255,255)
BLACK = (0,0,0)

class Pixel:
    def __init__(self, x, y, size=10):
        self.x = x
        self.y = y
        self.size = size
        self.color = WHITE
        self.neighbors = []

    def draw_pixel(self, window):
        pixel = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(window, self.color, pixel, 0)
        #pygame.draw.rect(window, (0,0,0), pixel, 1)

    def get_neighbors(self):
        self.neighbors = []
        # left neighbor
        if self.x - self.size >= 0:
            self.neighbors.append('left') # to change
        # right neighbor
        if self.x + self.size < 280:
            self.neighbors.append('right')
        # down neighbor
        if self.y - self.size >= 0 :
            self.neighbors.append('down')
        # up neighbor
        if self.y + self.size < 280:
            self.neighbors.append('up')
        return self.neighbors
    
class Window:
    def __init__(self, width=280, height=280):
        self.width = width
        self.height = height
        self.grid = []
        self.running = True
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Draw digit")
        self.rows = self.height // 10
        self.cols = self.width // 10
        self.generate_pixels()

    def generate_pixels(self):
        self.grid = []
        for row in range(self.rows):
            row_grid = []
            for col in range(self.cols):
                pixel = Pixel(row*10, col*10)
                pixel.draw_pixel(self.window)
                row_grid.append(pixel)
            self.grid.append(row_grid)

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                pix = self.grid[row][col]
                pix.draw_pixel(self.window)

    def draw_pixel_neighbours(self, row, col):
        self.grid[row][col].color = BLACK
        neighbors = self.grid[row][col].get_neighbors()
        if 'left' in neighbors:
            self.grid[row-1][col].color = BLACK
        if 'right' in neighbors:
            self.grid[row+1][col].color = BLACK
        if 'up' in neighbors:
            self.grid[row][col+1].color = BLACK
        if 'down' in neighbors:
            self.grid[row][col-1].color = BLACK

    def target_pixel(self, position):
        x_pos, y_pos = position
        for row in range(self.rows):
            for col in range(self.cols):
                x_pix = self.grid[row][col].x
                y_pix = self.grid[row][col].y
                pix_size = self.grid[row][col].size
                if x_pix+pix_size > x_pos >= x_pix:
                    if y_pix+pix_size > y_pos >= y_pix:
                        self.draw_pixel_neighbours(row, col)

    def get_image(self):
        array = []
        for row in range(self.rows):
            line = []
            for col in range(self.cols):
                if self.grid[row][col].color == (255,255,255):
                    line.append(0)
                else:
                    line.append(1)
            array.append(line)

        mnist = tf.keras.datasets.mnist
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        for row in range(28):
            for col in range(28):
                x_test[0][row][col] = array[row][col]

        return x_test[:1]

    def popup_message(self, prediction):
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showinfo('Prediction', f'This number is a: {prediction}')


    def predict(self, image):
        model = tf.keras.models.load_model('saved_model/')
        predictions = model.predict(image)
        prediction = np.argmax(predictions[0])
        print(prediction)
        self.popup_message(prediction)


    def event_handler(self, event):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            self.target_pixel(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                image = self.get_image()
                self.predict(image)
                self.generate_pixels()
                #print(image)
        if event.type == pygame.QUIT:
            self.running = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.event_handler(event)

            self.draw_grid()
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    win = Window(280,280)
    win.run()