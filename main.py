import sys

def read_points(file):
    points = []
    for line_number, line in enumerate(file):
        point = line.strip().split(',')
        assert len(point) == 2, f'A point has to be separated by a comma and contains only two numbers.\
            There can only be one point per line. (line: {line_number + 1})'

        point[0] = point[0].replace(' ', '')
        point[1] = point[1].replace(' ', '')

        assert (point[0].replace('.','',1).isdigit() and point.count('.') < 2),\
            f'A point has to be a number of some kind (line: {line_number + 1})'
        assert (point[1].replace('.','',1).isdigit() and point.count('.') < 2),\
            f'A point has to be a number of some kind (line: {line_number + 1})'
        
        points.append([float(point[0]), float(point[1])])

    points.sort(key=lambda point: point[0])
    return points

def calc_slope(point1, point2):
    if (point2[0] - point1[0]) == 0:
        print(f'there can\'t be to equal x values: {point1[0]}, {point1[0]}; {point2[0]}, {point2[0]}')
        sys.exit(1)

    return (point2[1] - point1[1]) / (point2[0] - point1[0])

def calc_y(x, from_point, slope):
    return slope * (x - from_point[0])  + from_point[1]

def get_area_under_curve(points, precision):
    area_under_curve = 0
    prev_point = 0
    next_point = 1
    slope = calc_slope(points[prev_point], points[next_point])

    x = points[prev_point][0]
    while points[0][0] <= x <= points[-1][0]:
        if x > points[next_point][0]:
            prev_point += 1
            next_point += 1
            slope = calc_slope(points[prev_point], points[next_point])

        y = calc_y(x, points[prev_point], slope)
        area_under_curve += 1 / precision * y

        x += 1 / precision

    return area_under_curve

def get_area_not_absorbed(points, area_under_curve):
    max_area = (points[-1][0] - points[0][0])
    return max_area - area_under_curve

def get_point_max(points):
    point_max_absorbtion = [0, 0]
    for point in points:
        if point[1] > point_max_absorbtion[1]:
            point_max_absorbtion = point
    return point_max_absorbtion

#gives the average wave_length of photons that are not absorbed
#this wave_length can probably be mapped to the color of the particles
def get_average_wave_length(points, area_not_absorbed):
    return area_not_absorbed / points[-1][0]

def main():
    assert len(sys.argv) == 2, f'The programm takes one argument, a file to read points from. {len(sys.argv)} arguments where given'
    with open(sys.argv[1]) as file:
        points = read_points(file)

    #the area_under_curve of test points is 4
    #test_points = [[0, 0], [2, 2], [4, 0]]

    precision = 10000
    area_under_curve = get_area_under_curve(points, precision)    
    print(f'\narea_under_curve: {area_under_curve}\n')

    area_not_absorbed = get_area_not_absorbed(points, area_under_curve)
    print(f'\narea not absorbed: {area_not_absorbed}\n')

    point_max = get_point_max(points)
    print(f'\nx of maximum: {point_max[0]}, y of maximum: {point_max[1]}\n')

    average_wave_length = get_average_wave_length(points, area_not_absorbed)
    print(f'\naverage wave length of not absorbed photons: {average_wave_length}\n')

if __name__ == "__main__":
    main()