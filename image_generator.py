from diffusers import StableDiffusionPipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from io import BytesIO
import base64
import warnings
from PIL import Image

class StoryImageGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else cpu
        # Load image generation model
        self.pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained("pranavpsv/gpt2-genre-story-generator")
        self.model = AutoModelForCausalLM.from_pretrained("pranavpsv/gpt2-genre-story-generator").to(self.device)

    def generate_story(self, prompt):
        if not prompt.strip():
            prompt = "A young girl discovers a hidden magical forest behind her school and embarks on an adventure to save it."
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        output = self.model.generate(
            input_ids,
            max_length=300,
            temperature=0.9,
            top_p=0.95,
            top_k=50,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )

        story = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return story.strip()

    def split_story_into_parts(self, story, max_sentences_per_part=3):
        sentences = story.split(". ")
        parts = [".".join(sentences[i:i + max_sentences_per_part]).strip() + '.' for i in range(0, len(sentences), max_sentences_per_part)]
        return parts

    def generate_story_and_images(self, prompt):
        story = self.generate_story(prompt)
        story_parts = self.split_story_into_parts(story)

        # Ensure exactly 5 images are generated
        images = []
        num_images_needed = 5
        for idx, part in enumerate(story_parts[:num_images_needed]):  # Generate up to 5 parts
            try:
                image = self.pipe(prompt=part, num_inference_steps=50).images[0]  # Faster generation
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
                images.append(image_base64)
            except Exception as e:
                warnings.warn(f"Image generation failed for part {idx}: {e}")
                if len(images) < num_images_needed:  # Try to ensure you get 5 images
                    continue

        # Ensure 5 images even if there were errors (optional fallback image generation)
        while len(images) < num_images_needed:
            try:
                part = story_parts[len(images)] if len(story_parts) > len(images) else prompt  # Fallback to full prompt
                image = self.pipe(prompt=part, num_inference_steps=50).images[0]
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
                images.append(image_base64)
            except Exception as e:
                warnings.warn(f"Fallback image generation failed: {e}")
                break

        return story, images
