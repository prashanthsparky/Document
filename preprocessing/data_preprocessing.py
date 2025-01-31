import os
import numpy as np
import cv2
from data_augmentation import create_datagen

def load_and_preprocess_images(data_dir):
    images = []
    labels = []
    label_map = {'adhar': 0, 'pan': 1, 'driving_license': 2, 'voter_id': 3, 'passport': 4, 'utility': 5}

    print("Loading and preprocessing images...")
    for category in os.listdir(data_dir):
        category_folder = os.path.join(data_dir, category)
        if not os.path.isdir(category_folder):
            continue

        for filename in os.listdir(category_folder):
            file_path = os.path.join(category_folder, filename)
            try:
                image = cv2.imread(file_path)
                if image is None:
                    print(f"Failed to load image {file_path}")
                    continue
                image = cv2.resize(image, (224, 224))
                images.append(image)
                labels.append(label_map[category])
            except Exception as e:
                print(f"Error loading image {file_path}: {e}")

    images = np.array(images)
    labels = np.array(labels)
    print(f"Loaded {len(images)} images with corresponding labels.")
    return images, labels


def split_data(images, labels):
    from sklearn.model_selection import train_test_split
    print("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, stratify=labels)
    print(f"Data split: {len(X_train)} training samples and {len(X_test)} testing samples.")
    return X_train, X_test, y_train, y_test


def save_data(X_train, X_test, y_train, y_test):
    save_dir = '../preprocessing/data'
    os.makedirs(save_dir, exist_ok=True)
    print(f"Saving data to {save_dir}...")

    np.save(os.path.join(save_dir, 'X_train.npy'), X_train)
    np.save(os.path.join(save_dir, 'X_test.npy'), X_test)
    np.save(os.path.join(save_dir, 'y_train.npy'), y_train)
    np.save(os.path.join(save_dir, 'y_test.npy'), y_test)

    print("Data saved successfully.")
    print(
        f"Training data saved to: {os.path.join(save_dir, 'X_train.npy')} and {os.path.join(save_dir, 'y_train.npy')}")
    print(f"Testing data saved to: {os.path.join(save_dir, 'X_test.npy')} and {os.path.join(save_dir, 'y_test.npy')}")


if __name__ == "__main__":
    data_dir = r'C:\Users\X1\pycharmprojects\document_verification_project11\data'
    images, labels = load_and_preprocess_images(data_dir)
    X_train, X_test, y_train, y_test = split_data(images, labels)
    save_data(X_train, X_test, y_train, y_test)
