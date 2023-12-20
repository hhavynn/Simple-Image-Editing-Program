from PIL import Image

def get_size(image):
    return image.size

def get_pixel(image, x, y):
    return image.getpixel((x, y))

def put_pixel(image, x, y, pixel):
    image.putpixel((x, y), pixel)

def create_image(size, color="RGB"):
    return Image.new(color, size)

def negative_filter(image):
    size = get_size(image)
    negative_image = create_image(size)

    for x in range(size[0]):
        for y in range(size[1]):
            pixel = get_pixel(image, x, y)
            negative_pixel = tuple(255 - value for value in pixel)
            put_pixel(negative_image, x, y, negative_pixel)

    return negative_image

def edge_detection(image):
    size = get_size(image)
    edge_image = create_image(size)

    for x in range(1, size[0] - 1):
        for y in range(1, size[1] - 1):
            gx = sum(get_pixel(image, i, y)[0] for i in range(x - 1, x + 2))
            gy = sum(get_pixel(image, x, j)[0] for j in range(y - 1, y + 2))
            edge_value = int((gx**2 + gy**2)**0.5)
            put_pixel(edge_image, x, y, (edge_value, edge_value, edge_value))

    return edge_image

def blend_images(image1, image2, alpha):
    blended_image = create_image(get_size(image1))

    for x in range(get_size(image1)[0]):
        for y in range(get_size(image1)[1]):
            pixel1 = get_pixel(image1, x, y)
            pixel2 = get_pixel(image2, x, y)
            blended_pixel = tuple(
                int(alpha * p1 + (1 - alpha) * p2) for p1, p2 in zip(pixel1, pixel2)
            )
            put_pixel(blended_image, x, y, blended_pixel)

    return blended_image

# Load sky images
sky1 = Image.open("sky1.jpg")
sky2 = Image.open("sky2.jpg")

# Blend negative sky images
blended_sky = blend_images(sky1, sky2, alpha=0.5)

# Apply negative filter
negative_sky1 = negative_filter(sky1)
negative_sky2 = negative_filter(sky2)

# Load night images
night1 = Image.open("night1.jpg")
night2 = Image.open("night2.jpg")

# Blend night images
blended_night = blend_images(night1, night2, alpha=0.5)

# Apply edge detection filter
edge_night1 = edge_detection(night1)
edge_night2 = edge_detection(night2)

# Create a collage of all images
collage_size = (get_size(sky1)[0] * 3, get_size(sky1)[1] * 2)
collage = create_image(collage_size)

# Top left: Negative sky1
for x in range(get_size(sky1)[0]):
    for y in range(get_size(sky1)[1]):
        put_pixel(collage, x, y, get_pixel(negative_sky1, x, y))

# Top middle: Negative sky2
for x in range(get_size(sky2)[0]):
    for y in range(get_size(sky2)[1]):
        put_pixel(collage, x + get_size(sky1)[0], y, get_pixel(negative_sky2, x, y))

# Top right: Blend of sky1 and sky2
for x in range(get_size(blended_sky)[0]):
    for y in range(get_size(blended_sky)[1]):
        put_pixel(collage, x + get_size(sky1)[0] * 2, y, get_pixel(blended_sky, x, y))

# Bottom left: Edge detection of night1
for x in range(get_size(edge_night1)[0]):
    for y in range(get_size(edge_night1)[1]):
        put_pixel(collage, x, y + get_size(sky1)[1], get_pixel(edge_night1, x, y))

# Bottom middle: Edge detection of night2
for x in range(get_size(edge_night2)[0]):
    for y in range(get_size(edge_night2)[1]):
        put_pixel(collage, x + get_size(sky1)[0], y + get_size(sky1)[1], get_pixel(edge_night2, x, y))

# Bottom right: Blend of night1 and night2
for x in range(get_size(blended_night)[0]):
    for y in range(get_size(blended_night)[1]):
        put_pixel(collage, x + get_size(sky1)[0] * 2, y + get_size(sky1)[1], get_pixel(blended_night, x, y))

# Display the final image
collage.show()

# Save the final image
collage.save("final_collage.jpg")
