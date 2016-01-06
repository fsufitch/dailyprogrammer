import math, sys

def get_pixel(img, row, col, default=None):
    if not (0 <= row < len(img)): # invalid row
        return default
    if not (0 <= col < len(img[row])): # invalid col
        return default
    return img[row][col]

def get_pixel_neighbors(img, row, col, distance, default=None):
    subimg = []
    for drow in range(-1*distance, distance+1):
        subrow = []
        for dcol in range(-1*distance, distance+1):
            subrow.append(get_pixel(img, row + drow, col + dcol, default))
        subimg.append(subrow)
    return subimg

def rgb_to_grayscale(rgb_img):
    gray_img = []
    for rgb_row in rgb_img:
        gray_row = []
        for r, g, b in rgb_row:
            gray_row.append(int((r+g+b) / 3))
        gray_img.append(gray_row)
    return gray_img

def mask_sum_matrix(matrix, mask):
    total_value = 0
    total_weight = 0
    for i in range(len(mask)):
        for j in range(len(mask[i])):
            weight = mask[i][j]
            total_value += weight * matrix[i][j]
            total_weight += weight
    return total_value, total_weight
    

###

GAUSS_5x5_WEIGHT = [
    [ 2,  4,  5,  4,  2],
    [ 4,  9, 12,  9,  4],
    [ 5, 12, 15, 12,  5],
    [ 4,  9, 12,  9,  4],
    [ 2,  4,  5,  4,  2],
]
def gauss_pixel(gray_img, row, col):
    neighbors = get_pixel_neighbors(gray_img, row, col, 2, 0)
    gauss_sum, gauss_total_weight = mask_sum_matrix(neighbors, GAUSS_5x5_WEIGHT)
    return int(gauss_sum / gauss_total_weight)
    
def gauss(gray_img):
    gauss_img = []
    for i, gray_row in enumerate(gray_img):
        gauss_row = []
        for j, value in enumerate(gray_row):
            gauss_row.append(gauss_pixel(gray_img, i, j))
        gauss_img.append(gauss_row)
    return gauss_img
            
###

SOBEL_3x3_HORIZONTAL_MASK = [
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1],
]

SOBEL_3x3_VERTICAL_MASK = [
    [1, 2, 1],
    [0, 0, 0],
    [-1, -2, -1],
]

def sobel_pixel_gradient(gray_img, row, col):
    neighbors = get_pixel_neighbors(gray_img, row, col, 1, 0)
    gradient_h, _ = mask_sum_matrix(neighbors, SOBEL_3x3_HORIZONTAL_MASK)
    gradient_v, _ = mask_sum_matrix(neighbors, SOBEL_3x3_VERTICAL_MASK)
    gradient = math.sqrt(gradient_h * gradient_h + gradient_v * gradient_v)
    gradient_angle = math.atan2(gradient_h, gradient_v)
    return gradient, gradient_angle

def sobel_with_gradient_direction(gray_img):
    grad_img = []
    for i, gray_row in enumerate(gray_img):
        grad_row = []
        for j, value in enumerate(gray_row):
            grad_row.append(sobel_pixel_gradient(gray_img, i, j))
        grad_img.append(grad_row)
    return grad_img

###

def angle_to_coords(angle):
    while angle > math.pi:
        angle -= math.pi

    if (1/4 * math.pi < angle < 3/4 * math.pi):
        return [(-1, 0), (1, 0)] # direction = |
    else:
        return [(0, -1), (0, 1)] # direction = --

def suppress_pixel(grad_img, row, col):
    intensity, angle = get_pixel(grad_img, row, col, (0, 0))

    angle_coords = angle_to_coords(angle)

    # If either point along diagonals is more intense, suppress it
    for nbr_row, nbr_col in angle_coords:
        nbr_intensity, _ = get_pixel(grad_img, row+nbr_row, col+nbr_col, (0, 0))
        if nbr_intensity > intensity:
            return 0.7*intensity

    return 1.3*intensity

