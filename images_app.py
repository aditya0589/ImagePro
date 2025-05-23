import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
from image_edit import edit_image

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(page_title="ImagePro", page_icon="🖼️")

# Initialize Google genai client
try:
    client = genai.Client()
except Exception as e:
    st.error(f"Failed to initialize Google AI client: {e}")
    st.stop()

# Streamlit UI
st.title("ImagePro: AI Image Generation")
st.subheader("A product by Aditya")
st.write("Enter a prompt to generate an image or use the sidebar to edit an uploaded image.")

# Sidebar for image editing
st.sidebar.header("Edit Image")
uploaded_image = st.sidebar.file_uploader("Upload an image to edit", type=["png", "jpg", "jpeg"])
edit_prompt = st.sidebar.text_input("Enter edit prompt (e.g., 'Add a llama next to the subject'):", 
                                   value="Add a llama next to the subject")
edit_button = st.sidebar.button("Edit Image")

# Handle image editing
if edit_button:
    if not uploaded_image:
        st.sidebar.error("Please upload an image to edit.")
    elif not edit_prompt.strip():
        st.sidebar.error("Please enter a valid edit prompt.")
    else:
        with st.spinner("Editing image..."):
            try:
                # Load the uploaded image
                image = Image.open(uploaded_image)
                
                # Call the edit_image function
                edited_image, generated_text, error = edit_image(image, edit_prompt)
                
                if error:
                    st.error(error)
                else:
                    if generated_text:
                        st.write("**Generated Text (Edit):**")
                        st.write(generated_text)
                    
                    # Save edited image temporarily
                    edited_image.save('edited_image.png')
                    
                    # Display edited image in Streamlit
                    st.image(edited_image, caption=f"Edited: {edit_prompt}", use_container_width=True)
                    
                    # Provide download button
                    with open('edited_image.png', 'rb') as file:
                        st.download_button(
                            label="Download Edited Image",
                            data=file,
                            file_name="edited_image.png",
                            mime="image/png"
                        )
            except Exception as e:
                st.error(f"Error processing image: {e}")

# Main content for image generation
st.header("Generate New Image")
user_prompt = st.text_input("Enter your prompt (e.g., 'A dinosaur fighting an ant'):", 
                           value="A dinosaur fighting an ant")

# Handle image generation
if st.button("Generate Image"):
    if not user_prompt.strip():
        st.error("Please enter a valid prompt.")
    else:
        with st.spinner("Generating image..."):
            try:
                # Call the generate_content API with user prompt
                response = client.models.generate_content(
                    model="gemini-2.0-flash-preview-image-generation",
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE']
                    )
                )

                # Process the response
                image_found = False
                for part in response.candidates[0].content.parts:
                    if part.text is not None:
                        st.write("**Generated Text:**")
                        st.write(part.text)
                    elif part.inline_data is not None:
                        try:
                            # Convert inline data to image
                            image = Image.open(BytesIO(part.inline_data.data))
                            
                            # Save image temporarily
                            image.save('generated_image.png')
                            
                            # Display image in Streamlit
                            st.image(image, caption=user_prompt, use_container_width=True)
                            
                            # Provide download button
                            with open('generated_image.png', 'rb') as file:
                                st.download_button(
                                    label="Download Image",
                                    data=file,
                                    file_name="generated_image.png",
                                    mime="image/png"
                                )
                            image_found = True
                        except Exception as e:
                            st.error(f"Error processing image: {e}")

                if not image_found:
                    st.warning("No image was generated in the response.")

            except Exception as e:
                st.error(f"Error generating content: {e}")