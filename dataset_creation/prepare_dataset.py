import json
from argparse import ArgumentParser
from pathlib import Path
from tqdm.auto import tqdm

def main():
    parser = ArgumentParser()
    parser.add_argument("dataset_dir")
    args = parser.parse_args()
    dataset_dir = Path(args.dataset_dir)

    seeds = []
    with tqdm(desc="Listing dataset image seeds") as progress_bar:
        label_dirs = sorted(dataset_dir.glob("label_*"))
        print(f"Found {len(label_dirs)} label directories.")

        for label_dir in label_dirs:
            if not label_dir.is_dir():
                print(f"Skipping non-directory: {label_dir}")
                continue
            
            label_name = label_dir.name  # Gets 'label_0000000' from the directory name 'label_0000000'
            label_index = label_name.split('_')[1]  # Gets '0000000' from 'label_0000000'
            image_seeds = []

            print(f"Processing label: {label_name}")

            image_files = sorted(label_dir.glob(f"image_{label_index.split('0')[0]}*_1.jpg"))
            print(f"Found {len(image_files)} image files for label {label_name}.")

            for image_path in image_files:
                seed = "_".join(image_path.stem.split("_")[:3])  # Gets 'image_0_1' from 'image_0_1_1.png'
                print(f"Found image seed: {seed}")

                if seed not in image_seeds:
                    image_seeds.append(seed)
            
            if len(image_seeds) > 0:
                seeds.append((label_name, image_seeds))
                progress_bar.update()
            
            print(f"Label {label_name} seeds: {image_seeds}")

    seeds.sort()
    print(f"Total seeds found: {len(seeds)}")

    with open(dataset_dir.joinpath("seeds.json"), "w") as f:
        json.dump(seeds, f, indent=4)

    print("Seeds JSON created successfully!")

if __name__ == "__main__":
    main()
