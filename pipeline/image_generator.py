"""Image generator worker for pipeline"""
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
from src.models.shot import Shot
from src.models.character import Character
from src.models.location import Location
from src.models.asset import Asset
from src.services.image_engine import ImageEngine
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ImageGeneratorWorker:
    """Worker for processing image generation requests"""
    
    def __init__(self, output_dir: str = "data/generated/images"):
        self.image_engine = ImageEngine()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Job queue
        self.job_queue: List[Dict[str, Any]] = []
        self.processing = False
    
    async def add_job(
        self,
        shot: Shot,
        characters: Optional[List[Character]] = None,
        location: Optional[Location] = None,
        priority: int = 0
    ) -> str:
        """Add a job to the queue"""
        job_id = f"job_{shot.id}_{shot.shot_number}"
        
        job = {
            "job_id": job_id,
            "shot": shot,
            "characters": characters or [],
            "location": location,
            "priority": priority,
            "status": "queued",
        }
        
        self.job_queue.append(job)
        self.job_queue.sort(key=lambda x: x["priority"], reverse=True)
        
        logger.info(f"Added job {job_id} to queue (priority: {priority})")
        
        return job_id
    
    async def process_queue(self):
        """Process all jobs in the queue"""
        if self.processing:
            logger.warning("Queue is already being processed")
            return
        
        self.processing = True
        logger.info(f"Starting to process {len(self.job_queue)} jobs")
        
        while self.job_queue:
            job = self.job_queue.pop(0)
            await self.process_job(job)
        
        self.processing = False
        logger.info("Finished processing queue")
    
    async def process_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single job"""
        job_id = job["job_id"]
        shot = job["shot"]
        characters = job["characters"]
        location = job["location"]
        
        logger.info(f"Processing job {job_id}")
        job["status"] = "processing"
        
        try:
            # Generate image request
            generation_request = self.image_engine.generate_shot_image(
                shot=shot,
                characters=characters,
                location=location
            )
            
            # Simulate image generation (in production, this would call actual API)
            result = await self._generate_image(generation_request)
            
            # Create asset
            asset = self.image_engine.create_asset_from_generation(
                generation_result=result,
                shot_id=shot.id
            )
            
            # Validate generation
            validation = self.image_engine.validate_generation(
                asset=asset,
                shot=shot,
                characters=characters,
                location=location
            )
            
            job["status"] = "completed"
            job["result"] = {
                "asset": asset,
                "validation": validation,
            }
            
            logger.info(f"Job {job_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Job {job_id} failed: {str(e)}")
            job["status"] = "failed"
            job["error"] = str(e)
        
        return job
    
    async def _generate_image(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate image using the specified model"""
        # This is a placeholder that simulates image generation
        # In production, this would call actual image generation APIs
        
        model_provider = request["model_config"]["provider"]
        parameters = request["parameters"]
        
        logger.info(f"Generating image with {model_provider}")
        logger.info(f"Prompt: {parameters.get('prompt', '')}")
        
        # Simulate API call delay
        await asyncio.sleep(0.5)
        
        # Generate output filename
        shot_id = request["shot_id"]
        shot_number = request["shot_number"]
        filename = f"shot_{shot_number:04d}_{shot_id}.png"
        filepath = self.output_dir / filename
        
        # In production, would download and save actual generated image
        # For now, create a placeholder file
        filepath.touch(exist_ok=True)
        
        result = {
            "url": str(filepath),
            "filename": filename,
            "prompt": parameters.get("prompt"),
            "model": model_provider,
            "parameters": parameters,
            "width": 1024,
            "height": 576,
            "status": "success",
        }
        
        logger.info(f"Image generated: {filename}")
        
        return result
    
    async def process_scene(
        self,
        shots: List[Shot],
        characters_map: Dict[str, Character],
        locations_map: Dict[str, Location]
    ) -> List[Asset]:
        """Process all shots in a scene"""
        logger.info(f"Processing scene with {len(shots)} shots")
        
        # Add all shots to queue
        for shot in shots:
            shot_characters = [
                characters_map[char_id]
                for char_id in shot.characters
                if char_id in characters_map
            ]
            location = locations_map.get(shot.location_id) if shot.location_id else None
            
            await self.add_job(
                shot=shot,
                characters=shot_characters,
                location=location
            )
        
        # Process queue
        await self.process_queue()
        
        logger.info("Scene processing completed")
        
        return []
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        return {
            "queue_length": len(self.job_queue),
            "processing": self.processing,
            "jobs": [
                {
                    "job_id": job["job_id"],
                    "status": job["status"],
                    "shot_number": job["shot"].shot_number,
                }
                for job in self.job_queue
            ]
        }


async def main():
    """Example usage of the image generator worker"""
    worker = ImageGeneratorWorker()
    
    # Create sample data
    shot = Shot(
        scene_id="scene_001",
        shot_number=1,
        shot_type="close-up",
        description="Radha and Krishna walking through flower field",
        style="cinematic",
        lighting="golden-hour",
        mood="romantic and divine",
    )
    
    character = Character(
        name="Radha",
        description="Divine character",
        appearance={
            "hair": "long black hair",
            "eyes": "dark brown eyes"
        }
    )
    
    location = Location(
        name="Vrindavan Forest",
        description="Sacred forest with flower fields",
        location_type="exterior"
    )
    
    # Process
    job_id = await worker.add_job(shot, [character], location)
    await worker.process_queue()
    
    print(f"Job {job_id} completed")


if __name__ == "__main__":
    asyncio.run(main())
