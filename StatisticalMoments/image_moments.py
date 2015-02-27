import png

def image_moment(image_list_of_lists, i, j):
    moment = 0
    for x in range(len(image_list_of_lists[0])):
        for y in range(len(image_list_of_lists)):
            moment = moment + ((x**i)*(y**j)*image_list_of_lists[y][x])
    return moment

def area(image_list_of_lists):
    return naive_image_moment(image_list_of_lists, 0, 0)

def centre_of_mass(image_list_of_lists):
    area = area(image_list_of_lists)
    x_centroid = image_moment(image_list_of_lists, 1, 0)/area
    y_centroid = image_moment(image_list_of_lists, 0, 1)/area

    return (x_centroid,y_centroid)

def axis_of_orientation(image_list_of_lists):
    second_moment_a = image_moment(image_list_of_lists,2,0)
    second_moment_b = image_moment(image_list_of_lists,1,1)
    second_moment_c = image_moment(image_list_of_lists,0,2)

    sin_2_theta_1 = second_moment_b/math.sqrt((second_moment_b**2)+((second_moment_a-second_moment_c)**2))
    sin_2_theta_2 = -second_moment_b/math.sqrt((second_moment_b**2)+((second_moment_a-second_moment_c)**2))

    # the positive solution minimizes the integral, the negative solution maximizes the integral
    # this integral is (r**2)I(x,y) where r is the perp. distance from (x,y) to the line
    negative_theta_solution = min(sin_2_theta_1, sin_2_theta_2)
    positive_theta_solution = max(sin_2_theta_1, sin_2_theta_2)

    # we are trying to minimize the integral if we want to find the axis of orientation.
    # why? because the closer the points are to the line, the more likely it is that this line
    # is the axis of orientation, thus the smaller the value of r, and the smaller the value of
    # the integral.

    # Thus, we are concerned with the positive solution for theta.
    # theta is used to parametrize the line using:
    # x_prime*sin(theta) - y_prime*cos(theta) = 0
    # where x_prime = x - x_centroid, and y_prime = y - y-centroid

    # now we can return the line as a vector:
    x_centroid = centre_of_mass(image_list_of_lists)[0]
    y_centroid = centre_of_mass(image_list_of_lists)[1]
    parametrized_line = []
    for x in range(len(image_list_of_lists[0])):
        for y in range(len(image_list_of_lists)):
            x_prime = x - x_centroid
            y_prime = y - y_centroid
            parametrized_test = (x_prime*math.sin(negative_theta_solution)) - (y_prime*math.cos(negative_theta_solution))
            if(parametrized_test` == 0):
                parametrized_line.append(x,y)

    return parametrized_line


    

# def file2image(path):
#     (w, h, p, m) = png.Reader(filename = path).asRGBA()
#     return [image._flat2boxed(r) for r in p]

# def image2file(image, path):
#     if image.isgray(image):
#         img = image.gray2color(image)
#     else:
#         img = image
#     with open(path, 'wb') as f:
#         png.Writer(width=len(image[0]), height=len(image)).write(f, [_boxed2flat(r) for r in img])

# def color2gray(image):
#      """ Converts a color image to grayscale """
#      # we use HDTV grayscale conversion as per https://en.wikipedia.org/wiki/Grayscale
#      return [[int(0.2126*p[0] + 0.7152*p[1] + 0.0722*p[2]) for p in row] for row in image]
 
# def load_images(directoryname, num_faces = 2):
#      return {i:color2gray(file2image(os.path.join(directoryname,"img%02d.png" % i))) for i in range(num_faces)}
#      #loads the given number of image files from the classified files
#      #returns a dict of face number to image files

## Points for Meeting:
## Currently working on hacking up a system to compute moments for binary images
## Reading up on how to transform normal images into binary images by choosing threshold values for re-classification of pixel values