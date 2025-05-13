# Image-and-Story-Generator-Model

A multimodal AI-powered system that transforms a single text prompt into a **short fantasy story** and then illustrates it with a sequence of AI-generated images.
The result is a magical storybook experience—generated entirely by machine learning.

---

## Project Overview

**Prompt2Story2Image** is an end-to-end pipeline that combines Natural Language Processing (NLP) and image generation to:
1. Generate a fantasy short story using **GPT-2**.
2. Split the story into logical parts (2 sentences per part).
3. Generate a high-quality image for each part using **Stable Diffusion**.
4. Serve results via **gRPC** and a beautiful **Gradio UI**.

---

## Architecture
      +---------+           +----------+           +------------+
      |  Prompt |   --->    |  GPT-2   |   --->    |  Full Story|
      +---------+           +----------+           +------------+
                                                       |
                                                       v
                                               Split into Parts
                                                       |
                                                       v
                                   +---------------------------+
                                   |  Stable Diffusion (1 per) |
                                   +---------------------------+
                                                       |
                                                       v
                                    +------------------------+
                                    | Images + Full Story UI |
                                    +------------------------+


---

## Setup Instructions

### 1. Clone the Repo
```bash
git clone <your-repo-url>
cd prompt2story2image

## 2. Install Dependencies
We recommend using Docker for consistent setup.

# Option A:  Using Docker

docker build -t storybook-app .
docker run -p 50051:50051 storybook-app

# Option B:  Manual (Local) Installation
Ensure Python 3.10+, CUDA-enabled GPU (for image gen), then:

# pip install --upgrade pip
# pip install -r requirements.txt
# pip install "numpy<2" accelerate

# Then, run:

python server.py   # For gRPC server
python gradio_app.py  # For Gradio frontend

## Models Used

| Component       | Model                                  | Source                           |
| --------------- | -------------------------------------- | -------------------------------- |
| Story Generator | `pranavpsv/gpt2-genre-story-generator` | HuggingFace Transformers         |
| Image Generator | `CompVis/stable-diffusion-v1-4`        | HuggingFace Diffusers / RunwayML |


# Usage
# gRPC Client
To send a prompt and get back an image using gRPC:

python client.py

# Gradio Interface
Run the app and open your browser:

python gradio_app.py

You can enter prompts like:

"A dragon guarding a floating castle"

"An astronaut walking through a candy jungle"

You'll see:

A fantasy story
A gallery of generated images


#  File Structure

.
├── image_generator.py      # Handles story + image generation
├── server.py               # gRPC server
├── client.py               # gRPC client
├── gradio_app.py           # Gradio UI
├── texttoimg.proto         # Proto definition
├── requirements.txt
├── Dockerfile
└── README.md

## Limitations
 Heavy Resource Usage: Stable Diffusion requires a GPU with sufficient VRAM (at least 8GB).

 Loading Times: First-time model download can take several minutes.

 Story Quality: GPT-2 may produce slightly incoherent or genre-mixed stories.

 Image Relevance: Images are based on sentences, but may not perfectly match story semantics.

 Windows Warning: On Windows, symlink support is required for Hugging Face caching. If you're seeing warnings, consider enabling Developer Mode or using Linux.

# Credits
Hugging Face for GPT-2 and Diffusion models.
Diffusers for Stable Diffusion.
Gradio for the user interface.
gRPC for efficient model serving.
