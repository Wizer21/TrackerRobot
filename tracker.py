last_x = 0
last_y = 0
min_rgb = (0, 0, 0)
max_rgb = (0, 0, 0)

min_diameter = 0
step = 4
adaptive_color = (0, 0, 0)
mid_rgb = (0, 0, 0)
color_iterator = 0
color_range = 0
variations = []


def new_pos(x, y, new_mid_rgb, newcolor_range):
    global last_x
    global last_y
    global color_iterator
    global color_range
    global adaptive_color
    global mid_rgb
    global min_diameter
    global variations

    last_x = x
    last_y = y
    color_range = newcolor_range
    mid_rgb = new_mid_rgb
    min_diameter = step

    adaptive_color = new_mid_rgb
    color_iterator = 1

    cal_colors()

    variations = [[0, -step],
                 [+step, -step],
                 [+step, 0],
                 [+step, +step],
                 [0, +step],
                 [-step, +step],
                 [-step, 0],
                 [-step, -step]]


def cam_tracker(pixel_map):
    global last_x
    global last_y
    global min_diameter

    # DEF MIN AND MAX COLOR FROM ADAPTATIVE
    cal_colors() 
    define_starter(pixel_map)

    # DEFINE START POSITION
    top = [last_x, last_y]
    top_right = [last_x, last_y]
    right = [last_x, last_y]
    bot_right = [last_x, last_y]
    bot = [last_x, last_y]
    bot_left = [last_x, last_y]
    left = [last_x, last_y]
    top_left = [last_x, last_y]

    positions = [top, top_right, right, bot_right, bot, bot_left, left, top_left]

    track = True
    for i in range(len(positions)):
        while track:
            if validate_pixel(pixel_map, positions[i][1], positions[i][0]):
                positions[i][0] += variations[i][0]
                positions[i][1] += variations[i][1]
            else:
                y = 1
                matched = False
                while y < 10:
                    if validate_pixel(pixel_map, positions[i][1] + (variations[i][1] * y), positions[i][0] + (variations[i][0] * y)):
                        positions[i][0] += (variations[i][0] * y)
                        positions[i][1] += (variations[i][1] * y)
                        y = 10
                        matched = True
                    y += 1
                if not matched:
                    break

        positions[i][0] -= variations[i][0]
        positions[i][1] -= variations[i][1]

    # DEFINE NEXT STARTER
    last_x = left[0] + int(((right[0] - left[0])/2))  # NEXT STARTER
    last_y = top[1] + int(((bot[1] - top[1])/2))

    point_stack = positions.copy()

    # FIND FAREST CORNER
    if left[0] < top_left[0]: 
        top_left[0] = left[0]
    if bot_left[0] < top_left[0]:
        top_left[0] = bot_left[0]
    if top[1] < top_left[1]:
        top_left[1] = top[1]
    if top_right[1] < top_left[1]:
        top_left[1] = top_right[1]

    if right[0] > bot_right[0]:
        bot_right[0] = right[0]
    if top_right[0] > bot_right[0]:
        bot_right[0] = top_right[0]
    if bot[1] > bot_right[1]:
        bot_right[1] = bot[1]
    if bot_left[1] > bot_right[1]:
        bot_right[1] = bot_left[1]

    # FIND MIN DIAMETER
    new_diameter = 0
    if right[0] - left[0] > 10:  
        new_diameter = right[0] - left[0]
    if new_diameter > bot[1] - top[1] > 10:
        new_diameter = bot[1] - top[1]
    if new_diameter > top_right[0] - bot_left[0] > 10:
        new_diameter = top_right[0] - bot_left[0]
    if new_diameter > bot_left[1] - top_right[1] > 10:
        new_diameter = bot_left[1] - top_right[1]

    if new_diameter > 10:
        min_diameter += (new_diameter - min_diameter) * 0.01

    new_width = bot_right[0] - top_left[0]
    new_height = bot_right[1] - top_left[1]

    update_adaptive_color()

    return top_left, bot_right, new_width, new_height, point_stack, adaptive_color, new_diameter


# CHECK IF PIXEL MATCHING
def is_pixel_matching(pixel):
    global adaptive_color
    global color_iterator

    if min_rgb[0] <= pixel[0] <= max_rgb[0] and min_rgb[1] <= pixel[1] <= max_rgb[1] and min_rgb[2] <= pixel[2] <= max_rgb[2]:

        adaptive_color = (int(adaptive_color[0]) + pixel[0], int(adaptive_color[1]) + pixel[1], int(adaptive_color[2]) + pixel[2])
        color_iterator += 1
        return True

    return False