def nonmax_suppression(grad_img):
    intensity_img = []
    for i, grad_row in enumerate(grad_img):
        intensity_row = []
        for j, grad_data in enumerate(grad_row):
            intensity_row.append(suppress_pixel(grad_img, i, j))
        intensity_img.append(intensity_row)
    return intensity_img

###

def double_threshold(intensity_img, threshold_low=0.1, threshold_high=0.3):
    max_intensity = 0
    for row in intensity_img:
        max_intensity = max(max_intensity, *row)
        
    t1 = threshold_low * max_intensity
    t2 = threshold_high * max_intensity

    threshold_img = []
    for row in intensity_img:
        threshold_row = []
        for intensity in row:
            if intensity < t1:
                threshold_row.append(0)
            elif intensity < t2:
                threshold_row.append(1)
            else:
                threshold_row.append(2)
        threshold_img.append(threshold_row)
    return threshold_img

def weak_edge_tracking(threshold_img):
    edge_img = []
    for i, row in enumerate(threshold_img):
        edge_row = []
        for j, value in enumerate(row):
            neighbors = get_pixel_neighbors(threshold_img, i, j, 1, 0)
            edge_value = 1
            for nbr_row in neighbors:
                if 2 in nbr_row:
                    break
            else:
                edge_value = 0
            edge_row.append(edge_value)
        edge_img.append(edge_row)
    return edge_img

###

def normalize_intensity(intensity_img):
    max_intensity = 0
    avg_intensity = 0
    for row in intensity_img:
        max_intensity = max(max_intensity, *row)
        avg_intensity += sum(row)
    avg_intensity /= len(intensity_img) * len(intensity_img[0])

    white_value = (2 * avg_intensity + max_intensity) / 3
    
    gray_img = []
    for row in intensity_img:
        gray_row = []
        for intensity in row:
            value = int(255 * intensity / white_value)
            gray_row.append(min(value, 255))
        gray_img.append(gray_row)
    return gray_img

def parse_ppm_p3(data_str):
    chunks = data_str.split()
    if chunks[0] != "P3": 
        raise ValueError("This is not P3 PPM data!")
    width = int(chunks[1])
    height = int(chunks[2])
    cursor = 4
    img = []
    row = []
    while cursor < len(chunks):
        pixel = (int(chunks[cursor+0]), int(chunks[cursor+1]), int(chunks[cursor+2]))
        row.append(pixel)
        if len(row) == width:
            img.append(row)
            row = []
        cursor += 3
    return img

def print_grayscale_p3(gray_img, endl="\n", endpix="   "):
    print("P3")
    print(len(gray_img[0]), len(gray_img))
    print(255)
    print(endl.join([endpix.join(["{x} {x} {x}".format(x=value) for value in row]) for row in gray_img]))

def main():
    print("Reading image...", file=sys.stderr)
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    lines = [line.split("#", 1)[0] for line in lines]
    img = parse_ppm_p3('\n'.join(lines))
    
    print("Converting to grayscale...", file=sys.stderr)
    gray_img = rgb_to_grayscale(img)
    print("Blurring...", file=sys.stderr)
    gray_img = gauss(gray_img)
    print("Computing gradients...", file=sys.stderr)
    gradients = sobel_with_gradient_direction(gray_img)
    print("Performing non-maximum suppression...", file=sys.stderr)
    intensity_img = nonmax_suppression(gradients)
    """
    print("Applying double threshold filtering...", file=sys.stderr)
    if len(sys.argv) >= 4:
        print("  ... with custom thresholds", file=sys.stderr)
        threshold_img = double_threshold(intensity_img, float(sys.argv[2]), float(sys.argv[3]))
    else:
        threshold_img = double_threshold(intensity_img)
    print("Culling weak edges...", file=sys.stderr)
    threshold_img = weak_edge_tracking(threshold_img)
    """
    print("Normalizing intensity to 1-byte...", file=sys.stderr)
    gray_img = normalize_intensity(intensity_img)
    
    
    print("Printing...", file=sys.stderr)
    print_grayscale_p3(gray_img)

if __name__ == "__main__": main()
    
