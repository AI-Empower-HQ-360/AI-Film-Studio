import torch
from typing import List
from PIL import Image
import os
from config import settings


class VideoGenerationPipeline:
    """Pipeline for generating videos from images"""
    
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
        """Load the video generation model (lazy loading)"""
        if self.model is not None:
            return
        
        try:
            from diffusers import StableVideoDiffusionPipeline
            
            print(f"Loading video model: {settings.VIDEO_MODEL}")
            self.model = StableVideoDiffusionPipeline.from_pretrained(
                settings.VIDEO_MODEL,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                variant="fp16" if self.device == "cuda" else None,
            )
            self.model = self.model.to(self.device)
            
            if self.device == "cuda":
                self.model.enable_attention_slicing()
            
            print("Video model loaded successfully")
        except Exception as e:
            print(f"Error loading video model: {e}")
            print("Video generation will use fallback method")
    
    def generate_video_from_image(
        self,
        image_path: str,
        output_path: str,
        num_frames: int = None,
        fps: int = None
    ) -> str:
        """
        Generate a video from a single image using motion generation
        
        Args:
            image_path: Path to input image
            output_path: Path for output video
            num_frames: Number of frames to generate
            fps: Frames per second
            
        Returns:
            Path to generated video
        """
        fps = fps or settings.VIDEO_FPS
        num_frames = num_frames or (settings.VIDEO_DURATION * fps)
        
        try:
            self.load_model()
            
            # Load image
            image = Image.open(image_path)
            
            # Generate video frames
            frames = self.model(
                image,
                num_frames=num_frames,
                decode_chunk_size=8,
            ).frames[0]
            
            # Save as video using moviepy
            from moviepy.editor import ImageSequenceClip
            clip = ImageSequenceClip([frame for frame in frames], fps=fps)
            clip.write_videofile(output_path, codec='libx264', audio=False)
            
            return output_path
            
        except Exception as e:
            print(f"Error generating video with model: {e}")
            print("Using fallback: static image to video conversion")
            return self._fallback_image_to_video(image_path, output_path, fps)
    
    def _fallback_image_to_video(
        self,
        image_path: str,
        output_path: str,
        fps: int
    ) -> str:
        """
        Fallback method: Convert static image to video
        """
        from moviepy.editor import ImageClip
        
        clip = ImageClip(image_path, duration=settings.VIDEO_DURATION)
        clip = clip.set_fps(fps)
        clip.write_videofile(output_path, codec='libx264', audio=False)
        
        return output_path
    
    def create_video_sequence(
        self,
        image_paths: List[str],
        output_path: str,
        fps: int = None
    ) -> str:
        """
        Create a video sequence from multiple images
        
        Args:
            image_paths: List of image file paths
            output_path: Path for output video
            fps: Frames per second
            
        Returns:
            Path to generated video
        """
        from moviepy.editor import ImageClip, concatenate_videoclips
        
        fps = fps or settings.VIDEO_FPS
        
        print(f"Creating video sequence from {len(image_paths)} images...")
        
        clips = []
        for image_path in image_paths:
            clip = ImageClip(image_path, duration=settings.VIDEO_DURATION)
            clip = clip.set_fps(fps)
            clips.append(clip)
        
        # Concatenate all clips
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output_path, codec='libx264', audio=False)
        
        print(f"Video saved: {output_path}")
        return output_path


# Global instance
video_pipeline = VideoGenerationPipeline()
