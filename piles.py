import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BG_COLOR = (30, 30, 30)
STONE_COLOR = (200, 50, 50)
HIGHLIGHT_COLOR = (50, 200, 50)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 200)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game of Piles")

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Button dimensions
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
end_button_rect = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - 20, 20, BUTTON_WIDTH, BUTTON_HEIGHT)
restart_button_rect = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - 20, 80, BUTTON_WIDTH, BUTTON_HEIGHT)

# Functions
def reset_game():
    """Reset the game state."""
    global piles, player_turn, winner, last_move, selected_pile
    piles = [random.randint(3, 7) for _ in range(3)]
    player_turn = True
    winner = None
    last_move = None
    selected_pile = None

def draw_piles():
    """Draw the piles of stones on the screen."""
    for i, pile_size in enumerate(piles):
        x = 100 + i * 150
        for j in range(pile_size):
            y = SCREEN_HEIGHT - 100 - j * 35
            pygame.draw.circle(screen, STONE_COLOR, (x, y), 15)

def display_text(text, x, y, font=font, color=TEXT_COLOR):
    """Render and display text."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def calculate_nim_sum():
    """Calculate the XOR sum of all pile sizes."""
    nim_sum = 0
    for pile in piles:
        nim_sum ^= pile
    return nim_sum

def find_optimal_move():
    """Find the optimal move for the AI."""
    nim_sum = calculate_nim_sum()
    if nim_sum == 0:
        # No winning move, play randomly
        non_empty_piles = [i for i, pile in enumerate(piles) if pile > 0]
        pile = random.choice(non_empty_piles)
        stones = random.randint(1, piles[pile])
        return pile, stones

    # Find a pile to adjust to make nim_sum 0
    for i, pile in enumerate(piles):
        target = pile ^ nim_sum
        if target < pile:  # Valid move
            return i, pile - target

def draw_buttons():
    """Draw the End Game and Restart buttons."""
    pygame.draw.rect(screen, BUTTON_COLOR, end_button_rect)
    pygame.draw.rect(screen, BUTTON_COLOR, restart_button_rect)
    display_text("End Game", end_button_rect.x + 20, end_button_rect.y + 10, small_font)
    display_text("Restart", restart_button_rect.x + 20, restart_button_rect.y + 10, small_font)

# Initialize game state
reset_game()

# Game loop
running = True

while running:
    screen.fill(BG_COLOR)

    # Draw piles
    draw_piles()

    # Draw buttons
    draw_buttons()

    # Display player turn or winner
    if winner:
        display_text(f"{winner} Wins!", SCREEN_WIDTH // 2 - 80, 50, font, HIGHLIGHT_COLOR)
    elif player_turn:
        display_text("Your Turn", SCREEN_WIDTH // 2 - 80, 50)
    else:
        display_text("AI's Turn", SCREEN_WIDTH // 2 - 80, 50)

    # Display the last move
    if last_move:
        display_text(f"Last Move: {last_move}", 20, 20, small_font)

    # Display total stones
    total_stones = sum(piles)
    display_text(f"Total Stones: {total_stones}", 20, 60, small_font)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()  # Immediately stop execution after quitting

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if End Game button is clicked
            if end_button_rect.collidepoint(event.pos):
                running = False
                pygame.quit()
                exit()  # Immediately stop execution after quitting

            # Check if Restart button is clicked
            if restart_button_rect.collidepoint(event.pos):
                reset_game()

            if player_turn and not winner:
                # Detect pile selection
                x, y = event.pos
                for i, pile_size in enumerate(piles):
                    pile_x = 100 + i * 150
                    if abs(x - pile_x) < 50 and pile_size > 0:
                        selected_pile = i

        if event.type == pygame.KEYDOWN and player_turn and selected_pile is not None:
            # Detect key press to remove stones (1-9)
            if pygame.K_1 <= event.key <= pygame.K_9:
                stones = event.key - pygame.K_0
                if stones <= piles[selected_pile]:
                    piles[selected_pile] -= stones
                    last_move = f"Player removed {stones} stone(s) from pile {selected_pile}"
                    selected_pile = None
                    player_turn = False

    # AI's turn
    if not player_turn and not winner:
        if any(pile > 0 for pile in piles):  # Check if stones remain
            pygame.time.wait(1000)  # Pause for dramatic effect
            pile, stones = find_optimal_move()
            piles[pile] -= stones
            last_move = f"AI removed {stones} stone(s) from pile {pile}"
            player_turn = True
        else:
            winner = "Player"

    # Check for winner
    if all(pile == 0 for pile in piles):
        winner = "Player" if not player_turn else "AI"

    pygame.display.flip()

pygame.quit()