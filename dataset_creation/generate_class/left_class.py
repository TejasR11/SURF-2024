import numpy as np
from PIL import Image, ImageDraw
import random
import os
import json

class leftGenerator:
    def __init__(self, image_size=(640, 360), max_shape_size=(100, 100), num_images=1000, save_dir='physics_dataset'):
        self.image_size = image_size
        self.max_shape_size = max_shape_size
        self.num_images = num_images
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def create_image_with_shapes(self, shape1_coords, shape1_type, shape1_color, shape2_coords, shape2_type, shape2_color):
        """Create an image with two shapes based on the provided coordinates, types, and colors."""
        img = Image.new('RGB', self.image_size, color='white')
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

    def generate_label(self, shape1_type, shape1_color, shape2_type, shape2_color, moved_shape, direction):
        return f"Move the {shape1_color if moved_shape == 1 else shape2_color} {shape1_type if moved_shape == 1 else shape2_type} to the {direction} of the {shape2_color if moved_shape == 1 else shape1_color} {shape2_type if moved_shape == 1 else shape1_type}"

    def generate_dataset(self):
        dataset = {}
        shape_types = ['rectangle', 'circle']
        shape_colors = ['blue', 'red', 'green', 'yellow', 'purple']

        for _ in range(self.num_images):
            # Randomly generate the type, size, and color for shape 1
            shape1_type = random.choice(shape_types)
            shape1_color = random.choice(shape_colors)
            shape1_size = (np.random.randint(10, self.max_shape_size[0]), np.random.randint(10, self.max_shape_size[1]))
            shape1_x = np.random.randint(self.image_size[0] // 3, self.image_size[0] - shape1_size[0])
            shape1_y = np.random.randint(0, self.image_size[1] - shape1_size[1])
            shape1_coords = [shape1_x, shape1_y, shape1_x + shape1_size[0], shape1_y + shape1_size[1]]

            # Randomly generate the type, size, and color for shape 2
            shape2_type = random.choice(shape_types)
            shape2_color = random.choice(shape_colors)
            shape2_size = (np.random.randint(10, self.max_shape_size[0]), np.random.randint(10, self.max_shape_size[1]))
            shape2_x = np.random.randint(self.image_size[0] // 3, self.image_size[0] - shape2_size[0])
            shape2_y = np.random.randint(0, self.image_size[1] - shape2_size[1])
            shape2_coords = [shape2_x, shape2_y, shape2_x + shape2_size[0], shape2_y + shape2_size[1]]
            
            # Create the first image
            img1 = self.create_image_with_shapes(shape1_coords, shape1_type, shape1_color, shape2_coords, shape2_type, shape2_color)

            if shape1_x > shape2_x:
                # Move shape 1 to the left of shape 2
                new_shape1_x = shape2_x - shape2_size[0] - random.randint(0, shape2_x - 100)
                shape1_coords_moved = [new_shape1_x, shape1_y, new_shape1_x + shape1_size[0], shape1_y + shape1_size[1]]
                shape2_coords_moved = shape2_coords
                direction = "left"
                moved_shape = 1
            else:
                # Move shape 2 to the left of shape 1
                new_shape2_x = shape1_x - shape1_size[0] - random.randint(0, shape1_x - 100)
                shape2_coords_moved = [new_shape2_x, shape2_y, new_shape2_x + shape2_size[0], shape2_y + shape2_size[1]]
                shape1_coords_moved = shape1_coords
                direction = "left"
                moved_shape = 2
            
            # Create the second image with the adjusted position
            img2 = self.create_image_with_shapes(shape1_coords_moved, shape1_type, shape1_color, shape2_coords_moved, shape2_type, shape2_color)

            label = self.generate_label(shape1_type, shape1_color, shape2_type, shape2_color, moved_shape, direction)
            
            if label not in dataset:
                dataset[label] = []
            
            dataset[label].append((img1, img2))

        return dataset

    def save_dataset(self, dataset):
        label_counter = 0
        for label, image_pairs in dataset.items():
            label_dir_name = f'{label_counter:07d}'
            label_dir = os.path.join(self.save_dir, f'label_{label_dir_name}')
            os.makedirs(label_dir, exist_ok=True)
            
            for i, (img1, img2) in enumerate(image_pairs):
                img1.save(os.path.join(label_dir, f'image_{label_counter}_{i + 1}_0.jpg'))
                img2.save(os.path.join(label_dir, f'image_{label_counter}_{i + 1}_1.jpg'))

            label_json = {
                "edit": label
            }
            with open(os.path.join(label_dir, 'prompt.json'), 'w') as f:
                json.dump(label_json, f, indent=4)

            label_counter += 1
