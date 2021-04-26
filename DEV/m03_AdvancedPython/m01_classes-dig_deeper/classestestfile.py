class Square:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.width * self.length
    
r = Square(20,20)

print(f"Rectangle Area: {r.area()}")