# cell.py
import pygame
from settings import convert_list

pygame.font.init()

class Cell:
    def __init__(self, row, col, cell_size, value, is_correct_guess = None):
        self.row = row
        self.col = col
        self.cell_size = cell_size
        self.width = self.cell_size[0]
        self.height = self.cell_size[1]
        self.abs_x = row * self.width
        self.abs_y = col * self.height
        self.value = value
        self.is_correct_guess = is_correct_guess
        self.guesses = None if self.value != 0 else [0 for x in range(9)]
        self.color = pygame.Color("antiquewhite1")
        self.default_color = pygame.Color("antiquewhite1")
        self.selected_color = pygame.Color("thistle2")
        self.font = pygame.font.SysFont('notomono', self.cell_size[0])
        self.g_font = pygame.font.SysFont('notomono', (cell_size[0] // 3))
        self.rect = pygame.Rect(self.abs_x,self.abs_y,self.width,self.height)

    def toggle_color(self):
        if self.color == self.default_color:
            self.color = self.selected_color
        else:
            self.color = self.default_color

    def update(self, screen, SRN = None):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.value != 0:
            font_color = pygame.Color("black") if self.is_correct_guess else pygame.Color("indianred2")
            num_val = self.font.render(str(self.value), True, font_color)
            text_rect = num_val.get_rect(center=self.rect.center)  # Center the text
            screen.blit(num_val, text_rect)
        elif self.value == 0 and self.guesses != None:
            cv_list = convert_list(self.guesses, [SRN, SRN, SRN])
            for y in range(SRN):
                for x in range(SRN):
                    num_txt = " "
                    if cv_list[y][x] != 0:
                        num_txt = cv_list[y][x]
                    num_txt = self.g_font.render(str(num_txt), True, pygame.Color("firebrick2"))
                    abs_x = (self.abs_x + ((self.width // SRN) * x))
                    abs_y = (self.abs_y + ((self.height // SRN) * y))
                    abs_pos = (abs_x, abs_y)
                    screen.blit(num_txt, abs_pos)