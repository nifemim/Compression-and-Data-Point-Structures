from math import pow
from math import sqrt
from math import sin
from math import cos

""" This method uses summations to find the moment of an image of degree (i, j)
OUTPUT: moment
"""
def image_moment(image_dict, i, j):
  moment = 0
  for point in image_dict.keys():
    x = point[0]
    y = point[1]
    moment = moment + (pow(x,i)*pow(y,j)*image_dict[point])
  
  return moment

""" This method uses the 0'th moment to find the area of the foreground point in an image
OUTPUT: the area of the image
"""
def area(image_dict):
  return image_moment(image_dict, 0, 0)

""" This method uses the coefficients up to N = p+q order to attempt to reconstruct the image.
OUTPUT: toReturn - a dictionary mapping locations onto values
"""
def reconstruct(image_dict, p, q):
  toReturn = {}
  exes = [-1, 0, 1]
  ys = [-1, 0, 1]
  for x in exes:
    for y in ys:
      toReturn[x, y] = 0
      for i in range(p):
        for j in range(q):
          toReturn[x, y] += (image_moment(image_dict, i, j)*pow(x, i)*pow(y, j))
  return toReturn

""" This method uses the first moment and area to find the centroids of an image.
OUTPUT: (x_centroid,y_centroid) - the x and y coordinates of the 'centre' of an image
"""
def centre_of_mass(image_dict):
  img_area = area(image_dict)
  x_centroid = image_moment(image_dict, 1, 0)/img_area
  y_centroid = image_moment(image_dict, 0, 1)/img_area

  return (x_centroid,y_centroid)

""" This method centers the points of an image
OUTPUT: centered_points - a dictionary of (x,y) coordinates mapped onto binary image values (foreground or background)
"""
def center_image(image_dict):
  centered_points = {}
  x_centroid = centre_of_mass(image_dict)[0]
  y_centroid = centre_of_mass(image_dict)[1]
  for point in image_dict.keys():
    x = point[0]
    y = point[1]
    centered_points[x - x_centroid, y - y_centroid] = image_dict[point]

  return centered_points

""" This method finds the axes of orientation of an image.
OUTPUT: (first_axis_line, second_axis_line) where first_axis_line is the principal axis and second_axis_line is the axis perpendicular to that.
"""
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

  # However, to span the entire image, we need two angles, theta (the line parametrizing the axis of orientation) and orth_theta
  # (the theta value giving a line orthogonal to the principal axis of orientation)

  theta = positive_2_theta_solution / 2
  orth_theta = negative_2_theta_solution / 2
  # Thus, we are concerned with the positive solution for theta and the negative value for orth_theta.
  # theta is used to parametrize the line using:
  # x_prime*sin(theta) - y_prime*cos(theta) = 0
  # where x_prime = x - x_centroid, and y_prime = y - y-centroid
  # Then, we do the same but with orth_theta, solving for:
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
  img_area = area(image_dict)
  x_centroid = centre_of_mass(image_dict)[0]
  y_centroid = centre_of_mass(image_dict)[1]
  # Centering the image
  centered_points = center_image(image_dict)
  # Finding the variance divided by the area
  varx = image_moment(centered_points, 2, 0)/img_area
  vary = image_moment(centered_points, 0, 2)/img_area
  # The standard deviation is the square root of the variance
  stdx = sqrt(varx)
  stdy = sqrt(vary)

  return (stdx, stdy)

""" Here, I find the skewness of the image using third central image moment.
OUTPUT: (skewx, skewy) where skewx is the skewness in the x direction and skewy is the skewness in the y direction.
"""
def skewness(image_dict):
  # As always, we will need the area
  img_area = area(image_dict)
  # Finding the standard deviation
  stdx = standard_deviation(image_dict)[0]
  stdy = standard_deviation(image_dict)[1]
  centered_points = center_image(image_dict)
  # Finding the third central image moment divided by area
  thirdx = image_moment(centered_points, 3, 0)/img_area
  thirdy = image_moment(centered_points, 0, 3)/img_area
  # Skewness is this third central moment divided by standard devation cubed
  # We have to check whether there is any standard deviation in either direction.
  # If not, then we know that the image is symmetrical.
  if stdx == 0:
    skewx = 0
  else:
    skewx = thirdx/pow(stdx,3)
  if stdy == 0:
    skewy = 0
  else:
    skewy = thirdy/pow(stdy,3)

  return (skewx, skewy)

""" Here, I find the kurtosis of the image using fourth central image moment.
OUTPUT: (kurtx, kurty) where kurtx is the kurtosis in the x direction and kurty is the kurtosis in the y direction.
"""
def kurtosis(image_dict):
  # We find the area, standard deviation and centered image
  img_area = area(image_dict)
  stdx = standard_deviation(image_dict)[0]
  stdy = standard_deviation(image_dict)[1]
  centered_points = center_image(image_dict)
  # Finding the fourth central moment divided by area
  fourthx = image_moment(centered_points, 4, 0)/img_area
  fourthy = image_moment(centered_points, 0, 4)/img_area
  # Kurtosis is the fourth central moment divided by standard deviation raised to four
  # We have to check whether there is any standard deviation in either direction.
  # If not, then the image is symmetrical.
  if stdx == 0:
    kurtx = 0
  else:
    kurtx = fourthx/pow(stdx,4)
  if stdy == 0:
    kurty = 0
  else:
    kurty = fourthy/pow(stdy,4)

  return (kurtx, kurty)