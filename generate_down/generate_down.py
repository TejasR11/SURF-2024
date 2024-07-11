import numpy as np
from PIL import Image, ImageDraw
import random

def create_image_with_shapes(shape1_coords, shape1_type, shape1_color, shape2_coords, shape2_type, shape2_color, image_size=(640, 360)):
    """Create an image with two shapes based on the provided coordinates, types, and colors."""
    img = Image.new('RGB', image_size, color='white')
    draw = ImageDraw.Draw(img)

    # Draw shape 1
    if shape1_type == 'rectangle':
        draw.rectangle(shape1_coords, outline='black', fill=shape1_color)
    elif shape1_type == 'circle':
        draw.ellipse(shape1_coords, outline='black', fill=shape1_color)

    # Draw shape 2
    if shape2_type == 'rectangle':
        draw.rectangle(shape2_coords, outline='black', fill=shape2_color)
    elif shape2_type == 'circle':
        draw.ellipse(shape2_coords, outline='black', fill=shape2_color)

    return img

def generate_label(shape1_type, shape1_color, shape2_type, shape2_color, moved_shape, direction):
    return f"Move the {shape1_color if moved_shape == 1 else shape2_color} {shape1_type if moved_shape == 1 else shape2_type} {direction} the {shape2_color if moved_shape == 1 else shape1_color} {shape2_type if moved_shape == 1 else shape1_type}"

def generate_dataset(image_size=(640, 360), max_shape_size=(100, 100), num_images=10):
    dataset = []
    shape_types = ['rectangle', 'circle']
    shape_colors = ['blue', 'red', 'green', 'yellow', 'purple']

    for _ in range(num_images):
        # Randomly generate the type, size, and color for shape 1
        shape1_type = random.choice(shape_types)
        shape1_color = random.choice(shape_colors)
        shape1_size = (np.random.randint(10, max_shape_size[0]), np.random.randint(10, max_shape_size[1]))
        shape1_x = np.random.randint(0, image_size[0] - shape1_size[0])
        shape1_y = np.random.randint(0, (image_size[1] - shape1_size[1]) * 2 / 3)
        shape1_coords = [shape1_x, shape1_y, shape1_x + shape1_size[0], shape1_y + shape1_size[1]]

        # Randomly generate the type, size, and color for shape 2
        shape2_type = random.choice(shape_types)
        shape2_color = random.choice(shape_colors)
        shape2_size = (np.random.randint(10, max_shape_size[0]), np.random.randint(10, max_shape_size[1]))
        shape2_x = np.random.randint(0, image_size[0] - shape2_size[0])
        shape2_y = np.random.randint(0, (image_size[1] - shape2_size[1]) * 2 / 3)
        shape2_coords = [shape2_x, shape2_y, shape2_x + shape2_size[0], shape2_y + shape2_size[1]]
        
        # Create the first image
        img1 = create_image_with_shapes(shape1_coords, shape1_type, shape1_color, shape2_coords, shape2_type, shape2_color, image_size)

        if shape1_y < shape2_y:
            # Move shape 1 below shape 2
            new_shape1_y = shape2_y + shape2_size[1] + random.randint(0, 50)
            shape1_coords_moved = [shape1_x, new_shape1_y, shape1_x + shape1_size[0], new_shape1_y + shape1_size[1]]
            shape2_coords_moved = shape2_coords
            direction = "below"
            moved_shape = 1
        else:
            # Move shape 2 below shape 1
            new_shape2_y = shape1_y + shape1_size[1] + random.randint(0, 50)
            shape2_coords_moved = [shape2_x, new_shape2_y, shape2_x + shape2_size[0], new_shape2_y + shape2_size[1]]
            shape1_coords_moved = shape1_coords
            direction = "below"
            moved_shape = 2
        
        # Create the second image with the adjusted position
        img2 = create_image_with_shapes(shape1_coords_moved, shape1_type, shape1_color, shape2_coords_moved, shape2_type, shape2_color, image_size)

        label = generate_label(shape1_type, shape1_color, shape2_type, shape2_color, moved_shape, direction)
        dataset.append((img1, img2, label))

    return dataset

# Generate the dataset
dataset = generate_dataset()

# Save the images and labels to disk for verification
for i, (img1, img2, label) in enumerate(dataset):
    img1.save(f'image_{i}_1.png')
    img2.save(f'image_{i}_2.png')
    with open(f'label_{i}.txt', 'w') as f:
        f.write(label)
