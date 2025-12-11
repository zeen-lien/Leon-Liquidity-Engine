"""
LEON LIQUIDITY ENGINE - LSTM PRICE PREDICTOR
Deep Learning model untuk prediksi arah harga cryptocurrency

ARSITEKTUR:
- Input: Sequence of OHLCV + Technical Indicators
- Model: LSTM (Long Short-Term Memory)
- Output: Prediksi arah harga (UP/DOWN) + Confidence

FITUR:
- Training dengan data historis
- Prediksi real-time
- Confidence scoring
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json
import pickle
from datetime import datetime

# Flag untuk cek apakah TensorFlow tersedia
TENSORFLOW_AVAILABLE = False
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
    from sklearn.preprocessing import MinMaxScaler
    TENSORFLOW_AVAILABLE = True
except ImportError:
    print("TensorFlow tidak tersedia. LSTM predictor akan menggunakan mode simulasi.")


# Konfigurasi default
DEFAULT_CONFIG = {
    "sequence_length": 24,  # 24 jam lookback untuk H1 data
    "features": ["close", "volume", "rsi_14", "ema_20", "ema_50", "atr_14"],
    "lstm_units": [64, 32],
    "dropout_rate": 0.2,
    "learning_rate": 0.001,
    "epochs": 50,
    "batch_size": 32,
    "validation_split": 0.2
}

# Path untuk menyimpan model
MODEL_DIR = Path("data/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)


class LSTMPredictor:
    """
    LSTM-based price direction predictor.
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or DEFAULT_CONFIG
        self.model = None
        self.scaler = MinMaxScaler() if TENSORFLOW_AVAILABLE else None
        self.is_trained = False
        self.training_history = None
        self.feature_columns = self.config["features"]
    
    def _prepare_sequences(
        self,
        df: pd.DataFrame,
        sequence_length: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare sequences untuk training LSTM.
        
        Parameters:
        -----------
        df: DataFrame dengan features
        sequence_length: Panjang sequence input
        
        Returns:
        --------
        X: Input sequences (samples, timesteps, features)
        y: Target labels (0=DOWN, 1=UP)
        """
        # Pastikan semua feature ada
        available_features = [f for f in self.feature_columns if f in df.columns]
        if len(available_features) < len(self.feature_columns):
            missing = set(self.feature_columns) - set(available_features)
            print(f"Warning: Missing features: {missing}")
        
        # Ambil data features
        data = df[available_features].values
        
        # Normalize data
        data_scaled = self.scaler.fit_transform(data)
        
        # Create sequences
        X, y = [], []
        for i in range(sequence_length, len(data_scaled)):
            X.append(data_scaled[i-sequence_length:i])
            
            # Target: 1 jika harga naik, 0 jika turun
            current_close = df['close'].iloc[i]
            prev_close = df['close'].iloc[i-1]
            y.append(1 if current_close > prev_close else 0)
        
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape: Tuple[int, int]) -> None:
        """
        Build LSTM model architecture.
        
        Parameters:
        -----------
        input_shape: (sequence_length, num_features)
        """
        if not TENSORFLOW_AVAILABLE:
            print("TensorFlow tidak tersedia. Model tidak bisa dibangun.")
            return
        
        self.model = Sequential([
            # First LSTM layer
            LSTM(
                units=self.config["lstm_units"][0],
                return_sequences=True,
                input_shape=input_shape
            ),
            BatchNormalization(),
            Dropout(self.config["dropout_rate"]),
            
            # Second LSTM layer
            LSTM(
                units=self.config["lstm_units"][1],
                return_sequences=False
            ),
            BatchNormalization(),
            Dropout(self.config["dropout_rate"]),
            
            # Dense layers
            Dense(16, activation='relu'),
            Dropout(self.config["dropout_rate"]),
            
            # Output layer (binary classification)
            Dense(1, activation='sigmoid')
        ])
        
        self.model.compile(
            optimizer=Adam(learning_rate=self.config["learning_rate"]),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        print("Model architecture:")
        self.model.summary()
    
    def train(
        self,
        df: pd.DataFrame,
        save_path: str = None
    ) -> Dict:
        """
        Train LSTM model dengan data historis.
        
        Parameters:
        -----------
        df: DataFrame dengan OHLCV + indicators
        save_path: Path untuk menyimpan model (optional)
        
        Returns:
        --------
        Dict dengan training metrics
        """
        if not TENSORFLOW_AVAILABLE:
            return self._simulate_training(df)
        
        # Prepare data
        X, y = self._prepare_sequences(df, self.config["sequence_length"])
        
        if len(X) < 100:
            raise ValueError(f"Data terlalu sedikit untuk training. Minimal 100 samples, got {len(X)}")
        
        # Build model
        input_shape = (X.shape[1], X.shape[2])
        self.build_model(input_shape)
        
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            )
        ]
        
        if save_path:
            callbacks.append(
                ModelCheckpoint(
                    save_path,
                    monitor='val_accuracy',
                    save_best_only=True
                )
            )
        
        # Train
        history = self.model.fit(
            X, y,
            epochs=self.config["epochs"],
            batch_size=self.config["batch_size"],
            validation_split=self.config["validation_split"],
            callbacks=callbacks,
            verbose=1
        )
        
        self.is_trained = True
        self.training_history = history.history
        
        # Calculate final metrics
        final_metrics = {
            "train_accuracy": float(history.history['accuracy'][-1]),
            "val_accuracy": float(history.history['val_accuracy'][-1]),
            "train_loss": float(history.history['loss'][-1]),
            "val_loss": float(history.history['val_loss'][-1]),
            "epochs_trained": len(history.history['loss']),
            "total_samples": len(X),
            "sequence_length": self.config["sequence_length"],
            "features_used": self.feature_columns
        }
        
        # Save scaler
        if save_path:
            scaler_path = save_path.replace('.h5', '_scaler.pkl').replace('.keras', '_scaler.pkl')
            with open(scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
        
        return final_metrics
    
    def _simulate_training(self, df: pd.DataFrame) -> Dict:
        """
        Simulasi training jika TensorFlow tidak tersedia.
        """
        self.is_trained = True
        return {
            "status": "simulated",
            "message": "TensorFlow tidak tersedia. Menggunakan mode simulasi.",
            "simulated_accuracy": 0.75,
            "total_samples": len(df),
            "sequence_length": self.config["sequence_length"]
        }
    
    def predict(self, df: pd.DataFrame) -> Dict:
        """
        Prediksi arah harga berdasarkan data terbaru.
        
        Parameters:
        -----------
        df: DataFrame dengan OHLCV + indicators (minimal sequence_length rows)
        
        Returns:
        --------
        Dict dengan prediksi dan confidence
        """
        if not self.is_trained:
            return self._simulate_prediction(df)
        
        if not TENSORFLOW_AVAILABLE:
            return self._simulate_prediction(df)
        
        # Prepare input sequence
        available_features = [f for f in self.feature_columns if f in df.columns]
        data = df[available_features].tail(self.config["sequence_length"]).values
        
        if len(data) < self.config["sequence_length"]:
            return {
                "error": f"Data tidak cukup. Butuh {self.config['sequence_length']} rows, got {len(data)}"
            }
        
        # Scale data
        data_scaled = self.scaler.transform(data)
        X = np.array([data_scaled])
        
        # Predict
        prediction = self.model.predict(X, verbose=0)[0][0]
        
        # Interpret prediction
        direction = "UP" if prediction > 0.5 else "DOWN"
        confidence = prediction if prediction > 0.5 else (1 - prediction)
        
        return {
            "direction": direction,
            "confidence": float(confidence),
            "raw_prediction": float(prediction),
            "current_price": float(df['close'].iloc[-1]),
            "timestamp": datetime.now().isoformat(),
            "model_status": "trained"
        }
    
    def _simulate_prediction(self, df: pd.DataFrame) -> Dict:
        """
        Simulasi prediksi berdasarkan indikator teknikal sederhana.
        """
        if df.empty:
            return {"error": "Data kosong"}
        
        # Simple prediction based on RSI and EMA
        current_close = float(df['close'].iloc[-1])
        
        # RSI-based prediction
        rsi = df['rsi_14'].iloc[-1] if 'rsi_14' in df.columns else 50
        
        # EMA-based prediction
        ema_20 = df['ema_20'].iloc[-1] if 'ema_20' in df.columns else current_close
        ema_50 = df['ema_50'].iloc[-1] if 'ema_50' in df.columns else current_close
        
        # Calculate direction
        bullish_signals = 0
        total_signals = 3
        
        if rsi < 40:  # Oversold = bullish
            bullish_signals += 1
        elif rsi > 60:  # Overbought = bearish
            bullish_signals -= 1
        
        if current_close > ema_20:
            bullish_signals += 1
        else:
            bullish_signals -= 1
        
        if ema_20 > ema_50:
            bullish_signals += 1
        else:
            bullish_signals -= 1
        
        # Determine direction and confidence
        if bullish_signals > 0:
            direction = "UP"
            confidence = 0.5 + (bullish_signals / total_signals) * 0.3
        elif bullish_signals < 0:
            direction = "DOWN"
            confidence = 0.5 + (abs(bullish_signals) / total_signals) * 0.3
        else:
            direction = "NEUTRAL"
            confidence = 0.5
        
        return {
            "direction": direction,
            "confidence": round(confidence, 2),
            "current_price": current_close,
            "rsi": round(float(rsi), 2) if not pd.isna(rsi) else None,
            "ema_20": round(float(ema_20), 2) if not pd.isna(ema_20) else None,
            "ema_50": round(float(ema_50), 2) if not pd.isna(ema_50) else None,
            "timestamp": datetime.now().isoformat(),
            "model_status": "simulated"
        }
    
    def save(self, path: str) -> None:
        """Save model dan scaler."""
        if self.model and TENSORFLOW_AVAILABLE:
            self.model.save(path)
            scaler_path = path.replace('.h5', '_scaler.pkl').replace('.keras', '_scaler.pkl')
            with open(scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            
            # Save config
            config_path = path.replace('.h5', '_config.json').replace('.keras', '_config.json')
            with open(config_path, 'w') as f:
                json.dump(self.config, f)
    
    def load(self, path: str) -> bool:
        """Load model dan scaler."""
        if not TENSORFLOW_AVAILABLE:
            print("TensorFlow tidak tersedia. Model tidak bisa di-load.")
            return False
        
        try:
            self.model = load_model(path)
            
            scaler_path = path.replace('.h5', '_scaler.pkl').replace('.keras', '_scaler.pkl')
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            
            config_path = path.replace('.h5', '_config.json').replace('.keras', '_config.json')
            if Path(config_path).exists():
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return False


# Global instance
lstm_predictor = LSTMPredictor()


def get_prediction_for_symbol(df: pd.DataFrame, symbol: str) -> Dict:
    """
    Helper function untuk mendapatkan prediksi untuk symbol tertentu.
    """
    prediction = lstm_predictor.predict(df)
    prediction["symbol"] = symbol
    return prediction
