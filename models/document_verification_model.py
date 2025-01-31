import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report

def load_data():
    # Load preprocessed data
    X_train = np.load('../preprocessing/data/X_train.npy')
    X_test = np.load('../preprocessing/data/X_test.npy')
    y_train = np.load('../preprocessing/data/y_train.npy')
    y_test = np.load('../preprocessing/data/y_test.npy')
    return X_train, X_test, y_train, y_test


def build_model(input_shape, num_classes):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


def train_model():
    X_train, X_test, y_train, y_test = load_data()

    # Data Augmentation
    train_datagen = ImageDataGenerator(rescale=1. / 255, horizontal_flip=True, rotation_range=20)
    test_datagen = ImageDataGenerator(rescale=1. / 255)

    # Define the model
    model = build_model(input_shape=(224, 224, 3), num_classes=6)

    # Train the model
    history = model.fit(
        train_datagen.flow(X_train, y_train, batch_size=32),
        validation_data=test_datagen.flow(X_test, y_test),
        epochs=15
    )

    # Save the trained model
    model.save('../models/document_verification_model.h5')

    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test accuracy: {accuracy:.4f}")

    # Generate classification report
    y_pred = np.argmax(model.predict(X_test), axis=1)
    print(classification_report(y_test, y_pred))


if __name__ == "__main__":
    train_model()
