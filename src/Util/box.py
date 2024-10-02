from typing import Tuple

class Box():
    """
    Simple class use to represent the a bounding box.
    """

    def __init__(self, x:float, y:float, width:float, hight:float) -> None:
        """
        Constructs a box object with a reference to the to corner and the width and hight (size).
        """
        self.left = x
        self.top = y
        self.width = width
        self.hight = hight

    @classmethod
    def from_points(cls, top_left:tuple[float, float], bottom_right:tuple[float,float]):
        x, y = top_left
        x_2, y_2 = bottom_right
        return cls(x,y,x_2-x,y-y_2)
    
    def get_width(self):
        return self.width
    def get_height(self):
        return self.hight
    
    def get_left(self):
        return self.left
    
    def get_top(self):
        return self.top
    
    def get_right(self):
        return self.get_left() + self.get_width()
    
    def get_bottom(self):
        return self.get_top() - self.get_height()
    
    
    def get_size(self)->tuple[float, float]:
        return self.width, self.hight
    
    def get_top_left(self)->tuple[float, float]:
        """Returns the position of the top left box corner (x,y)"""
        return self.get_left(), self.get_top()
    
    def get_bottom_right(self)->tuple[float,float]:
        """Returns the position of the bottom right corer (x,y)"""
        return self.get_right(), self.get_bottom()
    
    def get_points(self)->tuple[float, float, float, float]:
        """
        Returns the position of the box edges in the order left, top, right, bottom.
        """
        return self.get_left(), self.get_top(), self.get_right(), self.get_bottom()