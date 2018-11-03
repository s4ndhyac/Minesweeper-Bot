

class Cell:

    def __init__(self, cell_state, percept, mine_probability, xPos, yPos):
        self.cell_state = cell_state
        self.percept = percept
        self.mine_probability = mine_probability
        self.xPos = xPos
        self.yPos = yPos
