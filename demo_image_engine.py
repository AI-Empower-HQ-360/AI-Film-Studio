"""Demonstration of Image Creation Engine functionality"""
import asyncio
from src.models.shot import Shot
from src.models.character import Character
from src.models.location import Location
from src.services.image_engine import ImageEngine
from pipeline.image_generator import ImageGeneratorWorker


def demonstrate_prompt_building():
    """Demonstrate prompt building capabilities"""
    print("\n" + "="*80)
    print("DEMONSTRATION: Prompt Building")
    print("="*80 + "\n")
    
    # Create a character
    character = Character(
        id="char_radha",
        name="Radha",
        description="Divine character with traditional Indian attire",
        appearance={
            "hair": "long flowing black hair",
            "eyes": "deep brown expressive eyes",
            "skin": "fair radiant complexion",
            "build": "graceful and elegant"
        },
        attire={
            "style": "traditional Indian saree",
            "colors": ["red", "gold"],
            "jewelry": ["ornate necklace", "bangles", "earrings"]
        },
        character_type="main"
    )
    
    # Create a location
    location = Location(
        id="loc_vrindavan",
        name="Vrindavan Forest",
        description="Sacred forest with vibrant flower fields",
        location_type="exterior",
        environment={
            "terrain": "flower-covered meadow",
            "vegetation": ["lotus flowers", "jasmine", "sacred trees"],
            "features": ["winding paths", "gentle streams"]
        },
        atmosphere={
            "lighting": "golden hour glow",
            "mood": "divine and peaceful"
        },
        time_of_day="dusk",
        weather="clear"
    )
    
    # Create a shot
    shot = Shot(
        id="shot_001",
        scene_id="scene_001",
        shot_number=1,
        shot_type="close-up",
        camera_angle="eye-level",
        camera_movement="slow-pan",
        description="Radha walking gracefully through the flower field",
        action="walking with serene expression",
        characters=["char_radha"],
        location_id="loc_vrindavan",
        style="cinematic",
        lighting="golden-hour",
        mood="romantic and divine",
        duration=5.0
    )
    
    # Generate image request
    engine = ImageEngine()
    request = engine.generate_shot_image(
        shot=shot,
        characters=[character],
        location=location
    )
    
    # Display results
    print("CHARACTER:")
    print(f"  Name: {character.name}")
    print(f"  Appearance: {character.appearance}")
    print(f"  Attire: {character.attire}")
    
    print("\nLOCATION:")
    print(f"  Name: {location.name}")
    print(f"  Type: {location.location_type}")
    print(f"  Time: {location.time_of_day}")
    print(f"  Environment: {location.environment}")
    
    print("\nSHOT:")
    print(f"  Type: {shot.shot_type}")
    print(f"  Style: {shot.style}")
    print(f"  Lighting: {shot.lighting}")
    print(f"  Mood: {shot.mood}")
    
    print("\nGENERATED PROMPT:")
    print(f"  {request['parameters']['prompt']}")
    
    print("\nNEGATIVE PROMPT:")
    print(f"  {request['parameters']['negative_prompt']}")
    
    print("\nMODEL CONFIGURATION:")
    print(f"  Provider: {request['model_config']['provider']}")
    print(f"  Endpoint: {request['model_config']['endpoint']}")
    
    print("\nGENERATION PARAMETERS:")
    for key, value in request['model_config']['default_params'].items():
        print(f"  {key}: {value}")


async def demonstrate_worker():
    """Demonstrate worker functionality"""
    print("\n" + "="*80)
    print("DEMONSTRATION: Image Generator Worker")
    print("="*80 + "\n")
    
    # Create worker
    worker = ImageGeneratorWorker()
    
    # Create sample shots
    shots = [
        Shot(
            id=f"shot_{i:03d}",
            scene_id="scene_001",
            shot_number=i,
            shot_type=shot_type,
            description=f"Sample shot {i}",
            style="cinematic",
            lighting="natural"
        )
        for i, shot_type in enumerate([
            "wide", "medium", "close-up"
        ], start=1)
    ]
    
    print(f"Adding {len(shots)} jobs to queue...\n")
    
    # Add jobs
    for shot in shots:
        job_id = await worker.add_job(shot=shot, priority=1)
        print(f"  Added job: {job_id}")
    
    # Show queue status
    status = worker.get_queue_status()
    print(f"\nQueue Status:")
    print(f"  Queue length: {status['queue_length']}")
    print(f"  Processing: {status['processing']}")
    
    # Process queue
    print("\nProcessing queue...")
    await worker.process_queue()
    
    # Show final status
    status = worker.get_queue_status()
    print(f"\nFinal Queue Status:")
    print(f"  Queue length: {status['queue_length']}")
    print(f"  All jobs completed!")


def demonstrate_consistency():
    """Demonstrate character and location consistency"""
    print("\n" + "="*80)
    print("DEMONSTRATION: Character & Location Consistency")
    print("="*80 + "\n")
    
    from src.services.character_consistency import CharacterConsistency
    from src.services.location_consistency import LocationConsistency
    
    # Character consistency
    char_consistency = CharacterConsistency()
    
    character = Character(
        id="char_001",
        name="Krishna",
        description="Divine character",
        appearance={"hair": "curly black hair", "eyes": "deep blue eyes"},
        seed=42,
        embedding_id="krishna_lora_v1"
    )
    
    char_consistency.register_character(character)
    params = char_consistency.get_consistency_params(character)
    
    print("CHARACTER CONSISTENCY PARAMETERS:")
    for key, value in params.items():
        if key not in ['appearance_prompt', 'attire_prompt']:
            print(f"  {key}: {value}")
    
    # Location consistency
    loc_consistency = LocationConsistency()
    
    location = Location(
        id="loc_001",
        name="Palace Courtyard",
        description="Grand palace courtyard",
        location_type="exterior",
        time_of_day="golden-hour",
        weather="clear"
    )
    
    loc_consistency.register_location(location)
    
    # Test lighting params
    lighting = loc_consistency.get_lighting_params(
        location, "golden-hour", "clear"
    )
    
    print("\nLOCATION LIGHTING PARAMETERS:")
    for key, value in lighting.items():
        print(f"  {key}: {value}")


def main():
    """Main demonstration"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  AI FILM STUDIO - IMAGE CREATION ENGINE DEMONSTRATION".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    # Run demonstrations
    demonstrate_prompt_building()
    demonstrate_consistency()
    
    # Run async demonstration
    print("\n")
    asyncio.run(demonstrate_worker())
    
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("="*80 + "\n")
    
    print("Next steps:")
    print("  1. Configure API keys in .env file")
    print("  2. Implement actual API calls in model clients")
    print("  3. Set up image storage (S3, etc.)")
    print("  4. Configure database for asset tracking")
    print("\nSee IMAGE_ENGINE.md for full documentation.\n")


if __name__ == "__main__":
    main()
