class Dynamic_shape:
    def __init__(self):
        self.top_left = [0, 0]
        self.bot_right = [0, 0]
        self.center = [0, 0]
        self.width = 0
        self.height = 0
        self.points = []

    def build(self, new_top_left, new_bot_right, new_width, new_height, point_list):
        self.top_left = new_top_left
        self.bot_right = new_bot_right
        self.width = new_width
        self.height = new_height
        self.center = [new_top_left[0] + (self.width/2), new_top_left[1] + (self.height/2)]
        self.points = point_list