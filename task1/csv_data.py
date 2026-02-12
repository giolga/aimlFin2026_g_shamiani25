import numpy as np
import pandas as pd


def generate_image_csv(num_samples=1000, filename="image_malware.csv"):
    np.random.seed(42)

    # Generate random grayscale images (0-255)
    X = np.random.randint(0, 256, (num_samples, 32 * 32))

    # Generate binary labels
    y = np.random.randint(0, 2, num_samples).reshape(-1, 1)

    # Combine pixels + label
    data = np.hstack((X, y))

    columns = [f"pixel_{i}" for i in range(1024)] + ["label"]
    df = pd.DataFrame(data, columns=columns)

    df.to_csv("image_malware.csv", index=False)
    print("Dataset saved as image_malware.csv")


generate_image_csv()
