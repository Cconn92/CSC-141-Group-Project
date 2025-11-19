""" Im just gonna throw in some code that would probably be useful"""

def _create_board(rows,cols,default_value=0):
    """ Creates a 2D array (list of lists) with the given number of rows and columns,
        initialized with the default_value.
    """
    return [[default_value for _ in range(cols)] for _ in range(rows)]

def _create_icons(self, x-position, y-position):
    """ Creates a list of icon objects for the game board.
    """
    icons = []
    for row in range(self.rows):
        icon = Icon(x-position, y-position + row * self.icon_size, self.icon_size)
        icons.append(icon)
    return icons

def _swap_icons(self, icon1, icon2,icon3):
    """ Swaps the positions of three icons on the game board.
    """
    temp_x, temp_y = icon1.x, icon1.y
    icon1.x, icon1.y = icon2.x, icon2.y
    icon2.x, icon2.y = icon3.x, icon3.y
    icon3.x, icon3.y = temp_x, temp_y


