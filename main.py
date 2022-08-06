from sense_hat import SenseHat
import time
from random import seed
from random import randint
import collect_data
import datetime

#Initialize SenseHat.
s = SenseHat()
s.low_light = True

collect_data.sense = s

# Defining colors
red = (255, 0, 0)
green = (0, 255, 0)
orange = (255, 140, 0)
none = (0, 0, 0)


# Snake code inspired by https://pythonspot.com/snake-with-pygame/

# Snake's food.
class Apple:
    # Apple's coordinates.
    x = 0
    y = 0

    # Initialization.
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Drawing pixel on the screen with colour as an argument.
    def draw(self, colour):
        s.set_pixel(self.x, self.y, colour)


# Snake controlled by computer.
class ComputerPlayer:
    # Initialize x and y arrays that will store position of every point of our
    # Snake.
    x = []
    y = []

    # Define points of Hamiltonian cycle that our snake will follow.
    destinations = [(7, 1),
        (1, 2),
        (7, 3),
        (1, 4),
        (7, 5),
        (1, 6),
        (7, 7),
        (0, 0),]

    # Direction our snake is facing.
    _dir = 0

    # Default length of our snake, also variable that stores it's length.
    length = 5

    # Max frames before updating snake's position.
    updateCountMax = 2

    # Frames since last position update.
    updateCount = 0

    # Constructor method.
    def __init__(self, length):
        # Set length from argument.
        self.length = length

        # Add dummy fragments.
        for i in range(0, 68):
            self.x.append(0)
            self.y.append(0)

        # Set starting positions for snake to make sure it won't get stuck.
        self.x[1] = 1
        self.x[2] = 2

    # Update method (it's fired every frame).
    def update(self):

        # Add one to "updateCount" every frame.
        self.updateCount += 1
        # If "updateCount" is greater than "updateCountMax", it's time to
        # update our snake.
        if self.updateCount > self.updateCountMax:
            # Move every point of our snake towards the head.
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            # If "_dir" is equal to 0, move right.
            if self._dir == 0:
                self.x[0] += 1

            # If "_dir" is equal to 1, move left.
            if self._dir == 1:
                self.x[0] -= 1

            # If "_dir" is equal to 2, move up.
            if self._dir == 2:
                self.y[0] -= 1

            # If "_dir" is equal to 3, move down.
            if self._dir == 3:
                self.y[0] += 1

            # Set "updateCount" back to 0.
            self.updateCount = 0

    # Moving right method.
    def moveR(self):
        self._dir = 0
    
    # Moving left method.
    def moveL(self):
        self._dir = 1

    # Moving up method.
    def moveU(self):
        self._dir = 2

    # Moving down method.
    def moveD(self):
        self._dir = 3

    # Draw snake with colour "colour".
    def draw(self, colour):
        for i in range(0, self.length - 1):
            s.set_pixel(self.x[i], self.y[i], colour)

    # Simple computer controlled movement.
    def target(self, destinationX, destinationY):
        # If snake's x is greater than destination's x -> move snake to the
        # left.
        if self.x[0] > destinationX:
            self.moveL()
        
        # If snake's x is lesser than destination's x -> move snake to the
        # right.
        if self.x[0] < destinationX:
            self.moveR()

        # If snake's x is equal check for if y is greater or lesser than
        # destination's y.
        if self.x[0] == destinationX:
        
            # If snake's y is greater than destination's y -> move snake up
            if self.y[0] > destinationY:
                self.moveU()
                
            # If snake's y is lesser than destination's x -> move snake down
            if self.y[0] < destinationY:
                self.moveD()

# Snake's core class.
class Core:
    # Collision checking function.
    def isCollision(self, x1, y1, x2, y2, bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False

# Main snake game class.
class Snake:
    # Initialize variables: player instance, apple instance, destination index
    # -> i.
    player = 0
    apple = 0
    i = 0

    # Initialization method.
    def __init__(self):
        # Snake is running.
        self._running = True
        # Create instance of "ComputerPlayer".
        self.player = ComputerPlayer(3)
        # Create instance of "Apple".
        self.apple = Apple(5, 5)
        # Create instance of "Core" class.
        self.core = Core()
        # Clear Pi's screen.
        s.clear()

    # Loop method (it's fired every frame).
    def on_loop(self):
        
        # Set target for computer player.
        self.player.target(self.player.destinations[self.i % 8][0],
            self.player.destinations[self.i % 8][1],)
        # If snake collides with its destination - change destination.
        if Core.isCollision(self,
            self.player.x[0],
            self.player.y[0],
            self.player.destinations[self.i % 8][0],
            self.player.destinations[self.i % 8][1],
            0.1,):
            self.i += 1
        # Call update method.
        self.player.update()
        # if any segment of our snake collides with apple, create new apple and
        # make our snake longer.
        for i in range(0, self.player.length):
            if self.core.isCollision(self.apple.x,
                self.apple.y,
                self.player.x[i],
                self.player.y[i],
                0.1,):
                # "Create" new apple.
                self.apple.x = randint(0, 7)
                self.apple.y = randint(0, 7)

                # We need to make sure that the apple won't spawn inside the
                # snake.
                # We make a list containing player's x and y location
                snake_body = list(zip(self.player.x, self.player.y))
                # We change apple's x and y values untill they are not in the
                # body of our snake.
                while (self.apple.x, self.apple.y) in snake_body:
                    self.apple.x = randint(0, 7)
                    self.apple.y = randint(0, 7)
                # Make our snake longer.
                self.player.length += 1
        # Check if snake has got its maximum length.
        if self.player.length >= 63:
            # Turn off snake game.
            self._running = False
        # Clear Pi's screen.
        s.clear()
        pass
    
    # Rendering method
    def on_render(self):
        # Draw snake on screen.
        self.player.draw(red)
        # Draw apple on screen.
        self.apple.draw(green)

    # First method fired when running snake.
    def on_execute(self):
        # Get time and save it to variable.
        starting_time = datetime.datetime.now()
        local_time = datetime.datetime.now()
        # Run while we are not saving data.
        while (local_time <= starting_time + datetime.timedelta(seconds=30 - 30 / 1000)) and self._running is True:
            # Fire methods "on_loop", "on_render".
            self.on_loop()
            self.on_render()
            
            # Stop snake after every step.
            time.sleep(30 / 1000.0)
            
            # Save time after every step.
            local_time = datetime.datetime.now()

# Changing modes
mode = 0
modes = 2

# Save time to variable.
global_starting_time = datetime.datetime.now()
global_time = datetime.datetime.now()
# Run our program while "global_time" is less than 180 minutes.
while global_time < global_starting_time + datetime.timedelta(minutes=179.5):
    # Run data collecting functions.
    collect_data.magnetometer()
    collect_data.location()
    collect_data.calculate()
    # Save data to file.
    collect_data.save()

    # Self-promote our team for 30 seconds.
    if mode % modes == 0:
        # This message is 39 pixels long so this should take around 10 seconds
        s.show_message("Foxes", 10 / 39, orange)
        # Show our logo for 20 seconds.
        s.load_image("FoxLogo.png")
        time.sleep(20)
        
    # Show snake for 30 seconds.
    if mode % modes == 1:
        # Create instance of snake.
        snake = Snake()
        # Execute snake game.
        snake.on_execute()

    # Save time after every cycle.
    global_time = datetime.datetime.now()

    # Change Mode
    mode += 1
