import gradio as gr
import base64
from PIL import Image
import io
from image_generator import StoryImageGenerator

# Create StoryImageGenerator instance
generator = StoryImageGenerator()

# Gradio interface function
def generate_story_and_images(prompt):
    story, images_base64 = generator.generate_story_and_images(prompt)
    
    # Decode base64 images to PIL images
    images = [Image.open(io.BytesIO(base64.b64decode(img))) for img in images_base64]

    return story, images

# Fancy CSS to beautify everything in pink and dreamy style
custom_css = """
:root {
    --primary: #2563eb;
    --primary-light: #3b82f6;
    --primary-dark: #1d4ed8;
    --text: #111827;
    --text-light: #6b7280;
    --bg: #f9fafb;
    --card-bg: #ffffff;
    --border: #e5e7eb;
    --shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
    --radius: 12px;
}

body {
    background: var(--bg);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    margin: 0;
    padding: 0;
    color: var(--text);
    line-height: 1.6;
}

.gradio-container {
    padding: 2.5rem;
    max-width: 1200px;
    margin: 2rem auto;
    background-color: var(--card-bg);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    position: relative;
    overflow: hidden;
}

.gradio-container::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 8px;
    background: linear-gradient(90deg, #2563eb, #3b82f6, #9333ea);
    background-size: 200% 200%;
    animation: gradientBG 8s ease infinite;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

textarea {
    background-color: #f8fafc !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
    font-size: 0.95rem;
    color: var(--text) !important;
    resize: vertical;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    min-height: 120px;
}

textarea:focus {
    border-color: var(--primary) !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

button {
    background: linear-gradient(to right, var(--primary), var(--primary-light)) !important;
    color: white !important;
    font-size: 0.95rem;
    font-weight: 600;
    padding: 0.8rem 1.5rem !important;
    border: none !important;
    border-radius: var(--radius) !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

button:hover {
    background: linear-gradient(to right, var(--primary-dark), var(--primary)) !important;
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

button:active {
    transform: translateY(0);
}

h1, h2, .title {
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 1rem;
    color: var(--text) !important;
    text-align: center;
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    position: relative;
    display: inline-block;
    left: 50%;
    transform: translateX(-50%);
}

.description {
    font-size: 1.05rem;
    color: var(--text-light) !important;
    text-align: center;
    margin-bottom: 2rem;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
}

.output-image {
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.output-image:hover {
    transform: scale(1.02);
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
}

.gr-gallery {
    gap: 1rem !important;
    padding: 1rem !important;
}

.gr-gallery-item {
    padding: 0.5rem !important;
    border-radius: var(--radius) !important;
    overflow: hidden;
    transition: all 0.3s ease;
}

.gr-textbox, .gr-markdown, .gr-text {
    color: var(--text) !important;
    font-size: 0.95rem;
    line-height: 1.7;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #a1a1a1;
}

/* Loading animation */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Tooltip styles */
.tooltip {
    position: relative;
    display: inline-block;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 200px;
    background-color: #333;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    opacity: 0;
    transition: opacity 0.3s;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}
"""





# Gradio Interface
iface = gr.Interface(
    fn=generate_story_and_images,
    inputs=gr.Textbox(
        lines=2,
        placeholder="Type your prompt",
        label=" Your Own Prompt "
    ),
    outputs=[
        gr.Textbox(label="📜 Generated Story"),
        gr.Gallery(label="🎨  Story Book Images ", elem_classes=["output-image"], columns=3)
    ],
    title="Prompt To StoryBook ",
    description="Type a prompt! Get a short story and AI-generated images inspired by it ",
    css=custom_css
)

if __name__ == "__main__":
    iface.launch()