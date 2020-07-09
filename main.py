# THe command pattern enables the recording and playback,
# of a series of commands.
# It can be used to help tests be created that pass without error,
# even before the tru implementation has begun.
# Then they can used in the real implementation to keep
# coupling loose.

# Initial Requirements
# Create a game board on which tokens can be placed,
# and removed.

# Hypothetical use case.
# Create an 8x8 board
# Place a token
# Verify its placement
# Remove a token
# Verify its removal.

# We can start by calling simple functions that can later hide
# the changing implementations details.

# b = Board(8, 8)

# we could call a class like this, but it makes some assumptions,
# about the implementaion being class and method based.


# IMPLEMENTATION CLASSES

class Token:
    def __init__(self, value):
        self.value = value


class Position:
    def __init__(self, x, y, token):
        self.x = x
        self.y = y
        self.token = token


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.positions = {}

    def __str__(self):
        output = ""
        for row in range(self.height):
            for column in range(self.width):
                if (column,row) in self.positions:
                    output += self.positions[(column,row)].value + " "
                else:
                    output+= ". "
            output += "\n\n"
        return output

    def get_token(self, x, y):
        for position in self.positions:
            if x == position[0] and y == position[1]:
                return self.positions[(x, y)].value
        return None

    def remove_token(self, x, y):
        for position in self.positions:
            if x == position[0] and y == position[1]:
                del self.positions[(x, y)]
                break

    def place_token(self, x, y, symbol: str):
        t = Token(symbol)
        self.positions[(x, y)] = t


# BASE CLASSES FOR COMMAND PATTERN


class Action:  # Action is a Synonymn for Command
    def __init__(self, name: str, payload: dict):
        self.name = name
        self.payload = payload


class App:
    def __init__(self):
        self.commands: {str: function} = {
            "create_board": self.create_board,
            "place_token": self.place_token,
            "get_token": self.get_token,
            "remove_token": self.remove_token,
        }

    def execute(self, action: Action):
        if action.name not in self.commands:
            return
        return self.commands[action.name](action.payload)

    def create_board(self, options: dict):
        self.board = Board(options['x'], options['y'])
        return self.board

    def place_token(self, options: dict):
        return self.board.place_token(options['x'], options['y'], options['symbol'])

    def get_token(self, options: dict):
        return self.board.get_token(options['x'], options['y'])

    def remove_token(self, options: dict):
        return self.board.remove_token(options['x'], options['y'])


app = App()

# We can see now that if we had envisioned the command pattern at the beginning
# We would not need the adapter functions to maintain a stable set of tests.
# this is the sort of revolutionary redesign where it may be worth it to update
# the tests, but do note that it is *not* required.

test_options = {
    "x": 3,
    "y": 3,
    "symbol": "X"
}

test_commands = [
    ["create_board", {"x": 8, "y": 8}],
    ["place_token", test_options],
    ["get_token", test_options, "X"],  # EXPECTED RESULT
    ["remove_token", test_options],
    ["get_token", test_options, None],  # EXPECTED RESULT
]
for c in test_commands:
    result = app.execute(Action(c[0], c[1]))
    print(str(app.board))
    if len(c) == 3:
        assert result == c[2]

# This is better and we can keep the interface to this simple
# function stable while the implementation evolves through
# refactoring.

# Here again we use a wrapper function that can remain stable.
# we pass the board object in as we cannot assume the kind of
# shared properties we would expect if we were committed to a
# design that used classes.

# OK thats enough tests to begin coding.
# Note that we have many syntax errors at this stage also,
# Calling unwritten functions causes this, and it is to be
# expected.
# Using these test helper functions allows us to make these simple
# tests stop erroring right away, before any ideal solution
# is even thought about.

# Yay! all tests are passing.
# Now we can refactor.
# A simple refactoring is to use a class for the shared data.
# While it might be tempting to change the signature of the
# test functions that have made the test go green
# they are an adapter from the tests to the real solution
# if they change then we would need to change the tests.
# changing the tests should be avoided if possible.

# tests are expected to fail during refactoring
# we will watch them pass one by one again as we complete the refactor.

# Lets see if we can do another refactoring.
# Can we abstract the position tuple into a class?

# Alright, thats quit a bit of refactoring, we could experiment with
# various ideas all day and night. All safely because we are protected by TDD
# Tests never changed due to using adapter functions with constant signatures.

# OK next we will fit this to a traditional command pattern
# to do this we will need to have a central App that commands are sent to and
# a command object that will execute the commands.

# OK so far we have not changed our adapter functions but lets do so to prove
# we would not need them if we had planned on the command pattern for
# decoupling from the start.

# Since we bit the bullet and decided to refactor our tests,
# Lets keep going.

# While I do not recommend testing UI output you could test the string output
# if you must.

#Thanks!
