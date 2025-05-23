# ImagePro: AI-Powered Image Generation and Editing
ImagePro is a web-based application built with Streamlit that allows users to generate images from text prompts and edit uploaded images using Google Generative AI. The app provides a user-friendly interface for creating and downloading AI-generated or edited images, making it ideal for creative projects and experimentation with AI-driven image manipulation.
This project is developed by Aditya.

# Features
Image Generation: Generate images from text prompts (e.g., "A dinosaur fighting an ant") using Google Generative AI.
Image Editing: Upload an image and provide a text prompt to edit it (e.g., "Add a llama next to the subject").
Downloadable Outputs: Download generated or edited images in PNG format.
Interactive UI: Built with Streamlit for a seamless and intuitive user experience.
Error Handling: Robust error messages for invalid inputs or API issues.

View the deployed app here : https://imagepro-ai-app.streamlit.app/

## Prerequisites
Before running the project, ensure you have the following:

Python 3.10+: The project is compatible with Python 3.8 or higher.
Google Generative AI API Key: Obtain an API key from Google Cloud and store it in a .env file as GOOGLE_API_KEY.
Git: To clone the repository.
Virtual Environment (recommended): To manage dependencies.

# Installation

Clone the Repository:
git clone https://github.com/aditya0589/ImagePro.git
cd imagepro


Set Up a Virtual Environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:Install the required Python packages listed in requirements.txt:
pip install -r requirements.txt

The requirements.txt includes:

streamlit==1.38.0
google-generativeai==0.8.2
Pillow==10.4.0
python-dotenv==1.0.1


Set Up Environment Variables:Create a .env file in the project root and add your Google Generative AI API key:
GOOGLE_API_KEY=your-api-key-here


Run the Application:Start the Streamlit app:
streamlit run main.py

The app will open in your default web browser at http://localhost:8501.


## Usage
Generating an Image

In the main section of the app, enter a text prompt in the "Generate New Image" input field (e.g., "A dinosaur fighting an ant").
Click the Generate Image button.
Wait for the AI to process the prompt. The generated image will be displayed along with any accompanying text.
Use the Download Image button to save the image as generated_image.png.

Editing an Image

In the sidebar, under "Edit Image," upload an image (PNG, JPG, or JPEG format).
Enter an edit prompt (e.g., "Add a llama next to the subject").
Click the Edit Image button.
The edited image will be displayed in the main section, along with any generated text.
Use the Download Edited Image button to save the image as edited_image.png.

## Notes

Ensure your Google API key is valid and has access to the gemini-2.0-flash-preview-image-generation model.
If you encounter errors, check the error messages displayed in the app for guidance (e.g., invalid prompt, API issues, or file format errors).
Temporary image files (generated_image.png and edited_image.png) are saved in the project directory during app execution.

Project Structure
imagepro/
├── main.py              # Main Streamlit application
├── image_edit.py        # Module for image editing functionality
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (not tracked in Git)
├── README.md            # Project documentation (this file)
└── .gitignore           # Git ignore file (recommended)

## File Descriptions

main.py: The core Streamlit app that handles the UI, image generation, and integration with the image editing module.
image_edit.py: A modular script that processes image edits using Google Generative AI.
requirements.txt: Lists all required Python packages.
.env: Stores sensitive information like the Google API key (ensure this is added to .gitignore).
.gitignore: Recommended to include .env, *.png, and venv/ to avoid committing sensitive or temporary files.

Example Inputs
Image Generation

Prompt: "A futuristic city at sunset with flying cars"
Output: An AI-generated image of a futuristic city, downloadable as generated_image.png.

Image Editing

Uploaded Image: A photo of a person.
Edit Prompt: "Add a rainbow in the background"
Output: The photo with a rainbow added, downloadable as edited_image.png.

## Troubleshooting

API Key Errors: Ensure your GOOGLE_API_KEY is correctly set in the .env file and that the API is enabled in Google Cloud.
Image Not Generated/Edited: Verify that the prompt is clear and the uploaded image is in a supported format (PNG, JPG, JPEG).
Streamlit Issues: Ensure all dependencies are installed correctly (pip install -r requirements.txt) and that you're using a compatible Python version.
Connection Issues: Check your internet connection, as the Google Generative AI API requires online access.

## Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes and commit (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

Please ensure your code follows the project's style and includes appropriate tests or documentation updates.
## License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Built with Streamlit for the web interface.
Powered by Google Generative AI for image generation and editing.
Developed by Aditya.

## Contact
For questions or feedback, please open an issue on the GitHub repository or contact the developer at yraditya895@gmail.com.

Last updated: May 23, 2025
