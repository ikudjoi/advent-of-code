class WireSection:
    def __init__(self, previousSection, vector):
        if (previousSection is None):
            x = 0
            y = 0
        else:
            x = previousSection.x2
            y = previousSection.y2

        self.vector = vector
        self.x1 = x
        self.y1 = y

        direction = vector[0]
        self.length = int(vector[1:])
        self.stepsToBegin = 0 if previousSection is None else previousSection.stepsToBegin + previousSection.length
        
        if direction == 'R':
            self.x2 = x + self.length
            self.y2 = y
        elif direction == 'L':
            self.x2 = x - self.length
            self.y2 = y
        elif direction == 'U':
            self.x2 = x
            self.y2 = y + self.length
        elif direction == 'D':
            self.x2 = x
            self.y2 = y - self.length
        else:
            raise Exception('perkele')
    
    def horizontal(self):
        return self.y1 == self.y2

    def left(self):
        return min(self.x1, self.x2)
    
    def right(self):
        return max(self.x1, self.x2)
    
    def low(self):
        return min(self.y1, self.y2)

    def high(self):
        return max(self.y1, self.y2)

    def intersectionDistance(self, otherVector):
        # Simplify the solution by assuming that wire sections can intersect
        # only if one is vertical and other is horizontal.
        if self.horizontal() == otherVector.horizontal():
            return None

        if self.horizontal():
            hor = self
            ver = otherVector
        else:
            hor = otherVector
            ver = self

        if ((hor.left() <= ver.x1 <= hor.right()) and (ver.low() <= hor.y1 <= ver.high())):
            #return abs(ver.x1) + abs(hor.y1)
            return hor.stepsToBegin + abs(hor.x1 - ver.x1) + ver.stepsToBegin + abs(ver.y1 - hor.y1)
        else:
            return None

def wireDefinitionToSections(wire):
    parts = wire.split(',')
    result = []
    previousSection = None
    for part in parts:
        section = WireSection(previousSection, part)
        result.append(section)
        previousSection = section
    return result

with open('input3.txt') as f:
    content = f.read()

#content = """R8,U5,L5,D3
#U7,R6,D4,L4"""

#content = """R75,D30,R83,U83,L12,D49,R71,U7,L72
#U62,R66,U55,R34,D71,R55,D58,R83"""

#content = """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
#U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"""

wires = [wire.strip() for wire in content.split('\n') if wire != '']
wireSections = [wireDefinitionToSections(wire) for wire in wires]

distances = [wireSection1.intersectionDistance(wireSection2) for wireSection1 in wireSections[0] for wireSection2 in wireSections[1]]
distances = [distance for distance in distances if distance is not None and distance > 0]
print(min(distances))

#print(wireSections)
#print(len(wireSections))