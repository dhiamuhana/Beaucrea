import streamlit as st
import tensorflow as tf
import os
from PIL import Image
import numpy as np

# Import the quiz component
import bsti_quiz

# Page Title
st.set_page_config(page_title="Beaucrea Skin Analyzer", layout="wide")
st.title("💖 Beaucrea: Smart Skin Analyzer")

# Load model only once
@st.cache_resource
def load_skin_model():
    return tf.keras.models.load_model("mobilenetv2_skin_classification_model.keras")

@st.cache_resource
def get_class_labels():
    train_dir = "C:/Users/Ideapad Gaming/OneDrive/Beaucrea Skin Classification/train"
    return sorted(os.listdir(train_dir))

model = load_skin_model()
class_labels = get_class_labels()

# Tabs for UI
tab1, tab2 = st.tabs(["📷 Skin Trait Classifier", "🧪 BSTI Quiz"])

# ---- TAB 1: Keras Model Prediction ----
with tab1:
    st.header("📷 Upload a Skin Image for Trait Prediction")

    uploaded_file = st.file_uploader("Upload a close-up skin image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB').resize((224, 224))
        st.image(image, caption="Uploaded Image", use_column_width=False)

        img_array = np.array(image) / 255.0
        img_array = img_array.reshape(1, 224, 224, 3)

        prediction = model.predict(img_array)[0]

        st.subheader("🔍 Trait Probabilities:")
        for i, label in enumerate(class_labels):
            st.write(f"**{label}**: {prediction[i]*100:.2f}%")

        st.subheader("🧾 Final Traits:")
        threshold = 0.5
        predicted_traits = [label for i, label in enumerate(class_labels) if prediction[i] >= threshold]

        if predicted_traits:
            st.success("Detected Traits: " + ", ".join(predicted_traits))
        else:
            st.warning("No clear traits detected (all below threshold). Marking as **Normal**.")
            st.success("Detected Traits: Normal")

# ---- TAB 2: BSTI Quiz ----
with tab2:
    st.header("🧪 Take the Baumann Skin Type Indicator (BSTI) Quiz")
    bsti_quiz.run_bsti_quiz()
