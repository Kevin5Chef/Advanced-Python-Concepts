import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")
print("SY-5, Kevin Victor, Roll No.-30")
import pygame
import sys
import time
import math

# ------------------------------------------------------------
# INITIALIZATION
# ------------------------------------------------------------
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Vehicle Mini-Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 20)

leaderboard = {
    "Car": None,
    "Bike": None,
    "Truck": None
}

# ------------------------------------------------------------
# VEHICLE CLASS (Polymorphism via default arguments)
# ------------------------------------------------------------
class Vehicle:
    def __init__(self, name, size, weight, aerodynamics, agility, stability):
        self.name = name
        self.size = size
        self.weight = weight
        self.aerodynamics = aerodynamics
        self.agility = agility
        self.stability = stability

        self.reset()

    def reset(self):
        self.x = 60
        self.y = HEIGHT - 60
        self.velocity = 0
        self.angle = -45  # Facing diagonally toward finish
        self.start_time = None

    # Polymorphic methods
    def accelerate(self, power=1.0):
        engine_force = power * (self.aerodynamics / 10) * 0.8
        acceleration = engine_force / self.weight
        self.velocity += acceleration

    def brake(self, intensity=1.0):
        brake_force = intensity * (self.stability / 10) * 0.5
        self.velocity -= brake_force
        if self.velocity < 0:
            self.velocity = 0

    def turn_left(self, sharpness=1.0):
        turn_rate = sharpness * (self.agility / 10) * 4
        self.angle -= turn_rate

    def turn_right(self, sharpness=1.0):
        turn_rate = sharpness * (self.agility / 10) * 4
        self.angle += turn_rate

    def update(self):
        # Aerodynamic drag
        drag = (1 - self.aerodynamics / 10) * 0.015
        self.velocity *= (1 - drag)

        # Movement
        rad = math.radians(self.angle)
        self.x += self.velocity * math.cos(rad)
        self.y += self.velocity * math.sin(rad)

        # Boundary collision
        if self.x < 0:
            self.x = 0
            self.velocity *= 0.5
        if self.x > WIDTH:
            self.x = WIDTH
            self.velocity *= 0.5
        if self.y < 0:
            self.y = 0
            self.velocity *= 0.5
        if self.y > HEIGHT:
            self.y = HEIGHT
            self.velocity *= 0.5

    def draw(self):
        rect = pygame.Rect(0, 0, self.size * 10, self.size * 5)
        rect.center = (self.x, self.y)

        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (220, 50, 50), (0, 0, rect.width, rect.height), border_radius=5)

        rotated = pygame.transform.rotate(surface, -self.angle)
        new_rect = rotated.get_rect(center=rect.center)
        screen.blit(rotated, new_rect.topleft)


# ------------------------------------------------------------
# VEHICLE DEFINITIONS
# ------------------------------------------------------------
car = Vehicle("Car", size=6, weight=6, aerodynamics=7, agility=6, stability=7)
bike = Vehicle("Bike", size=4, weight=3, aerodynamics=8, agility=9, stability=4)
truck = Vehicle("Truck", size=8, weight=9, aerodynamics=4, agility=3, stability=9)

vehicles = {
    "1": car,
    "2": bike,
    "3": truck
}

# ------------------------------------------------------------
# GAME FUNCTION
# ------------------------------------------------------------
def run_game(vehicle):
    vehicle.reset()
    vehicle.start_time = time.time()

    finish_x = WIDTH - 60
    finish_y = 60
    running = True

    while running:
        clock.tick(FPS)
        screen.fill((25, 25, 25))

        # Draw boundary
        pygame.draw.rect(screen, (80, 80, 80), (0, 0, WIDTH, HEIGHT), 4)

        # Draw finish zone
        pygame.draw.circle(screen, (0, 200, 0), (finish_x, finish_y), 35)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            vehicle.accelerate()
        if keys[pygame.K_DOWN]:
            vehicle.brake()
        if keys[pygame.K_LEFT]:
            vehicle.turn_left()
        if keys[pygame.K_RIGHT]:
            vehicle.turn_right()

        vehicle.update()
        vehicle.draw()

        # Finish check
        distance = math.hypot(vehicle.x - finish_x, vehicle.y - finish_y)
        if distance < 35:
            end_time = time.time()
            total_time = round(end_time - vehicle.start_time, 2)

            if leaderboard[vehicle.name] is None or total_time < leaderboard[vehicle.name]:
                leaderboard[vehicle.name] = total_time

            show_results(vehicle.name, total_time)
            running = False

        pygame.display.flip()


# ------------------------------------------------------------
# RESULTS SCREEN
# ------------------------------------------------------------
def show_results(vehicle_name, time_taken):
    showing = True
    while showing:
        screen.fill((20, 20, 20))

        title = font.render(f"{vehicle_name} Finished in {time_taken} seconds", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        y_offset = 200
        for name, time_value in leaderboard.items():
            text = f"{name}: {time_value if time_value else 'No Record'}"
            line = font.render(text, True, (200, 200, 200))
            screen.blit(line, (WIDTH // 2 - line.get_width() // 2, y_offset))
            y_offset += 40

        info = font.render("Press ENTER to return to menu", True, (180, 180, 180))
        screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    showing = False

        pygame.display.flip()


# ------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------
def main_menu():
    while True:
        print("\n===== VEHICLE MINI GAME =====")
        print("1. Play as Car")
        print("2. Play as Bike")
        print("3. Play as Truck")
        print("4. Exit")

        choice = input("Select vehicle: ")

        if choice in vehicles:
            run_game(vehicles[choice])
        elif choice == "4":
            pygame.quit()
            sys.exit()
        else:
            print("Invalid choice.")


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------
if __name__ == "__main__":
    main_menu()
