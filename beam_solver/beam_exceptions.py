class OutOfBounds(Exception):
    pass

class InvalidInput(Exception):
    pass

class BeamNotCalculated(Exception):
    pass

class ImpossibleToCalculate(Exception):
    pass


class SuperImposedSupports(Exception):
    def __init__(self):
        self.msg = "Supports are super-imposed"

    def __str__(self):
        return (self.msg)
