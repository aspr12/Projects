from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#800080"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self, canvas):
        """Initialize the snake with body parts and draw it on the canvas."""
        self.body_size = BODY_PARTS
        self.coordinates = [[0, 0]] * BODY_PARTS
        self.squares = []

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        """Initialize the food at a random position on the canvas."""
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

class SnakeGame:

    def __init__(self, window):
        """Initialize the game with a window and set up the canvas, score, and key bindings."""
        self.window = window
        self.window.title("Snake Game")
        self.window.resizable(False, False)

        self.score = 0
        self.direction = 'down'

        self.label = Label(window, text=f"Score: {self.score}", font=('consolas', 40))
        self.label.pack()

        self.canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        self.window.update()

        window_width = window.winfo_width()
        window_height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)

        self.window.bind('<Left>', self.change_direction)
        self.window.bind('<Right>', self.change_direction)
        self.window.bind('<Up>', self.change_direction)
        self.window.bind('<Down>', self.change_direction)

        self.next_turn()

    def next_turn(self):
        """Move the snake, check for collisions and food consumption, and schedule the next turn."""
        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        self.snake.coordinates.insert(0, [x, y])

        square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        self.snake.squares.insert(0, square)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            self.canvas.delete("food")
            self.food = Food(self.canvas)
        else:
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(SPEED, self.next_turn)

    def change_direction(self, event):
        """Change the direction of the snake based on key press events."""
        new_direction = event.keysym.lower()
        if new_direction in ['left', 'right', 'up', 'down']:
            opposite_directions = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
            if new_direction != opposite_directions[self.direction]:
                self.direction = new_direction

    def check_collisions(self):
        """Check if the snake has collided with the walls or itself."""
        x, y = self.snake.coordinates[0]

        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True

        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def game_over(self):
        """Display game over message and create a restart button."""
        self.canvas.delete(ALL)
        self.canvas.create_text(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
        restart_button = Button(self.window, text="Restart", font=('consolas', 20), command=self.restart_game)
        restart_button.pack()

    def restart_game(self):
        """Restart the game by resetting score, direction, and creating new snake and food."""
        self.score = 0
        self.direction = 'down'
        self.label.config(text=f"Score: {self.score}")
        self.canvas.delete("all")
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)
        self.next_turn()


if __name__ == "__main__":
    window = Tk()
    game = SnakeGame(window)
    window.mainloop()
