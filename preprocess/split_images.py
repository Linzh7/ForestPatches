import os
import argparse
from PIL import Image
import linzhutils as lu
import json
from tqdm import tqdm


def split_image(input_path,
                output_path,
                num_rows=10,
                num_cols=10,
                subimage_size=512,
                batch_size=20,
                threshold_memory_gb=4):
    # Create output directory if it doesn't exist
    lu.checkDir(output_path)

    subimages = []
    current_memory = 0

    # Convert threshold memory from GB to bytes
    threshold_memory = int(threshold_memory_gb * 1024 * 1024 * 1024)

    # Loop over all files in input directory
    for filename in tqdm(lu.getFileList(input_path)):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # Load image
            image = Image.open(os.path.join(input_path, filename))

            # Loop over sub-images and save them
            for i in range(num_rows):
                for j in range(num_cols):
                    # Calculate coordinates of sub-image
                    left = j * subimage_size
                    top = i * subimage_size
                    right = left + subimage_size
                    bottom = top + subimage_size

                    # Crop sub-image and save it
                    subimage = image.crop((left, top, right, bottom))
                    subimage_filename = f"{filename[:-4]}_{i}_{j}.png"
                    subimages.append(
                        (subimage, os.path.join(output_path,
                                                subimage_filename)))
                    current_memory += subimage.size[0] * subimage.size[
                        1] * 3  # assume RGB image
                    if current_memory > threshold_memory or len(
                            subimages) == batch_size:
                        for subimage, subimage_filename in subimages:
                            subimage.save(subimage_filename)
                        subimages = []
                        current_memory = 0

    if subimages:
        for subimage, subimage_filename in subimages:
            subimage.save(subimage_filename)


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='path of the configuration file',
        default='./preprocess/split_conf.json',
    )
    # required=True)
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    # Split images
    split_image(config["input_path"],
                config["output_path"],
                threshold_memory_gb=config["memory_threshold"],
                batch_size=config["batch"])
