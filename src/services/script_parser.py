"""Script parsing to extract scenes and shots"""
import re
from typing import List, Dict, Any
from src.models.workflow import Scene, Shot
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ScriptParser:
    """Parse film scripts into scenes and shots"""
    
    def parse_script(self, script: str, job_id: str) -> List[Scene]:
        """
        Parse script into scenes with shots
        
        Expected format:
        SCENE 1: INT. LOCATION - TIME
        Description text...
        SHOT 1: Camera angle - duration (e.g., "5s")
        Shot description...
        SHOT 2: ...
        
        SCENE 2: ...
        """
        scenes = []
        
        # Split by SCENE markers
        scene_pattern = r'SCENE\s+(\d+):\s*([^\n]+)'
        scene_matches = list(re.finditer(scene_pattern, script, re.IGNORECASE))
        
        if not scene_matches:
            # If no explicit scene markers, treat entire script as one scene
            logger.warning("No scene markers found, creating single scene")
            scene = self._create_default_scene(script, job_id, 1)
            scenes.append(scene)
            return scenes
        
        for i, match in enumerate(scene_matches):
            scene_number = int(match.group(1))
            scene_header = match.group(2).strip()
            
            # Extract scene content (from this SCENE to next SCENE or end)
            start_pos = match.end()
            end_pos = scene_matches[i + 1].start() if i + 1 < len(scene_matches) else len(script)
            scene_content = script[start_pos:end_pos].strip()
            
            # Parse scene header for location and time
            location, time_of_day = self._parse_scene_header(scene_header)
            
            # Extract shots from scene content
            shots = self._parse_shots(scene_content, scene_number)
            
            # If no shots found, create a default shot
            if not shots:
                shots = [self._create_default_shot(scene_content, 1)]
            
            scene = Scene(
                job_id=job_id,
                scene_number=scene_number,
                description=scene_header,
                location=location,
                time_of_day=time_of_day,
                shots=[]  # Will be populated by shot IDs
            )
            
            # Set scene_id for shots
            for shot in shots:
                shot.scene_id = scene.id
            
            scene.shots = shots
            scenes.append(scene)
            logger.info(f"Parsed scene {scene_number} with {len(shots)} shots")
        
        return scenes
    
    def _parse_scene_header(self, header: str) -> tuple:
        """Parse scene header to extract location and time"""
        # Format: INT/EXT. LOCATION - TIME
        parts = header.split('-')
        location = parts[0].strip() if parts else header
        time_of_day = parts[1].strip() if len(parts) > 1 else None
        return location, time_of_day
    
    def _parse_shots(self, scene_content: str, scene_number: int) -> List[Shot]:
        """Parse shots from scene content"""
        shots = []
        
        shot_pattern = r'SHOT\s+(\d+):\s*([^\n]+)'
        shot_matches = list(re.finditer(shot_pattern, scene_content, re.IGNORECASE))
        
        for i, match in enumerate(shot_matches):
            shot_number = int(match.group(1))
            shot_header = match.group(2).strip()
            
            # Extract shot content
            start_pos = match.end()
            end_pos = shot_matches[i + 1].start() if i + 1 < len(shot_matches) else len(scene_content)
            shot_content = scene_content[start_pos:end_pos].strip()
            
            # Parse duration and camera angle
            duration, camera_angle = self._parse_shot_header(shot_header)
            
            shot = Shot(
                scene_id="",  # Will be set by caller
                shot_number=shot_number,
                description=shot_content or shot_header,
                duration=duration,
                camera_angle=camera_angle
            )
            shots.append(shot)
        
        return shots
    
    def _parse_shot_header(self, header: str) -> tuple:
        """Parse shot header to extract duration and camera angle"""
        duration = 5.0  # Default duration
        camera_angle = None
        
        # Look for duration pattern like "5s" or "3.5s"
        duration_match = re.search(r'(\d+\.?\d*)\s*s', header, re.IGNORECASE)
        if duration_match:
            duration = float(duration_match.group(1))
        
        # Everything else is camera angle
        camera_angle = re.sub(r'(\d+\.?\d*)\s*s', '', header, flags=re.IGNORECASE).strip()
        if not camera_angle:
            camera_angle = None
        
        return duration, camera_angle
    
    def _create_default_scene(self, script: str, job_id: str, scene_number: int) -> Scene:
        """Create a default scene from unstructured script"""
        shot = self._create_default_shot(script, 1)
        
        scene = Scene(
            job_id=job_id,
            scene_number=scene_number,
            description="Main Scene",
            location="Unknown",
            shots=[]
        )
        
        shot.scene_id = scene.id
        scene.shots = [shot]
        
        return scene
    
    def _create_default_shot(self, content: str, shot_number: int) -> Shot:
        """Create a default shot from content"""
        # Limit description length
        description = content[:500] if len(content) > 500 else content
        
        return Shot(
            scene_id="",
            shot_number=shot_number,
            description=description,
            duration=5.0,
            camera_angle="Medium Shot"
        )
