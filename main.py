# main.py
import pygame, sys
from settings import WIDTH, HEIGHT, CELL_SIZE
from table import Table
import pygame.time

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT + (CELL_SIZE[1] * 3)))
pygame.display.set_caption("Sudoku")

pygame.font.init()


class Main:
    def __init__(self, screen):
        self.screen = screen
        self.FPS = pygame.time.Clock()
        self.lives_font = pygame.font.SysFont("notomono", CELL_SIZE[0] // 2)
        self.message_font = pygame.font.SysFont("googlesans", (CELL_SIZE[0]))
        self.color = pygame.Color("darkgreen")

    def main(self):
        table = Table(self.screen)
        while True:
            self.screen.fill("lavender")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if table.difficulty:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        table.handle_mouse_click(event.pos)
                    elif event.type == pygame.KEYDOWN:
                        table.handle_keyboard_input(event)
                elif (
                    not table.difficulty
                ):  # Allow interaction only if difficulty is not selected
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Check if the click is within the new game button area
                        if (
                            table.new_game_button
                            and table.new_game_button.collidepoint(event.pos)
                        ):
                            table._select_difficulty()  # Start a new game

            if table.difficulty and not table.game_over:
                my_lives = self.lives_font.render(
                    f"Lives Left: {table.lives}", True, pygame.Color("navyblue")
                )
                self.screen.blit(
                    my_lives,
                    (
                        (WIDTH // table.SRN) - (CELL_SIZE[0] // 2),
                        HEIGHT + (CELL_SIZE[1] * 2.2),
                    ),
                )
                table.update()
            elif not table.new_game_button:
                if table.lives <= 0:
                    message = self.message_font.render(
                        "GAME OVER!", True, pygame.Color("indianred2")
                    )
                    message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    self.screen.blit(message, message_rect)

                elif table.lives > 0:
                    message = self.message_font.render(
                        "CONGRATS!", True, pygame.Color("seagreen3")
                    )
                    message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    self.screen.blit(message, message_rect)
                pygame.time.delay(1000)
                table.update2()
            if not table.difficulty:
                # Display the buttons for selecting difficulty
                table._draw_buttons()
                # Display "Sudoku" in the middle of the screen
                sudoku_text = self.message_font.render(
                    "SUDOKU", True, pygame.Color("navyblue")
                )
                sudoku_rect = sudoku_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                self.screen.blit(sudoku_text, sudoku_rect)

            elif table.new_game_button and table.lives == 0:
                # Display the buttons for selecting difficulty
                table._draw_buttons()
                # Display "Sudoku" in the middle of the screen
                sudoku_text = self.message_font.render(
                    "SUDOKU", True, pygame.Color("navyblue")
                )
                sudoku_rect = sudoku_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                self.screen.blit(sudoku_text, sudoku_rect)

            elif table.new_game_button and table._puzzle_solved:
                # Display the buttons for selecting difficulty
                table._draw_buttons()
                # Display "Sudoku" in the middle of the screen
                sudoku_text = self.message_font.render(
                    "SUDOKU", True, pygame.Color("navyblue")
                )
                sudoku_rect = sudoku_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                self.screen.blit(sudoku_text, sudoku_rect)

            pygame.display.flip()
            self.FPS.tick(30)


if __name__ == "__main__":
    play = Main(screen)
    play.main()
