import streamlit as st
from PIL import Image
from backend import ASLPredictor

st.set_page_config(
    page_title="ASL Recognition Studio",
    page_icon="🤟",
    layout="wide"
)

@st.cache_resource
def load_predictor():
    return ASLPredictor()

try:
    predictor = load_predictor()
except Exception as e:
    st.error("Error loading model. Make sure 'asl_base_model.keras' is in the same folder!")
    st.stop()

st.title("American Sign Language (ASL) Recognition 🤟")
st.markdown("Upload an image or use your camera to predict the ASL sign.")
st.markdown("---")

col1, col2 = st.columns([0.5, 0.5])

with col1:
    st.subheader("Input Image")
    option = st.radio("Choose Input Method:", ("Upload Image", "Camera Shot"))
    
    uploaded_file = None
    if option == "Upload Image":
        uploaded_file = st.file_uploader("Choose an ASL image...", type=["jpg", "jpeg", "png"])
    else:
        uploaded_file = st.camera_input("Take a photo of the sign")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Selected Image", use_container_width=True)

with col2:
    st.subheader("Prediction Results")
    if uploaded_file is not None:
        if st.button("Predict Sign", type="primary"):
            with st.spinner("Analyzing image..."):
                predicted_class, confidence, probabilities = predictor.predict(image)
            
            st.success(f"### Predicted Sign: {predicted_class}")
            st.metric(label="Confidence Score", value=f"{confidence * 100:.2f}%")
            
            st.markdown("---")
            st.write("#### Top Probabilities:")
            sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:5]
            for label, prob in sorted_probs:
                st.write(f"**{label}**")
                st.progress(prob)
                st.write(f"{prob * 100:.2f}%")
    else:
        st.info("Please upload an image or capture one using the camera to see predictions.")