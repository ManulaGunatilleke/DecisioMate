import logging
import pickle
import os
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import numpy as np

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(level=logging.DEBUG)
formatter =  logging.Formatter('%(levelname)s : %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

logger.debug('simple message')

def predict_price_range_from_input(*args):
    """
    Predict the price range from the input features.

    Args:
        *args: Variable number of input features.

    Returns:
        numpy.ndarray: Predicted price range.
    """
    try:
        logging.debug("Predicting price range from input...")
        
        # Create a numpy array with the input values
        X_values = np.array([args])

        # Define the paths to the model weights file and the scaler file
        model_path = 'rec_sys/rec_data/mobile_price_prediction_weights.h5'
        scaler_path = 'rec_sys/rec_data/scaler.pkl'

        # Predict the price range
        y_pred = predict_price_range(X_values, model_path, scaler_path)
        logging.debug("Price range prediction successful.")

        return y_pred
    except Exception as e:
        logging.error(f"Error predicting price range from input: {e}")
        raise

def load_model(model_path):
    """
    Load the trained Keras model from the given path.
    
    Args:
        model_path (str): Path to the model weights file.
    
    Returns:
        model: Loaded Keras model.
    """
    try:
        logging.debug("Loading model...")
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(8, activation='relu', input_dim=20),  # Adjust input_dim to 21
            tf.keras.layers.Dense(4, activation='relu'),
            tf.keras.layers.Dense(2, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        model.load_weights(model_path)
        logging.debug("Model loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"Error loading the model: {e}")
        raise

def load_scaler(scaler_path):
    """
    Load the scaler object from the given path.
    
    Args:
        scaler_path (str): Path to the scaler file.
    
    Returns:
        scaler: Loaded scaler object.
    """
    try:
        logging.debug("Loading scaler...")
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        logging.debug("Scaler loaded successfully.")
        return scaler
    except Exception as e:
        logging.error(f"Error loading the scaler: {e}")
        raise

def predict_price_range(X_values, model_path, scaler_path):
    """
    Predict the price range using the trained model and scaler.
    
    Args:
        X_values (numpy.ndarray): Input features for prediction.
        model_path (str): Path to the model weights file.
        scaler_path (str): Path to the scaler file.
    
    Returns:
        numpy.ndarray: Predicted price range.
    """
    try:
        logging.debug("Predicting price range...")
        # Load the trained model
        model = load_model(model_path)

        # Load the scaler object
        scaler = load_scaler(scaler_path)

        # Feature scaling
        X_scaled = scaler.transform(X_values)

        # Predict using the model
        y_pred_probs = model.predict(X_scaled)
        y_pred = y_pred_probs.argmax(axis=1)  # Convert probabilities to class labels
        logging.debug("Price range prediction successful.")

        return y_pred
    except Exception as e:
        logging.error(f"Error predicting price range: {e}")
        raise
