import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
from image_edit import edit_image  # <-- your separate file containing edit_image()

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(page_title="ImagePro Chat & Editor", page_icon="🖼️")


# Initialize Google genai client
try:
    client = genai.Client()
except Exception as e:
    st.error(f"Failed to initialize Google AI client: {e}")
    st.stop()

# Session state initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None

# Sidebar for image editing functionality
st.sidebar.header("🖌️ Image Editing")
uploaded_image = st.sidebar.file_uploader("Upload an image to edit:", type=["png", "jpg", "jpeg"])
edit_prompt = st.sidebar.text_input("Enter edit prompt:", value="Add a llama next to the subject")
edit_button = st.sidebar.button("Edit Image")

if edit_button:
    if not uploaded_image:
        st.sidebar.error("Please upload an image.")
    elif not edit_prompt.strip():
        st.sidebar.error("Please enter a valid edit prompt.")
    else:
        with st.spinner("Editing image..."):
            try:
                image = Image.open(uploaded_image)
                edited_image, generated_text, error = edit_image(image, edit_prompt)
                if error:
                    st.sidebar.error(error)
                else:
                    if generated_text:
                        st.sidebar.write("**Generated Text (Edit):**")
                        st.sidebar.write(generated_text)

                    st.sidebar.image(edited_image, caption="Edited Image", use_container_width=True)
                    edited_image.save('edited_image.png')
                    with open('edited_image.png', 'rb') as file:
                        st.sidebar.download_button("Download Edited Image", file, "edited_image.png", "image/png")
            except Exception as e:
                st.sidebar.error(f"Error editing image: {e}")

# Main page
st.title("🖼️ ImagePro: AI Image Generation & Chat")
st.subheader("A product by Aditya")
st.write("Generate images, chat with AI to suggest improvements, and regenerate images.")

# Image generation section
st.header("🎨 Generate Image")
initial_prompt = st.text_input("Enter an image generation prompt:", value="A dinosaur fighting an ant")

if st.button("Generate Image"):
    if not initial_prompt.strip():
        st.error("Please enter a valid prompt.")
    else:
        with st.spinner("Generating image..."):
            try:
                response = client.models.generate_content(
                    model="imagen-3.0-generate-002",
                    contents=initial_prompt,
                    config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
                )

                image_found = False
                for part in response.candidates[0].content.parts:
                    if part.text is not None:
                        st.write("**Generated Text:**")
                        st.write(part.text)
                    elif part.inline_data is not None:
                        image = Image.open(BytesIO(part.inline_data.data))
                        st.image(image, caption=initial_prompt, use_container_width=True)
                        st.session_state.generated_image = image

                        image.save("generated_image.png")
                        with open('generated_image.png', 'rb') as file:
                            st.download_button("Download Image", file, "generated_image.png", "image/png")
                        image_found = True

                if not image_found:
                    st.warning("No image was generated.")
                else:
                    st.session_state.chat_history.append({"role": "assistant", "content": initial_prompt})

            except Exception as e:
                st.error(f"Error generating content: {e}")

# Chat interface for refinement
st.header("💬 Chat for Improvements")

if st.session_state.generated_image is None:
    st.info("Generate an image first before chatting.")
else:
    # Display previous chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.chat_message("user").write(message['content'])
        else:
            st.chat_message("assistant").write(message['content'])

    user_input = st.chat_input("Suggest improvements or ask anything:")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Processing your request..."):
            try:
                history_prompts = "\n".join(
                    [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history]
                )
                new_prompt = f"Based on the previous image and chat history:\n{history_prompts}\nGenerate improved image."

                response = client.models.generate_content(
                    model="gemini-2.0-flash-preview-image-generation",
                    contents=new_prompt,
                    config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
                )

                image_found = False
                for part in response.candidates[0].content.parts:
                    if part.text is not None:
                        st.chat_message("assistant").write(part.text)
                        st.session_state.chat_history.append({"role": "assistant", "content": part.text})
                    elif part.inline_data is not None:
                        image = Image.open(BytesIO(part.inline_data.data))
                        st.image(image, caption="Improved Image", use_container_width=True)
                        st.session_state.generated_image = image

                        image.save("improved_image.png")
                        with open('improved_image.png', 'rb') as file:
                            st.download_button("Download Improved Image", file, "improved_image.png", "image/png")
                        image_found = True

                if not image_found:
                    st.warning("No image generated for the improvement request.")

            except Exception as e:
                st.error(f"Error generating content: {e}")




