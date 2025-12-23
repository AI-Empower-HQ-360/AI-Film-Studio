"""
Video Assembler - Assemble shots into a complete video.
"""

from pathlib import Path


class VideoAssembler:
    """Assemble individual shots into a complete video."""

    def __init__(self, output_dir: str = "./output/video") -> None:
        """
        Initialize the video assembler.

        Args:
            output_dir: Directory to save assembled videos.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def assemble(self, shots: list[Path], output_name: str = "film.mp4") -> Path:
        """
        Assemble shots into a single video.

        Args:
            shots: List of shot file paths in order.
            output_name: Name of the output video file.

        Returns:
            Path to the assembled video file.
        """
        output_path = self.output_dir / output_name
        # TODO: Implement video assembly using ffmpeg or similar
        return output_path

    def add_audio(self, video: Path, audio: Path, output_name: str | None = None) -> Path:
        """
        Add audio track to a video.

        Args:
            video: Path to the video file.
            audio: Path to the audio file.
            output_name: Optional output file name.

        Returns:
            Path to the video with audio.
        """
        if output_name is None:
            output_name = f"{video.stem}_with_audio{video.suffix}"
        output_path = self.output_dir / output_name
        # TODO: Implement audio addition
        return output_path
