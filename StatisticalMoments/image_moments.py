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

def center_image(image_dict):
  centered_points = {}
  x_centroid = centre_of_mass(image_dict)[0]
  y_centroid = centre_of_mass(image_dict)[1]
  for point in image_dict.keys():
    x = point[0]
    y = point[1]
    centered_points[x - x_centroid, y - y_centroid] = image_dict[point]

  return centered_points

def axes_of_orientation(image_dict):
  x_centroid = centre_of_mass(image_dict)[0]
  y_centroid = centre_of_mass(image_dict)[1]

  centered_points = center_image(image_dict)

  # computing second central moments
  seconda = image_moment(centered_points, 2, 0)
  secondb = image_moment(centered_points, 1, 1)
  secondc = image_moment(centered_points, 0, 2)

  sin_2_theta_1 = secondb / sqrt(pow(secondb, 2) + pow(seconda - secondc,2))
  sin_2_theta_2 = -secondb / sqrt(pow(secondb, 2) + pow(seconda - secondc,2))

  # the positive solution minimizes the integral, the negative solution maximizes the integral
  # this integral is (r**2)I(x,y) where r is the perp. distance from (x,y) to the line
  negative_2_theta_solution = min(sin_2_theta_1, sin_2_theta_2)
  positive_2_theta_solution = max(sin_2_theta_1, sin_2_theta_2)

  # we are trying to minimize the integral if we want to find the axis of orientation.
  # the closer the points are to the line, the more likely it is that this line
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

  """ In this function, I calculate the standard deviation of foreground/background values in the binary image. This standard deviation is returned as a tuple
  OUTPUT: (stdx, stdy) where stdx is the standard deviation in the x axis, and stdy is the standard deviation in the y axis.
  """
def standard_deviation(image_dict):
  # Finding the area and centroids
  area = area(image_dict)
  x_centroid = centre_of_mass(image_dict)[0]
  y_centroid = centre_of_mass(image_dict)[1]
  # Centering the image
  centered_points = center_image(image_dict)
  # Finding the variance divided by the area
  varx = image_moment(centered_points, 2, 0)/area
  vary = image_moment(centered_points, 0, 2)/area
  # The standard deviation is the square root of the variance
  stdx = sqrt(varx)
  stdy = sqrt(vary)

  return (stdx, stdy)

""" Here, I find the skewness of the image using third central image moment.
OUTPUT: (skewx, skewy) where skewx is the skewness in the x direction and skewy is the skewness in the y direction.
"""
def skewness(image_dict):
  # As always, we will need the area
  area = area(image_dict)
  # Finding the standard deviation
  stdx = standard_deviation(image_dict)[0]
  stdy = standard_deviation(image_dict)[1]
  centered_points = center_image(image_dict)
  # Finding the third central image moment divided by area
  thirdx = image_moment(centered_points, 3, 0)/area
  thirdy = image_moment(centered_points, 0, 3)/area
  # Skewness is this third central moment divided by standard devation cubed
  skewx = thirdx/pow(stdx,3)
  skewy = thirdy/pow(stdy,3)

  return (skewx, skewy)

def kurtosis(image_dict):
  # We find the area, standard deviation and centered image
  area = area(image_dict)
  stdx = standard_deviation(image_dict)[0]
  stdy = standard_deviation(image_dict)[1]
  centered_points = center_image(image_dict)
  # Finding the fourth central moment divided by area
  fourthx = image_moment(centered_points, 4, 0)/area
  fourthy = image_moment(centered_points, 0, 4)/area
  # Kurtosis is the fourth central moment divided by standard deviation raised to four
  kurtx = fourthx/pow(stdx,4)
  kurty = fourthy/pow(stdy,4)

  return (kurtx, kurty)