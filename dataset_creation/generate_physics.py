from generate_class.down_class import downGenerator
from generate_class.up_class import upGenerator
from generate_class.left_class import leftGenerator
from generate_class.right_class import rightGenerator
from generate_class.swap_class import swapGenerator


if __name__ == "__main__":
    generators = [
        rightGenerator(),
        leftGenerator(),
        downGenerator(),
        swapGenerator(),
        upGenerator()
    ]

    for generator in generators:
        dataset = generator.generate_dataset()
        generator.save_dataset(dataset)