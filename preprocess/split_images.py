import os
import argparse
from PIL import Image
import linzhutils as lu
from tqdm import tqdm


def split_image(input_path,
                output_path,
                num_rows=10,
                num_cols=10,
                subimage_size=512):
    # Create output directory if it doesn't exist
    lu.checkDir(output_path)

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
                    subimage.save(os.path.join(output_path, subimage_filename))


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',
                        '--input',
                        type=str,
                        required=True,
                        help='Path to input directory')
    parser.add_argument('-o',
                        '--output',
                        type=str,
                        required=True,
                        help='Path to output directory')
    args = parser.parse_args()

    # Split images
    split_image(args.input, args.output)