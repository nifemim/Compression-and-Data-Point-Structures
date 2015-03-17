from math import pow
from math import sqrt
from math import sin
from math import cos

def image_moment(image_dict, i, j):
  moment = 0
  for point in image_dict.keys():
    x = point[0]
    y = point[1]
    moment = moment + (pow(x,i)*pow(y,j)*image_dict[point])
  
  return moment

def area(image_dict):
  return naive_image_moment(image_dict, 0, 0)

def centre_of_mass(image_dict):
  area = area(image_dict)
  x_centroid = image_moment(image_dict, 1, 0)/area
  y_centroid = image_moment(image_dict, 0, 1)/area

  return (x_centroid,y_centroid)

def axes_of_orientation(image_dict):
  x_centroid = centre_of_mass(image_dict)[0]
  y_centroid = centre_of_mass(image_dict)[1]

  centered_points = {}
  for point in image_dict.keys():
    x = point[0]
    y = point[1]
    centered_points[x - x_centroid, y - y_centroid] = image_list_of_lists[y][x]

  # computing second moments on centered points
  second_moment_a = image_moment(centered_points, 2, 0)
  second_moment_b = image_moment(centered_points, 1, 1)
  second_moment_c = image_moment(centered_points, 0, 2)

  sin_2_theta_1 = second_moment_b / sqrt(pow(second_moment_b, 2) + pow(second_moment_a - second_moment_c,2))
  sin_2_theta_2 = -second_moment_b / sqrt(pow(second_moment_b, 2) + pow(second_moment_a - second_moment_c,2))

  # the positive solution minimizes the integral, the negative solution maximizes the integral
  # this integral is (r**2)I(x,y) where r is the perp. distance from (x,y) to the line
  negative_2_theta_solution = min(sin_2_theta_1, sin_2_theta_2)
  positive_2_theta_solution = max(sin_2_theta_1, sin_2_theta_2)

  # we are trying to minimize the integral if we want to find the axis of orientation.
  # why? because the closer the points are to the line, the more likely it is that this line
  # is the axis of orientation, thus the smaller the value of r, and the smaller the value of
  # the integral.

  # However, to span the entire image, we need two lines, theta (the line parametrizing the axis of orientation) and orth_theta
  # (the theta value giving a line orthogonal to the principal axis of orientation)

  theta = positive_2_theta_solution / 2
  orth_theta = negative_2_theta_solution / 2
  # Thus, we are concerned with the positive solution for theta and the negative value for orth_theta.
  # theta is used to parametrize the line using:
  # x_prime*sin(theta) - y_prime*cos(theta) = 0
  # where x_prime = x - x_centroid, and y_prime = y - y-centroid
  # Then, we do the same but with orth_theta, giving:
  # x_prime*sin(orth_theta) - y_prime*cos(orth_theta) = 0

  # now we can return the line as a vector:
  first_axis_line = []
  second_axis_line = []
  for pair in centered_points:
    x_prime = pair[0]
    y_prime = pair[1]
    on_first_axis_test = (x_prime * sin(theta)) - (y_prime * cos(theta))
    on_second_axis_test = (x_prime * sin(orth_theta)) - (y_prime * cos(orth_theta))
    if on_first_axis_test == 0:
      # de-centering the points
      first_axis_line.append((x_prime + x_centroid, y_prime + y_centroid))
    if on_second_axis_test == 0:
      # de-centering the points
      second_axis_line.append((x_prime + x_centroid, y_prime + y_centroid))
  
  return (first_axis_line, second_axis_line)