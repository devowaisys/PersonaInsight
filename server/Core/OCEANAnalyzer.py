import nltk
import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, optimizers, preprocessing
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras import metrics
from TextPreProcessor import TextPreprocessor
from PersonalityInterpretor import PersonalityInterpreter


def download_nltk_resources():
    try:
        resources = ['punkt', 'stopwords', 'wordnet', 'omw-1.4']
        for resource in resources:
            nltk.download(resource, quiet=True)
            print(f"Successfully downloaded {resource}")
    except Exception as e:
        print(f"Error downloading NLTK resources: {str(e)}")


class OceanAnalyzer:
    def __init__(self, preprocessor, max_length=50):
        self.preprocessor = preprocessor
        self.max_length = max_length
        self.model = None
        self.tokenizer = preprocessing.text.Tokenizer()
        self.model_file = '../ocean_model.keras'  # Changed to .keras extension
        self.tokenizer_file = '../ocean_tokenizer.pkl'
        self.interpreter = PersonalityInterpreter()

    def save_model(self):
        # Save the Keras model with the newer .keras format
        self.model.save(self.model_file, save_format='keras')
        # Save the tokenizer
        with open(self.tokenizer_file, 'wb') as f:
            pickle.dump(self.tokenizer, f)
        print("OCEAN model saved successfully")

    def load_model(self):
        if os.path.exists(self.model_file) and os.path.exists(self.tokenizer_file):
            try:
                # Load the Keras model
                self.model = load_model(self.model_file)
                # Load the tokenizer
                with open(self.tokenizer_file, 'rb') as f:
                    self.tokenizer = pickle.load(f)
                print("OCEAN model loaded successfully")
                return True
            except Exception as e:
                print(f"Error loading OCEAN model: {str(e)}")
                return False
        return False

    def build_model(self, vocab_size):
        model = Sequential([
            layers.Embedding(vocab_size, 50, input_length=self.max_length),
            layers.LSTM(64, return_sequences=True),
            layers.GlobalMaxPooling1D(),
            layers.Dense(32, activation='relu'),
            layers.Dense(5, activation='linear')
        ])
        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss='mean_squared_error',  # Changed from 'mse' to full name
            metrics=[metrics.MeanSquaredError()]  # Explicit metric
        )
        return model

    def load_data(self, filepath):
        print("Loading OCEAN dataset...")
        encodings = ['utf-8', 'iso-8859-1', 'cp1252', 'latin1']

        for encoding in encodings:
            try:
                df = pd.read_csv(filepath, encoding=encoding)
                print(f"Successfully loaded OCEAN data using {encoding} encoding.")
                return df
            except UnicodeDecodeError:
                continue

        raise Exception("Failed to load OCEAN dataset with any encoding.")

    def prepare_data(self, df):
        sentences = df['STATUS'].values
        labels = df[['sEXT', 'sNEU', 'sAGR', 'sCON', 'sOPN']].values

        self.tokenizer.fit_on_texts(sentences)
        X = self.tokenizer.texts_to_sequences(sentences)
        X = preprocessing.sequence.pad_sequences(X, maxlen=self.max_length)

        return train_test_split(X, labels, test_size=0.2, random_state=42)

    def train(self, X_train, y_train, X_test, y_test, epochs=5, batch_size=64, save_model=True):
        print("\nTraining OCEAN analyzer...")
        vocab_size = len(self.tokenizer.word_index) + 1
        self.model = self.build_model(vocab_size)

        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(X_test, y_test),
            verbose=1
        )
        print("OCEAN training completed")
        if save_model:
            self.save_model()
        return history

    def analyze(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        sequences = self.tokenizer.texts_to_sequences(texts)
        padded_sequences = preprocessing.sequence.pad_sequences(
            sequences, maxlen=self.max_length
        )
        predictions = self.model.predict(padded_sequences, verbose=0)

        results = []
        for text, pred in zip(texts, predictions):
            results.append({
                'text': text,
                'ocean_scores': {
                    'extraversion': float(pred[0]),
                    'neuroticism': float(pred[1]),
                    'agreeableness': float(pred[2]),
                    'conscientiousness': float(pred[3]),
                    'openness': float(pred[4])
                }
            })
        return results

    def calculate_average_scores(self, results):
        """Calculate average OCEAN scores across multiple text samples."""
        if not results:
            return None

        # Initialize counters
        count = len(results)
        total_scores = {
            'extraversion': 0.0,
            'neuroticism': 0.0,
            'agreeableness': 0.0,
            'conscientiousness': 0.0,
            'openness': 0.0
        }

        # Sum all scores
        for result in results:
            for trait, score in result['ocean_scores'].items():
                total_scores[trait] += score

        # Calculate averages
        average_scores = {trait: score / count for trait, score in total_scores.items()}

        return average_scores

    def generate_personality_summary(self, results):
        """Generate a complete personality summary based on multiple text analyses."""
        # Calculate average scores
        average_scores = self.calculate_average_scores(results)
        if not average_scores:
            return "Insufficient data to generate a personality profile."

        # Use the interpreter to generate a detailed summary
        summary = self.interpreter.generate_personality_summary(average_scores)

        return summary


def main():
    preprocessor = TextPreprocessor()
    ocean_analyzer = OceanAnalyzer(preprocessor)

    try:
        # Try to load existing model first
        model_loaded = ocean_analyzer.load_model()

        if not model_loaded:
            print("OCEAN model not found. Training new model...")
            ocean_df = ocean_analyzer.load_data(r'C:\Users\Owais\PycharmProjects\PersonaInsight-server\mypersonality_final.csv')
            X_train, X_test, y_train, y_test = ocean_analyzer.prepare_data(ocean_df)
            ocean_analyzer.train(X_train, y_train, X_test, y_test)
        else:
            print("Using pre-trained OCEAN model")

        # Test analysis with more diverse text samples
        test_texts = [
            "I absolutely love this new product! Best purchase ever!",
            "This is the worst experience ever. Never buying again.",
            "Just received my order and it isn't exactly what I wanted!",
            "Terrible customer service, completely disappointed.",
            "I prefer spending time alone with a good book rather than going to parties.",
            "I always plan everything in advance and stick to my schedule.",
            "I'm always thinking about new ideas and love exploring different possibilities.",
            "I try to consider everyone's feelings before making decisions.",
            "Sometimes I worry too much about what could go wrong in situations."
        ]

        print("\nAnalyzing text samples...")
        results = ocean_analyzer.analyze(test_texts)

        # Print individual results
        print("\nIndividual Analysis Results:")
        for result in results:
            print(f"\nText: {result['text']}")
            print("OCEAN Traits:")
            for trait, score in result['ocean_scores'].items():
                print(f"  {trait.capitalize()}: {score:.2f}")

        # Calculate average scores
        average_scores = ocean_analyzer.calculate_average_scores(results)

        # Print average scores
        print("\n\nAverage OCEAN Scores Across All Texts:")
        for trait, score in average_scores.items():
            print(f"  {trait.capitalize()}: {score:.2f}")

        # Generate and print personality summary
        print("\n\n=====================================================")
        print("PERSONALITY PROFILE SUMMARY")
        print("=====================================================")
        summary = ocean_analyzer.generate_personality_summary(results)
        print(summary)
        print("=====================================================")

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    download_nltk_resources()
    main()