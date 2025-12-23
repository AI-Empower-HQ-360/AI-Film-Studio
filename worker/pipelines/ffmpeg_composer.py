from typing import Optional
import subprocess
import os


class FFmpegComposer:
    """FFmpeg-based video composition and encoding"""
    
    @staticmethod
    def check_ffmpeg():
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    @staticmethod
    def compose_video_with_audio(
        video_path: str,
        audio_path: str,
        output_path: str,
        audio_volume: float = 1.0
    ) -> str:
        """
        Compose video with audio track using FFmpeg
        
        Args:
            video_path: Path to input video
            audio_path: Path to input audio
            output_path: Path for output video
            audio_volume: Audio volume multiplier
            
        Returns:
            Path to composed video
        """
        if not FFmpegComposer.check_ffmpeg():
            print("FFmpeg not found, using moviepy fallback")
            return FFmpegComposer._compose_with_moviepy(
                video_path, audio_path, output_path, audio_volume
            )
        
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-filter:a", f"volume={audio_volume}",
            "-shortest",
            "-y",
            output_path
        ]
        
        print(f"Composing video with audio using FFmpeg...")
        subprocess.run(cmd, check=True)
        print(f"Composition saved: {output_path}")
        
        return output_path
    
    @staticmethod
    def _compose_with_moviepy(
        video_path: str,
        audio_path: str,
        output_path: str,
        audio_volume: float
    ) -> str:
        """Fallback composition using moviepy"""
        from moviepy.editor import VideoFileClip, AudioFileClip
        
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        if audio_volume != 1.0:
            audio = audio.volumex(audio_volume)
        
        # Set audio to video
        final = video.set_audio(audio)
        final.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        return output_path
    
    @staticmethod
    def add_text_overlay(
        video_path: str,
        output_path: str,
        text: str,
        position: str = "center",
        fontsize: int = 48,
        color: str = "white"
    ) -> str:
        """
        Add text overlay to video using FFmpeg
        
        Args:
            video_path: Path to input video
            output_path: Path for output video
            text: Text to overlay
            position: Position (center, top, bottom)
            fontsize: Font size
            color: Text color
            
        Returns:
            Path to video with text overlay
        """
        if not FFmpegComposer.check_ffmpeg():
            print("FFmpeg not found, skipping text overlay")
            return video_path
        
        # Position mapping
        positions = {
            "center": "(w-text_w)/2:(h-text_h)/2",
            "top": "(w-text_w)/2:50",
            "bottom": "(w-text_w)/2:h-100"
        }
        
        pos = positions.get(position, positions["center"])
        
        # Escape text for FFmpeg
        text_escaped = text.replace("'", "\\'").replace(":", "\\:")
        
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"drawtext=text='{text_escaped}':fontsize={fontsize}:fontcolor={color}:x={pos.split(':')[0]}:y={pos.split(':')[1]}",
            "-codec:a", "copy",
            "-y",
            output_path
        ]
        
        print(f"Adding text overlay: {text[:30]}...")
        subprocess.run(cmd, check=True)
        
        return output_path
    
    @staticmethod
    def create_thumbnail(
        video_path: str,
        output_path: str,
        timestamp: float = 1.0
    ) -> str:
        """
        Create a thumbnail from video
        
        Args:
            video_path: Path to input video
            output_path: Path for thumbnail image
            timestamp: Time in seconds to capture frame
            
        Returns:
            Path to thumbnail
        """
        if not FFmpegComposer.check_ffmpeg():
            print("FFmpeg not found, using moviepy fallback")
            return FFmpegComposer._thumbnail_with_moviepy(
                video_path, output_path, timestamp
            )
        
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-ss", str(timestamp),
            "-vframes", "1",
            "-y",
            output_path
        ]
        
        subprocess.run(cmd, check=True)
        return output_path
    
    @staticmethod
    def _thumbnail_with_moviepy(
        video_path: str,
        output_path: str,
        timestamp: float
    ) -> str:
        """Fallback thumbnail generation using moviepy"""
        from moviepy.editor import VideoFileClip
        
        clip = VideoFileClip(video_path)
        frame = clip.get_frame(timestamp)
        
        from PIL import Image
        img = Image.fromarray(frame)
        img.save(output_path)
        
        return output_path


# Global instance
ffmpeg_composer = FFmpegComposer()
