import torch
from typing import List, Optional
from PIL import Image
import os
from config import settings


class ImageGenerationPipeline:
    """Pipeline for generating images from text prompts using Stable Diffusion"""
    
    def __init__(self):
        self.device = self._get_device()
        self.model = None
        
    def _get_device(self) -> str:
        """Determine the best device to use"""
        if settings.DEVICE == "cuda" and torch.cuda.is_available():
            return "cuda"
        elif settings.DEVICE == "mps" and torch.backends.mps.is_available():
            return "mps"
        return "cpu"
    
    def load_model(self):
        """Load the image generation model (lazy loading)"""
        if self.model is not None:
            return
        
        try:
            from diffusers import StableDiffusionXLPipeline
            
            print(f"Loading image model: {settings.IMAGE_MODEL}")
            self.model = StableDiffusionXLPipeline.from_pretrained(
                settings.IMAGE_MODEL,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                use_safetensors=True,
            )
            self.model = self.model.to(self.device)
            
            if self.device == "cuda":
                self.model.enable_attention_slicing()
            
            print("Image model loaded successfully")
        except Exception as e:
            print(f"Error loading image model: {e}")
            print("Model will be loaded on first use")
    
    def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = None,
        height: int = None,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None
    ) -> Image.Image:
        """
        Generate an image from a text prompt
        
        Args:
            prompt: Text description of the image to generate
            negative_prompt: Things to avoid in the generation
            width: Image width (defaults to config)
            height: Image height (defaults to config)
            num_inference_steps: Number of denoising steps
            guidance_scale: How closely to follow the prompt
            seed: Random seed for reproducibility
            
        Returns:
            PIL Image
        """
        self.load_model()
        
        width = width or settings.IMAGE_WIDTH
        height = height or settings.IMAGE_HEIGHT
        
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        else:
            generator = None
        
        # Generate image
        result = self.model(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator,
        )
        
        return result.images[0]
    
    def generate_scene_images(
        self,
        scene_prompts: List[str],
        output_dir: str
    ) -> List[str]:
        """
        Generate images for multiple scenes
        
        Args:
            scene_prompts: List of prompts for each scene
            output_dir: Directory to save images
            
        Returns:
            List of image file paths
        """
        os.makedirs(output_dir, exist_ok=True)
        image_paths = []
        
        for i, prompt in enumerate(scene_prompts):
            print(f"Generating image {i+1}/{len(scene_prompts)}: {prompt[:50]}...")
            
            image = self.generate_image(prompt)
            
            # Save image
            image_path = os.path.join(output_dir, f"scene_{i:03d}.png")
            image.save(image_path)
            image_paths.append(image_path)
            
            print(f"Saved: {image_path}")
        
        return image_paths


# Global instance
image_pipeline = ImageGenerationPipeline()