def update_adaptive_color():
    global adaptive_color
    global color_iterator

    if color_iterator != 0:
        adaptive_color = (round(int(adaptive_color[0] / color_iterator)), round(int(adaptive_color[1] / color_iterator)), round(int(adaptive_color[2] / color_iterator)))
        color_iterator = 1

        # new_color = [adaptive_color[0], adaptive_color[1], adaptive_color[2]]
        # for i in range(len(new_color)):
        #     if new_color[i] <= native_rgb_min[i]:
        #         new_color[i] = native_rgb_min[i]
        #     elif native_rgb_max[i] <= new_color[i]:
        #         new_color[i] = native_rgb_max[i]
        #
        # adaptive_color = new_color


# DEFINE MIN AND MAX COLOR, FOR RANGE, BASED ON ADAPTATIVE COLOR
def cal_colors():
    global min_rgb
    global max_rgb

    # Set Min Color
    rgb = [adaptive_color[0], adaptive_color[1], adaptive_color[2]]
    for i in range(len(rgb)):
        rgb[i] -= int(color_range)
        if rgb[i] < 0:
            rgb[i] = 0
    min_rgb = (rgb[0], rgb[1], rgb[2])

    # Set Max Color
    rgb = [adaptive_color[0], adaptive_color[1], adaptive_color[2]]
    for i in range(len(rgb)):
        rgb[i] += int(color_range)
        if 255 < rgb[i]:
            rgb[i] = 255
    max_rgb = (rgb[0], rgb[1], rgb[2])


def new_color_range(new_value):
    global color_range

    color_range = new_value

# FIND THE PIXEL FROM WHERE THE TRACKING WILL BEGIN
def define_starter(pixel_map):
    global last_x
    global last_y
    global adaptive_color

    my_range = round(min_diameter)
    half_range = round(min_diameter/2)

    # IF THE FIRST PIXEL IS ALREADY MATCHING
    if validate_pixel(pixel_map, last_y, last_x):
        return

    stepper = variations

    maxi_stepper = [[0, -step],
                    [0, -step],
                    [+step, -step],
                    [+step, 0],
                    [+step, 0],
                    [+step, 0],
                    [+step, +step],
                    [0, +step],
                    [0, +step],
                    [0, +step],
                    [-step, +step],
                    [-step, 0],
                    [-step, 0],
                    [-step, 0],
                    [-step, -step],
                    [0, -step]]

    for y in range(4):

        if y > 1:
            position_list = [[0, -my_range],
                             [0 + half_range, -my_range],
                             [+my_range, -my_range],
                             [+my_range, 0 - half_range],
                             [+my_range, 0],
                             [+my_range, 0 + half_range],
                             [+my_range, +my_range],
                             [0 + half_range, +my_range],
                             [0, +my_range],
                             [0 - half_range, +my_range],
                             [-my_range, +my_range],
                             [-my_range, 0 + half_range],
                             [-my_range, 0],
                             [-my_range, 0 - half_range],
                             [-my_range, -my_range],
                             [0 - half_range, -my_range]]

            stepper = maxi_stepper

        else:
            position_list = [[0, -my_range],
                             [+my_range, -my_range],
                             [+my_range, 0],
                             [+my_range, +my_range],
                             [0, +my_range],
                             [-my_range, +my_range],
                             [-my_range, 0],
                             [-my_range, -my_range]]

        for i in range(len(position_list)):
            if validate_pixel(pixel_map, last_y + position_list[i][1], last_x + position_list[i][0]):
                last_x += position_list[i][0]
                last_y += position_list[i][1]
                return
            else:
                if validate_pixel(pixel_map, last_y + position_list[i][1] + stepper[i][1], last_x + position_list[i][0] + stepper[i][0]):
                    last_x += position_list[i][0] + stepper[i][0]
                    last_y += position_list[i][1] + stepper[i][1]
                    return
                else:
                    if validate_pixel(pixel_map, last_y + position_list[i][1] - stepper[i][1], last_x + position_list[i][0] - stepper[i][0]):
                        last_x += position_list[i][0] - stepper[i][0]
                        last_y += position_list[i][1] - stepper[i][1]
                        return

        my_range += round(min_diameter)
        half_range += round(min_diameter/2)


# CHECK IF THE PIXEL IS ->IN<- THE IMAGE
def validate_pixel(pixel_map, y, x):
    try:
        color = pixel_map[y][x]
        return is_pixel_matching((color[0], color[1], color[2]))
    except IndexError:
        return False