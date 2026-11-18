import turtle, colorsys, math, random

"""
Static values to configure the drawing
"""
SEED: int = 1  # Define the seed of the drawing.
TILTING: float = 0.5  # Define the angle of rotation of the galaxy (WARNING: the angle is in radians)
SCREEN_WIDTH: int = 1080
SCREEN_HEIGHT: int = 720
SCREEN_TITLE: str = "Galaxy"

CLOCKWISE: bool = False  # Direction the arms curl in as they go outward
ARM_WINDING: float = 5.5  # How much each arm curls between its start and its tip (in radians)
ARM_START_RADIUS: float = 10  # Distance from the center where the arms start
ARM_END_RADIUS: float = 300  # Distance from the center where the arms end
STAR_HUES: list = [0.6, 0.55, 0.14, 0.08, 0.02]  # Background star colors: blue, blue-white, yellow, orange, red

random.seed(SEED)  # Same seed = same galaxy on every run

"""
Turtle setup
"""
screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)  # Set the window size
screen.title(SCREEN_TITLE)  # Set the window title
screen.tracer(30)  # Refresh the window every 30 actions
screen.bgcolor("#03030b")  # Set the background color of the window

t = turtle.Turtle()
t.hideturtle()  # Hides the turtle
t.speed(0)  # Set the speed to the fastest one
t.penup()  # Draw only dots, not lines


def glow(h: float, v: float = 1.0, s: float = 0.7) -> tuple:
    """Color helper function: converts HSV to RGB"""
    return colorsys.hsv_to_rgb(h % 1, s, v)


def place(x, y) -> None:
    """Place turtle at position x, y"""
    y *= 0.55
    cos = math.cos(TILTING)
    sin = math.sin(TILTING)
    t.goto(x * cos - y * sin, x * sin + y * cos)


def stars(quantity: int) -> None:
    for _ in range(quantity):
        x = random.randint(int(-SCREEN_WIDTH / 2), int(SCREEN_WIDTH / 2))
        y = random.randint(int(-SCREEN_HEIGHT / 2), int(SCREEN_HEIGHT / 2))
        t.goto(x, y)
        # Low saturation keeps the stars pale, like real ones: only a hint of colour
        color = glow(random.choice(STAR_HUES), random.uniform(0.7, 1), random.uniform(0.1, 0.45))
        t.dot(random.randint(1, 3), color)


def cloud(quantity: int, spread: float, size_min: int, size_max: int, color) -> None:
    """Scatter dots around the centre, denser in the middle and fading out (used for dust, core and sparkles)"""
    for _ in range(quantity):
        r = random.gauss(0, spread)
        a = random.uniform(0, math.tau)
        place(r * math.cos(a), r * math.sin(a))
        t.dot(random.randint(size_min, size_max), color)


def arms(quantity: int, arms_nb: int) -> None:
    direction = -1 if CLOCKWISE else 1
    growth = math.log(ARM_END_RADIUS / ARM_START_RADIUS)
    for i in range(quantity):
        for k in range(arms_nb):
            d = i / quantity
            # Logarithmic spiral: the angle grows with log(r), so arms curl tightly near the core and open up outside
            r = ARM_START_RADIUS + d * (ARM_END_RADIUS - ARM_START_RADIUS)
            a = k * math.tau / arms_nb + direction * ARM_WINDING * math.log(r / ARM_START_RADIUS) / growth
            s = 4 + d * 26
            x = r * math.cos(a) + random.gauss(0, s)
            y = r * math.sin(a) + random.gauss(0, s)
            place(x, y)
            hue = 0.13 - d * 0.55
            v = random.uniform(0.6, 1)
            size = random.randint(2, 4)
            t.dot(size, glow(hue, v))


def draw(stars_qtt: int, dust_qtt: int, arms_qtt: int, arms_nb: int, core_qtt: int, sparkle_qtt: int) -> None:
    stars(stars_qtt)
    cloud(dust_qtt, 120, 2, 4, glow(0.7, 0.3))  # Dust: faint blue-violet halo
    arms(arms_qtt, arms_nb)
    cloud(core_qtt, 26, 2, 5, glow(0.12))  # Core: dense bright gold bulge
    cloud(sparkle_qtt, 150, 5, 8, "white")  # Sparkles: big white foreground stars
    t.goto(0, 0)
    t.dot(26, "#fff3c4")
    screen.update()
    turtle.done()


draw(140, 700, 500, 5, 260, 40)
