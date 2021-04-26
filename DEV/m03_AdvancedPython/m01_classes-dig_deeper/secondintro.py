import turtle

class Polygon():
    def __init__(self, sides, name, size=100, color="black", line_thickness=100):
        self.sides = sides
        self.name = name
        self.size = size
        self.color = color
        self.line_thickness = line_thickness/10
        self.interior_angles = (self.sides - 2)*180
        self.angle = self.interior_angles/self.sides

    def draw(self):
        turtle.pensize(self.line_thickness)
        turtle.color(self.color)
        for i in range(self.sides):
            turtle.forward(self.size)
            turtle.right(180-self.angle)
        turtle.done()
#SubClass

class Square(Polygon):
    def __init__(self, size=100, color="black", line_thickness=80):
        super().__init__(4,"square", size, color, line_thickness)

square = Square()
pentagon = Polygon(5, "Pentagon")
hexagon = Polygon(6, "Hexagon")

square.draw()

print(square.sides)
print(square.name)
print(square.interior_angles)
print(square.angle)