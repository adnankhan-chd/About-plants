
import os
import streamlit as st
from google import genai
from google.genai import types

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Plant Identification AI",
    page_icon="🌿",
    layout="wide"
)

# -------------------------------
# CUSTOM DESIGN
# -------------------------------

st.markdown("""
<style>
.main {
    background-color: #f5faf5;
}
.title {
    text-align: center;
    color: #176b3a;
    font-size: 38px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #52745b;
    font-size: 17px;
}
.stButton>button {
    background-color: #198754;
    color: white;
    border-radius: 10px;
    width: 100%;
    height: 45px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------

st.markdown(
    '<p class="title">🌿 Plant Identification AI</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Discover the identity and science behind every plant.</p>',
    unsafe_allow_html=True
)

st.divider()

# -------------------------------
# GET API KEY
# -------------------------------

def get_api_key():
    try:
        key = st.secrets.get("GEMINI_API_KEY")
        if key:
            return key
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY")


api_key = get_api_key()

if not api_key:
    st.error(
        "Gemini API key not found. "
        "Please configure GEMINI_API_KEY."
    )
    st.stop()

# -------------------------------
# INITIALIZE GEMINI
# -------------------------------

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.8-flash"

# -------------------------------
# IMAGE UPLOAD
# -------------------------------

st.subheader("📸 Upload Your Plant Image")

uploaded_file = st.file_uploader(
    "Choose a plant picture",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file:

    if uploaded_file.size > 10 * 1024 * 1024:
        st.error("Image must be smaller than 10 MB.")
        st.stop()

    image_bytes = uploaded_file.getvalue()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(
            image_bytes,
            caption="Your Uploaded Plant",
            use_container_width=True
        )

    with col2:
        st.info(
            "Your image is ready for AI analysis. "
            "Click the button below to identify your plant."
        )

    # -------------------------------
    # IDENTIFICATION BUTTON
    # -------------------------------

    if st.button("🔍 Identify Plant"):

        prompt = """
        You are an expert botanical assistant.

        Analyze the uploaded image.

        First determine whether the image contains a recognizable plant.

        If it does not, explain that it cannot be identified as a plant.

        If it does, provide a structured report using these headings:

        # 1. Plant Identification
        - Common name
        - Scientific name
        - Identification confidence (high, medium, or low)
        - Other possible identities if uncertain

        # 2. Plant Description
        - Physical characteristics
        - Leaf characteristics
        - Flower and fruit characteristics, if visible

        # 3. Botanical Classification
        - Domain
        - Kingdom
        - Division
        - Class
        - Order
        - Family
        - Genus
        - Species

        Mark unavailable or uncertain classifications clearly.

        # 4. Plant Group
        Identify its major botanical group:
        - Angiosperm (flowering plant)
        - Gymnosperm
        - Fern
        - Moss
        - Algae
        - Other appropriate group

        Explain why it belongs to this group.

        # 5. Habitat and Distribution
        Describe its natural habitat and geographical
        distribution. Do not guess its exact location.

        # 6. Growing and Care Requirements
        - Sunlight
        - Water
        - Soil
        - Temperature
        - General maintenance

        # 7. Uses and Importance
        Explain its ecological and common practical uses.

        # 8. Interesting Facts
        Provide three interesting facts.

        Important instructions:
        - Do not invent scientific facts.
        - Clearly state uncertainty.
        - Do not claim exact species identification
          when the photograph does not support it.
        - Do not recommend eating or using an
          unidentified plant medicinally.
        - Use clear and beginner-friendly language.
        """

        with st.spinner(
            "🌱 Gemini AI is analyzing your plant..."
        ):

            try:

                image_part = types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=uploaded_file.type
                )

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=[prompt, image_part]
                )

                result = response.text

                if result:
                    st.success("Plant analysis completed!")

                    st.divider()

                    st.subheader("🌿 Plant Identification Results")

                    st.markdown(result)

                else:
                    st.warning(
                        "The AI did not return a result. "
                        "Please try another image."
                    )

            except Exception as e:

                st.error(
                    "Something went wrong while analyzing "
                    "the image. Please try again."
                )

                st.caption(str(e))

# -------------------------------
# FOOTER
# -------------------------------

st.divider()

st.markdown(
    """
    <center>
    🌿 Plant Identification AI |
    Powered by Python, Streamlit and Gemini AI
    </center>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Disclaimer: AI identification can be inaccurate. "
    "Verify important botanical information with a "
    "qualified botanical source."
)
