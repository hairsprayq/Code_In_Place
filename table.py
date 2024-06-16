# table.py
import pygame
from cell import Cell
from sudoku import Sudoku
from clock import Clock
import pygame.time
import math
import sys

from settings import WIDTH, HEIGHT, N_CELLS, CELL_SIZE

pygame.font.init()

class Table:
    def __init__(self, screen):
        self.screen = screen
        self.sudoku = None
        self.clock = Clock()
        self.SRN = int(math.sqrt(N_CELLS))
        self.table_cells = []
        self.num_choices = []
        self.clicked_cell = None
        self.clicked_num_below = None
        self.cell_to_empty = None
        self.making_move = False
        self.guess_mode = True
        self.lives = 3
        self.game_over = False
        self.new_game_button = None  # Initialize as None
        self.delete_button = pygame.Rect(
            0, HEIGHT + CELL_SIZE[1], CELL_SIZE[0] * 3, CELL_SIZE[1]
        )
        self.guess_button = pygame.Rect(
            CELL_SIZE[0] * 6, HEIGHT + CELL_SIZE[1], CELL_SIZE[0] * 3, CELL_SIZE[1]
        )
        self.font = pygame.font.SysFont("googlesans", CELL_SIZE[0] // 2)
        self.font_color = pygame.Color("white")
        self.last_clicked_cell = None
        self.incorrect_guesses = []
        self.remove_incorrect_guess_timer = None
        self.difficulty = None
        self._create_new_game_button()
        self._generate_game()
        self.game_over_display_timer = None  # Timer for game over message

    def _create_new_game_button(self):
        self.new_game_button = pygame.Rect(
            WIDTH // 2 - CELL_SIZE[0] * 2,
            HEIGHT + CELL_SIZE[1] * 2,
            CELL_SIZE[0] * 4,
            CELL_SIZE[1],
        )

    def _delete_new_game_button(self):
        self.new_game_button = None

    def _generate_game(self):
        self.table_cells = []
        if self.sudoku:
            self.answers = self.sudoku.puzzle_answers()
            self.answerable_table = self.sudoku.puzzle_table()
            for y in range(N_CELLS):
                for x in range(N_CELLS):
                    cell_value = self.answerable_table[y][x]
                    is_correct_guess = True if cell_value != 0 else False
                    self.table_cells.append(
                        Cell(x, y, CELL_SIZE, cell_value, is_correct_guess)
                    )
            self.lives = 3
            self.game_over = False
            # Automatically select the middle cell when the game is initialized
            middle_row = N_CELLS // 2
            middle_col = N_CELLS // 2
            self.clicked_cell = self._get_cell_from_pos((middle_row, middle_col))
            if self.clicked_cell:
                self.clicked_cell.toggle_color()
                self.last_clicked_cell = self.clicked_cell

    def _draw_grid(self):
        grid_color = (50, 80, 80)
        pygame.draw.rect(self.screen, grid_color, (-3, -3, WIDTH + 6, HEIGHT + 6), 6)
        i = 1
        while i * CELL_SIZE[0] < WIDTH:
            line_size = 2 if i % 3 > 0 else 4
            pygame.draw.line(
                self.screen,
                grid_color,
                ((i * CELL_SIZE[0]) - (line_size // 2), 0),
                ((i * CELL_SIZE[0]) - (line_size // 2), HEIGHT),
                line_size,
            )
            pygame.draw.line(
                self.screen,
                grid_color,
                (0, (i * CELL_SIZE[0]) - (line_size // 2)),
                (HEIGHT, (i * CELL_SIZE[0]) - (line_size // 2)),
                line_size,
            )
            i += 1

    def _draw_buttons(self):
        if self.difficulty and not self.game_over:
            # Draw the delete button
            dl_button_color = pygame.Color("indianred2")
            pygame.draw.rect(self.screen, dl_button_color, self.delete_button)
            del_msg = self.font.render("Delete", True, self.font_color)
            del_rect = del_msg.get_rect(center=self.delete_button.center)
            self.screen.blit(del_msg, del_rect)

            # Draw the guess button
            gss_button_color = (
                pygame.Color("cadetblue3") if self.guess_mode else pygame.Color("lightpink2")
            )
            pygame.draw.rect(self.screen, gss_button_color, self.guess_button)
            gss_msg = self.font.render(
                "Guess: On" if self.guess_mode else "Guess: Off", True, self.font_color
            )
            gss_rect = gss_msg.get_rect(center=self.guess_button.center)
            self.screen.blit(gss_msg, gss_rect)

        # New Game button
        if self.new_game_button:
            new_game_button_color = pygame.Color("palegreen3")
            pygame.draw.rect(self.screen, new_game_button_color, self.new_game_button)
            new_game_msg = self.font.render("New Game", True, self.font_color)
            new_game_rect = new_game_msg.get_rect(center=self.new_game_button.center)
            self.screen.blit(new_game_msg, new_game_rect)

    def _select_difficulty(self):
        running = True
        while running:
            self.screen.fill("lavender")
            easy_button = pygame.Rect(
                WIDTH // 2 - CELL_SIZE[0] * 2,
                HEIGHT // 2 - CELL_SIZE[1] * 2,
                CELL_SIZE[0] * 4,
                CELL_SIZE[1],
            )
            medium_button = pygame.Rect(
                WIDTH // 2 - CELL_SIZE[0] * 2,
                HEIGHT // 2,
                CELL_SIZE[0] * 4,
                CELL_SIZE[1],
            )
            hard_button = pygame.Rect(
                WIDTH // 2 - CELL_SIZE[0] * 2,
                HEIGHT // 2 + CELL_SIZE[1] * 2,
                CELL_SIZE[0] * 4,
                CELL_SIZE[1],
            )

            pygame.draw.rect(self.screen, pygame.Color("seagreen1"), easy_button)
            pygame.draw.rect(self.screen, pygame.Color("lightgoldenrod2"), medium_button)
            pygame.draw.rect(self.screen, pygame.Color("indianred2"), hard_button)

            easy_msg = self.font.render("Easy", True, self.font_color)
            easy_rect = easy_msg.get_rect(center=easy_button.center)
            self.screen.blit(easy_msg, easy_rect)

            medium_msg = self.font.render("Medium", True, self.font_color)
            medium_rect = medium_msg.get_rect(center=medium_button.center)
            self.screen.blit(medium_msg, medium_rect)

            hard_msg = self.font.render("Hard", True, self.font_color)
            hard_rect = hard_msg.get_rect(center=hard_button.center)
            self.screen.blit(hard_msg, hard_rect)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if easy_button.collidepoint(x, y):
                        self.difficulty = "easy"
                        running = False
                    elif medium_button.collidepoint(x, y):
                        self.difficulty = "medium"
                        running = False
                    elif hard_button.collidepoint(x, y):
                        self.difficulty = "hard"
                        running = False

        self.sudoku = Sudoku(N_CELLS, self.difficulty)
        self._generate_game()
        self._delete_new_game_button()
        self.clock.start_timer()

    def _get_cell_from_pos(self, pos):
        for cell in self.table_cells:
            if (cell.row, cell.col) == (pos[0], pos[1]):
                return cell

        # checking rows, cols, and subgroups for adding guesses on each cell

    def _not_in_row(self, row, num):
        for cell in self.table_cells:
            if cell.row == row:
                if cell.value == num:
                    return False
        return True

    def _not_in_col(self, col, num):
        for cell in self.table_cells:
            if cell.col == col:
                if cell.value == num:
                    return False
        return True

    def _not_in_subgroup(self, rowstart, colstart, num):
        for x in range(self.SRN):
            for y in range(self.SRN):
                current_cell = self._get_cell_from_pos((rowstart + x, colstart + y))
                if current_cell.value == num:
                    return False
        return True

    # remove numbers in guess if number already guessed in the same row, col, subgroup correctly
    def _remove_guessed_num(self, row, col, rowstart, colstart, num):
        for cell in self.table_cells:
            if cell.row == row and cell.guesses != None:
                for x_idx, guess_row_val in enumerate(cell.guesses):
                    if guess_row_val == num:
                        cell.guesses[x_idx] = 0
            if cell.col == col and cell.guesses != None:
                for y_idx, guess_col_val in enumerate(cell.guesses):
                    if guess_col_val == num:
                        cell.guesses[y_idx] = 0
        for x in range(self.SRN):
            for y in range(self.SRN):
                current_cell = self._get_cell_from_pos((rowstart + x, colstart + y))
                if current_cell.guesses != None:
                    for idx, guess_val in enumerate(current_cell.guesses):
                        if guess_val == num:
                            current_cell.guesses[idx] = 0

    def handle_mouse_click(self, pos):
        x, y = pos
        # getting table cell clicked
        # Check if the delete button was clicked
        if self.delete_button.collidepoint(x, y):
            if self.clicked_cell:
                # Clear the cell value if it's not in guess mode or if it's incorrect
                if not self.guess_mode or (
                    self.clicked_cell
                    and self.clicked_cell.value != 0
                    and not self.clicked_cell.is_correct_guess
                ):
                    self.clicked_cell.value = 0

                # Clear all guessed numbers in the cell
                if self.clicked_cell.guesses is not None:
                    self.clicked_cell.guesses = [0 for _ in range(9)]

                # Remove incorrect guesses from the tracking list
                if self.clicked_cell in self.incorrect_guesses:
                    self.incorrect_guesses.remove(self.clicked_cell)

        # Check if the guess button was clicked
        elif self.guess_button.collidepoint(x, y):
            # Toggle guess mode
            self._toggle_guess_mode()

        # Check if the new game button exists and was clicked
        elif self.new_game_button and self.new_game_button.collidepoint(x, y):
            self._select_difficulty()

        else:
            # Process cell selection and toggling as before
            # getting table cell clicked
            if x <= WIDTH and y <= HEIGHT:
                x = x // CELL_SIZE[0]
                y = y // CELL_SIZE[1]
                clicked_cell = self._get_cell_from_pos((x, y))
                self._select_cell(clicked_cell)

                # Toggle the color of the clicked cell
                if clicked_cell:
                    if self.last_clicked_cell:
                        self.last_clicked_cell.color = (
                            self.last_clicked_cell.default_color
                        )
                    # Toggle the color of the clicked cell
                    clicked_cell.toggle_color()

                    # Update the last clicked cell
                    self.last_clicked_cell = clicked_cell

                # if clicked empty cell
                if clicked_cell and clicked_cell.value == 0:
                    self.clicked_cell = clicked_cell
                    self.making_move = True
                # clicked unempty cell but with wrong number guess
                elif (
                    clicked_cell
                    and clicked_cell.value != 0
                    and clicked_cell.value != self.answers[y][x]
                ):
                    self.cell_to_empty = clicked_cell

    def handle_keyboard_input(self, event):

        if event.key in [
            pygame.K_KP1,
            pygame.K_KP2,
            pygame.K_KP3,
            pygame.K_KP4,
            pygame.K_KP5,
            pygame.K_KP6,
            pygame.K_KP7,
            pygame.K_KP8,
            pygame.K_KP9,
        ]:
            number = int(event.unicode)  # Extract number from unicode
            self._handle_number_input(number)
        else:
            # Handling input from the main keyboard
            if event.key == pygame.K_1:
                self._handle_number_input(1)
            elif event.key == pygame.K_2:
                self._handle_number_input(2)
            elif event.key == pygame.K_3:
                self._handle_number_input(3)
            elif event.key == pygame.K_4:
                self._handle_number_input(4)
            elif event.key == pygame.K_5:
                self._handle_number_input(5)
            elif event.key == pygame.K_6:
                self._handle_number_input(6)
            elif event.key == pygame.K_7:
                self._handle_number_input(7)
            elif event.key == pygame.K_8:
                self._handle_number_input(8)
            elif event.key == pygame.K_9:
                self._handle_number_input(9)
            elif event.key == pygame.K_BACKSPACE:
                self._handle_backspace()
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self._toggle_guess_mode()
            # Add handling for arrow keys
            elif event.key == pygame.K_LEFT:
                self._move_selected_cell(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self._move_selected_cell(1, 0)
            elif event.key == pygame.K_UP:
                self._move_selected_cell(0, -1)
            elif event.key == pygame.K_DOWN:
                self._move_selected_cell(0, 1)

    def _select_cell(self, cell):
        if cell:
            if self.last_clicked_cell:
                self.last_clicked_cell.toggle_color()  # Deselect the previously selected cell
            cell.toggle_color()  # Select the new cell
            self.last_clicked_cell = cell
            self.clicked_cell = cell

    # Modify _move_selected_cell method to handle both keyboard and mouse selections
    def _move_selected_cell(self, dx, dy):
        if self.clicked_cell:
            new_x = self.clicked_cell.row + dx
            new_y = self.clicked_cell.col + dy
            # Ensure the new coordinates are within bounds
            if 0 <= new_x < N_CELLS and 0 <= new_y < N_CELLS:
                new_cell = self._get_cell_from_pos((new_x, new_y))
                self._select_cell(new_cell)

    def _handle_number_input(self, number):
        if self.clicked_cell and self.clicked_cell.value == 0:
            if self.guess_mode:
                self._handle_guess_input(number)
            else:
                self._handle_regular_input(number)

    def _handle_guess_input(self, number):
        current_row = self.clicked_cell.row
        current_col = self.clicked_cell.col
        rowstart = current_row - current_row % self.SRN
        colstart = current_col - current_col % self.SRN
        if (
            self._not_in_row(current_row, number)
            and self._not_in_col(current_col, number)
            and self._not_in_subgroup(rowstart, colstart, number)
        ):
            if self.clicked_cell.guesses is not None:
                self.clicked_cell.guesses[number - 1] = number

    def _handle_regular_input(self, number):
        if self.clicked_cell:
            self.clicked_cell.value = number
            if (
                self.clicked_cell.value
                != self.answers[self.clicked_cell.col][self.clicked_cell.row]
            ):
                self.clicked_cell.is_correct_guess = False
                self.clicked_cell.guesses = [0 for _ in range(9)]
                self.lives -= 1
                # Add incorrect guess to the tracking list
                self.incorrect_guesses.append(self.clicked_cell)
                # Start a timer to remove the incorrect guess after a delay
                self.remove_incorrect_guess_timer = (
                    pygame.time.get_ticks() + 2000
                )  # Set the timer for 2 seconds (2000 milliseconds)
            else:
                self.clicked_cell.is_correct_guess = True
                self.clicked_cell.guesses = None

    def _handle_backspace(self):
        if self.clicked_cell:
            # Clear the cell value if it's not in guess mode or if it's incorrect
            if not self.guess_mode or (
                self.clicked_cell.value != 0 and not self.clicked_cell.is_correct_guess
            ):
                self.clicked_cell.value = 0

            # Clear all guessed numbers in the cell
            if self.clicked_cell.guesses is not None:
                self.clicked_cell.guesses = [0 for _ in range(9)]
            # Remove incorrect guesses from the tracking list
            if self.clicked_cell in self.incorrect_guesses:
                self.incorrect_guesses.remove(self.clicked_cell)

    def _toggle_guess_mode(self):
        self.guess_mode = not self.guess_mode

    def _puzzle_solved(self):
        check = None
        for cell in self.table_cells:
            if cell.value == self.answers[cell.col][cell.row]:
                check = True
            else:
                check = False
                break
        return check

    def update(self):
        [cell.update(self.screen, self.SRN) for cell in self.table_cells]
        self._draw_grid()
        self._draw_buttons()
        if self._puzzle_solved() or self.lives == 0:
            self.clock.stop_timer()
            self.game_over = True
            if self.game_over_display_timer is None:
                self.game_over_display_timer = pygame.time.get_ticks()
        else:
            self.clock.update_timer()
        # Remove incorrect guesses if the timer has elapsed
        if (
            self.remove_incorrect_guess_timer
            and pygame.time.get_ticks() >= self.remove_incorrect_guess_timer
        ):
            for cell in self.incorrect_guesses:
                cell.value = 0  # Delete the incorrect guess
            self.incorrect_guesses.clear()  # Clear the list of incorrect guesses
            self.remove_incorrect_guess_timer = None  # Reset the timer

        self.screen.blit(
            self.clock.display_timer(), (WIDTH // self.SRN, HEIGHT + CELL_SIZE[1])
        )

    def update2(self):
        current_time = pygame.time.get_ticks()
        if (
            self.game_over_display_timer
            and current_time >= self.game_over_display_timer + 5000
        ):
            self._create_new_game_button()
            self.game_over_display_timer = None  # Reset the timer
