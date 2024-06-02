import streamlit as st
import cv2
import numpy as np
from PIL import Image
from utils import apply_makeup

# Set the background color to a pastel shade
st.markdown(
    """
    <style>
    body {
        background-color: #f0e6f6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    # Add a header with the title
    st.title("BeauteTryOn")
    st.markdown("---")

    # Sidebar for selecting makeup feature
    st.sidebar.title("Options")
    feature = st.sidebar.radio("Select Makeup Feature", ["Foundation", "Lips"])

    # Load the image
    image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if image_file is not None:
        image = np.array(Image.open(image_file))
        st.image(image, caption="Original Image", use_column_width=True)

        # Apply makeup based on selected feature
        if feature == "Foundation":
            with st.spinner('Applying Foundation...'):
                output_image = apply_makeup(image, False, 'foundation', False)
        elif feature == "Lips":
            with st.spinner('Applying Lipstick...'):
                output_image = apply_makeup(image, False, 'lips', False)

        st.success('Makeup Applied!')
        st.image(output_image, caption="Makeup Applied", use_column_width=True)

if __name__ == "__main__":
    main()
