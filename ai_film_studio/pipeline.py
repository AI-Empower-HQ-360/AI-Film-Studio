"""
Film Pipeline - Main orchestration for the film production pipeline.
"""

from pathlib import Path
from typing import Any

from ai_film_studio.script import ScriptParser
from ai_film_studio.scenes import SceneAnalyzer, SceneBreakdown
from ai_film_studio.shots import ShotGenerator, ShotCompositor
from ai_film_studio.video import VideoAssembler
from ai_film_studio.output import Exporter
from ai_film_studio.utils import Config, get_logger


class FilmPipeline:
    """
    Main pipeline for film production.

    Orchestrates the full pipeline: script → scenes → shots → video → MP4
    """

    def __init__(self, config: Config | None = None) -> None:
        """
        Initialize the film pipeline.

        Args:
            config: Optional configuration object.
        """
        self.config = config or Config()
        self.logger = get_logger("FilmPipeline")

        # Initialize pipeline components
        self.script_parser = ScriptParser()
        self.scene_analyzer = SceneAnalyzer()
        self.scene_breakdown = SceneBreakdown()
        self.shot_generator = ShotGenerator()
        self.shot_compositor = ShotCompositor()
        self.video_assembler = VideoAssembler()
        self.exporter = Exporter()

    def run(
        self,
        script: str | Path,
        output_name: str = "film",
        **kwargs: Any,
    ) -> Path:
        """
        Run the complete film production pipeline.

        Args:
            script: Script text or path to script file.
            output_name: Name for the output film.
            **kwargs: Additional pipeline parameters.

        Returns:
            Path to the final exported film.
        """
        self.logger.info("Starting film production pipeline...")

        # Step 1: Parse script
        self.logger.info("Step 1: Parsing script...")
        if isinstance(script, Path) or (isinstance(script, str) and Path(script).exists()):
            scenes = self.script_parser.parse_file(str(script))
        else:
            scenes = self.script_parser.parse(str(script))

        # Step 2: Analyze scenes
        self.logger.info("Step 2: Analyzing scenes...")
        scene_analysis = self.scene_analyzer.analyze_all(scenes)

        # Step 3: Break down scenes into shots
        self.logger.info("Step 3: Breaking down scenes into shots...")
        shots = self.scene_breakdown.breakdown_all(scenes)

        # Step 4: Generate shots
        self.logger.info("Step 4: Generating shots...")
        shot_files = self.shot_generator.generate_all(shots)

        # Step 5: Compose shots
        self.logger.info("Step 5: Composing shots...")
        composed_shots = self.shot_compositor.compose(shot_files)

        # Step 6: Assemble video
        self.logger.info("Step 6: Assembling video...")
        video = self.video_assembler.assemble(composed_shots, f"{output_name}.mp4")

        # Step 7: Export final video
        self.logger.info("Step 7: Exporting final video...")
        final_output = self.exporter.export(
            video,
            output_name,
            format=kwargs.get("format", "mp4"),
            quality=kwargs.get("quality", "high"),
        )

        self.logger.info(f"Film production complete! Output: {final_output}")
        return final_output

    def run_preview(self, script: str | Path, output_name: str = "preview") -> Path:
        """
        Run the pipeline and export a preview version.

        Args:
            script: Script text or path to script file.
            output_name: Name for the preview file.

        Returns:
            Path to the preview file.
        """
        return self.run(script, output_name, quality="low")
