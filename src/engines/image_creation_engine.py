"""
Image Creation Engine
Comprehensive image generation for all age groups, genders, cultures, animals, locations, and dress types
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
import logging
import asyncio

# Import datetime for default_factory
from datetime import datetime as dt

# Handle optional pydantic import
try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            annotations = getattr(self.__class__, '__annotations__', {})
            for key, value in kwargs.items():
                setattr(self, key, value)
            for key, field_type in annotations.items():
                if not hasattr(self, key):
                    field_value = getattr(self.__class__, key, None)
                    if callable(field_value):
                        setattr(self, key, field_value())
                    elif field_value is None and key in ['image_id', 'job_id']:
                        setattr(self, key, str(uuid.uuid4()))
                    elif field_value is None and key in ['created_at']:
                        setattr(self, key, datetime.utcnow())
                    elif field_value is None and key in ['metadata']:
                        setattr(self, key, {})
    
    def Field(default=..., default_factory=None, **kwargs):
        if default_factory is not None:
            return default_factory
        if default is not ...:
            return default
        return None

logger = logging.getLogger(__name__)


# Age Groups
class AgeGroup:
    """Age group categories"""
    INFANT = "0-3"
    CHILD = "4-8"
    PRE_TEEN = "8-12"
    TEEN = "13-19"
    YOUNG_ADULT = "20-21"
    ADULT = "22-35"
    MIDDLE_AGE = "35-50"
    SENIOR = "50+"


# Gender Options
class Gender:
    """Gender options"""
    BOY = "boy"
    GIRL = "girl"
    MAN = "man"
    WOMAN = "woman"
    NON_BINARY = "non_binary"
    CHILD = "child"  # Gender-neutral for children


# Cultural Regions
class CulturalRegion:
    """Cultural and regional categories"""
    # South Asian
    SOUTH_INDIAN = "south_indian"
    NORTH_INDIAN = "north_indian"
    BENGALI = "bengali"
    PUNJABI = "punjabi"
    GUJARATI = "gujarati"
    MARATHI = "marathi"
    
    # East Asian
    CHINESE = "chinese"
    JAPANESE = "japanese"
    KOREAN = "korean"
    VIETNAMESE = "vietnamese"
    THAI = "thai"
    
    # Western
    AMERICAN = "american"
    EUROPEAN = "european"
    BRITISH = "british"
    LATIN_AMERICAN = "latin_american"
    
    # Middle Eastern
    ARABIC = "arabic"
    PERSIAN = "persian"
    TURKISH = "turkish"
    
    # African
    AFRICAN = "african"
    ETHIOPIAN = "ethiopian"
    NIGERIAN = "nigerian"
    
    # Other
    MIXED = "mixed"
    UNIVERSAL = "universal"


# Body Types
class BodyType:
    """Body type categories"""
    SLIM = "slim"
    AVERAGE = "average"
    ATHLETIC = "athletic"
    CURVY = "curvy"
    MUSCULAR = "muscular"
    PLUS_SIZE = "plus_size"
    PETITE = "petite"
    TALL = "tall"
    SHORT = "short"


# Character Types
class CharacterType:
    """Character and deity types"""
    KRISHNA = "krishna"
    RADHA = "radha"
    SHIVA = "shiva"
    PARVATI = "parvati"
    GANESHA = "ganesha"
    LAKSHMI = "lakshmi"
    SARASWATI = "saraswati"
    HANUMAN = "hanuman"
    RAMA = "rama"
    SITA = "sita"
    DURGA = "durga"
    KALI = "kali"
    BUDDHA = "buddha"
    JESUS = "jesus"
    ANGEL = "angel"
    FAIRY = "fairy"
    PRINCE = "prince"
    PRINCESS = "princess"
    WARRIOR = "warrior"
    SAGE = "sage"
    MONK = "monk"
    NUN = "nun"
    GENERIC_CHARACTER = "generic_character"


# Dress Types
class DressType:
    """Dress and clothing types"""
    # Traditional
    TRADITIONAL = "traditional"
    ETHNIC = "ethnic"
    CULTURAL = "cultural"
    
    # Modern
    CASUAL = "casual"
    FORMAL = "formal"
    BUSINESS = "business"
    SPORTS = "sports"
    PARTY = "party"
    WEDDING = "wedding"
    FESTIVAL = "festival"
    
    # Regional Traditional
    SARI = "sari"
    KURTA = "kurta"
    DHOTI = "dhoti"
    KIMONO = "kimono"
    HANBOK = "hanbok"
    ABAYA = "abaya"
    DASHIKI = "dashiki"
    
    # Western
    SUIT = "suit"
    DRESS = "dress"
    JEANS = "jeans"
    T_SHIRT = "t_shirt"
    
    # Children
    PLAY_CLOTHES = "play_clothes"
    SCHOOL_UNIFORM = "school_uniform"
    FESTIVE = "festive"
    
    # Character-specific
    KRISHNA_ATTIRE = "krishna_attire"  # Yellow dhoti, peacock feather, flute
    RADHA_ATTIRE = "radha_attire"  # Traditional lehenga, dupatta
    DEITY_ATTIRE = "deity_attire"  # Traditional deity clothing
    SAINT_ATTIRE = "saint_attire"  # Simple, spiritual clothing


# Location Types
class LocationType:
    """Location and setting types"""
    # Indoor
    HOME = "home"
    TEMPLE = "temple"
    OFFICE = "office"
    SCHOOL = "school"
    HOSPITAL = "hospital"
    RESTAURANT = "restaurant"
    MARKET = "market"
    
    # Outdoor
    GARDEN = "garden"
    BEACH = "beach"
    MOUNTAIN = "mountain"
    FOREST = "forest"
    DESERT = "desert"
    VILLAGE = "village"
    CITY = "city"
    PARK = "park"
    
    # Cultural
    TEMPLE_COURTYARD = "temple_courtyard"
    FESTIVAL_GROUND = "festival_ground"
    WEDDING_VENUE = "wedding_venue"
    
    # Natural
    OCEAN = "ocean"
    RIVER = "river"
    FIELD = "field"
    FARM = "farm"


# Animal Categories
class AnimalCategory:
    """Animal categories"""
    # Domestic
    DOG = "dog"
    CAT = "cat"
    COW = "cow"
    GOAT = "goat"
    SHEEP = "sheep"
    HORSE = "horse"
    CHICKEN = "chicken"
    DUCK = "duck"
    
    # Wild - Land
    LION = "lion"
    TIGER = "tiger"
    ELEPHANT = "elephant"
    BEAR = "bear"
    WOLF = "wolf"
    DEER = "deer"
    MONKEY = "monkey"
    RABBIT = "rabbit"
    
    # Wild - Birds
    PEACOCK = "peacock"
    EAGLE = "eagle"
    PARROT = "parrot"
    OWL = "owl"
    SWAN = "swan"
    
    # Wild - Water
    DOLPHIN = "dolphin"
    WHALE = "whale"
    FISH = "fish"
    TURTLE = "turtle"
    
    # Wild - Exotic
    PANDA = "panda"
    GIRAFFE = "giraffe"
    ZEBRA = "zebra"
    KANGAROO = "kangaroo"
    PENGUIN = "penguin"


class ImageGenerationRequest(BaseModel):
    """Request model for image generation"""
    prompt: str = Field(..., description="Base image description")
    age_group: Optional[str] = Field(default=None, description="Age group (0-3, 4-8, 8-12, 13-19, 20-21, 22-35, 35-50, 50+)")
    gender: Optional[str] = Field(default=None, description="Gender (boy, girl, man, woman, child, non_binary)")
    cultural_region: Optional[str] = Field(default=None, description="Cultural region")
    body_type: Optional[str] = Field(default=None, description="Body type")
    dress_type: Optional[str] = Field(default=None, description="Dress/clothing type")
    location: Optional[str] = Field(default=None, description="Location/setting")
    animal_type: Optional[str] = Field(default=None, description="Animal type (if generating animal)")
    character_type: Optional[str] = Field(default=None, description="Character type (krishna, radha, etc.)")
    character_name: Optional[str] = Field(default=None, description="Name to overlay on image")
    name_meaning: Optional[str] = Field(default=None, description="Meaning of the name (for overlay)")
    accessories: Optional[List[str]] = Field(default=None, description="List of accessories (crown, peacock_feather, jewelry, etc.)")
    pose: Optional[str] = Field(default=None, description="Pose (standing, sitting, playing_flute, etc.)")
    expression: Optional[str] = Field(default=None, description="Expression (smiling, serene, joyful, etc.)")
    style: str = Field(default="realistic", description="Image style (realistic, artistic, cinematic, traditional)")
    resolution: str = Field(default="1024x1024", description="Image resolution")
    num_images: int = Field(default=1, ge=1, le=4, description="Number of images to generate")
    seed: Optional[int] = Field(default=None, description="Random seed for reproducibility")
    negative_prompt: Optional[str] = Field(default=None, description="Things to avoid in image")
    cultural_context: Optional[Dict[str, Any]] = Field(default=None, description="Additional cultural context")
    include_name_overlay: bool = Field(default=False, description="Include name overlay on image")


class GeneratedImage(BaseModel):
    """Generated image model"""
    image_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    url: str = Field(..., description="S3 URL or base64 data URL")
    prompt: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ImageCreationEngine:
    """
    Image Creation Engine
    
    Generates images for:
    - All age groups (0-3, 4-8, 8-12, teens, 20-21, 22-35, 35-50, 50+)
    - All genders (boys, girls, men, women, non-binary)
    - All cultures and ethnicities
    - All types of animals
    - Different body types
    - Different locations and settings
    - Different dress types
    """
    
    def __init__(self):
        self.generated_images: Dict[str, GeneratedImage] = {}
        self.active_jobs: Dict[str, Any] = {}
    
    def _build_enhanced_prompt(self, request: ImageGenerationRequest) -> str:
        """
        Build enhanced prompt with all parameters
        
        Args:
            request: Image generation request
            
        Returns:
            Enhanced prompt string
        """
        prompt_parts = []
        
        # Character type takes precedence
        if request.character_type:
            character_descriptions = {
                CharacterType.KRISHNA: "Lord Krishna",
                CharacterType.RADHA: "Radha",
                CharacterType.SHIVA: "Lord Shiva",
                CharacterType.PARVATI: "Goddess Parvati",
                CharacterType.GANESHA: "Lord Ganesha",
                CharacterType.LAKSHMI: "Goddess Lakshmi",
                CharacterType.SARASWATI: "Goddess Saraswati",
                CharacterType.HANUMAN: "Lord Hanuman",
                CharacterType.RAMA: "Lord Rama",
                CharacterType.SITA: "Goddess Sita",
                CharacterType.DURGA: "Goddess Durga",
                CharacterType.KALI: "Goddess Kali",
                CharacterType.BUDDHA: "Buddha",
                CharacterType.JESUS: "Jesus Christ",
                CharacterType.ANGEL: "angel",
                CharacterType.FAIRY: "fairy",
                CharacterType.PRINCE: "prince",
                CharacterType.PRINCESS: "princess",
                CharacterType.WARRIOR: "warrior",
                CharacterType.SAGE: "sage",
                CharacterType.MONK: "monk",
                CharacterType.NUN: "nun"
            }
            character_desc = character_descriptions.get(request.character_type, request.character_type)
            prompt_parts.append(character_desc)
        else:
            # Use base prompt if no character type
            prompt_parts.append(request.prompt)
        
        # Add age group description
        if request.age_group:
            age_descriptions = {
                AgeGroup.INFANT: "baby or infant (0-3 years old)",
                AgeGroup.CHILD: "young child (4-8 years old)",
                AgeGroup.PRE_TEEN: "pre-teen child (8-12 years old)",
                AgeGroup.TEEN: "teenager (13-19 years old)",
                AgeGroup.YOUNG_ADULT: "young adult (20-21 years old)",
                AgeGroup.ADULT: "adult (22-35 years old)",
                AgeGroup.MIDDLE_AGE: "middle-aged person (35-50 years old)",
                AgeGroup.SENIOR: "senior person (50+ years old)"
            }
            prompt_parts.append(age_descriptions.get(request.age_group, request.age_group))
        
        # Add gender
        if request.gender:
            prompt_parts.append(request.gender)
        
        # Add cultural/ethnic description
        if request.cultural_region:
            cultural_descriptions = {
                CulturalRegion.SOUTH_INDIAN: "South Indian features and appearance",
                CulturalRegion.NORTH_INDIAN: "North Indian features and appearance",
                CulturalRegion.BENGALI: "Bengali features and appearance",
                CulturalRegion.CHINESE: "Chinese features and appearance",
                CulturalRegion.JAPANESE: "Japanese features and appearance",
                CulturalRegion.KOREAN: "Korean features and appearance",
                CulturalRegion.AMERICAN: "American features and appearance",
                CulturalRegion.EUROPEAN: "European features and appearance",
                CulturalRegion.ARABIC: "Arabic/Middle Eastern features and appearance",
                CulturalRegion.AFRICAN: "African features and appearance",
            }
            desc = cultural_descriptions.get(request.cultural_region, request.cultural_region)
            prompt_parts.append(desc)
        
        # Add body type
        if request.body_type:
            prompt_parts.append(f"{request.body_type} body type")
        
        # Add character-specific attire
        if request.character_type:
            if request.character_type == CharacterType.KRISHNA:
                prompt_parts.append("wearing yellow dhoti, golden crown with peacock feather, golden jewelry, holding flute")
            elif request.character_type == CharacterType.RADHA:
                prompt_parts.append("wearing traditional lehenga with dupatta, golden jewelry, crown")
            elif request.character_type in [CharacterType.SHIVA, CharacterType.PARVATI, CharacterType.GANESHA]:
                prompt_parts.append("wearing traditional deity attire with elaborate jewelry and ornaments")
        elif request.dress_type:
            dress_descriptions = {
                DressType.SARI: "wearing traditional sari",
                DressType.KURTA: "wearing kurta",
                DressType.DHOTI: "wearing dhoti",
                DressType.KIMONO: "wearing kimono",
                DressType.SUIT: "wearing formal suit",
                DressType.CASUAL: "wearing casual clothes",
                DressType.TRADITIONAL: "wearing traditional attire",
                DressType.FESTIVAL: "wearing festival clothes",
                DressType.WEDDING: "wearing wedding attire",
                DressType.KRISHNA_ATTIRE: "wearing yellow dhoti, golden crown with peacock feather, golden jewelry",
                DressType.RADHA_ATTIRE: "wearing traditional lehenga with dupatta, golden jewelry",
                DressType.DEITY_ATTIRE: "wearing traditional deity attire with elaborate jewelry",
                DressType.SAINT_ATTIRE: "wearing simple, spiritual clothing"
            }
            desc = dress_descriptions.get(request.dress_type, f"wearing {request.dress_type}")
            prompt_parts.append(desc)
        
        # Add accessories
        if request.accessories:
            accessories_desc = ", ".join(request.accessories)
            prompt_parts.append(f"with {accessories_desc}")
        
        # Add pose
        if request.pose:
            pose_descriptions = {
                "standing": "standing gracefully",
                "sitting": "sitting cross-legged",
                "playing_flute": "playing flute",
                "blessing": "hand raised in blessing gesture",
                "meditating": "in meditation pose",
                "dancing": "dancing",
                "smiling": "smiling joyfully",
                "serene": "serene expression"
            }
            pose_desc = pose_descriptions.get(request.pose, request.pose)
            prompt_parts.append(pose_desc)
        
        # Add expression
        if request.expression:
            prompt_parts.append(f"{request.expression} expression")
        
        # Add location/setting
        if request.location:
            location_descriptions = {
                LocationType.TEMPLE: "at a temple",
                LocationType.BEACH: "at the beach",
                LocationType.GARDEN: "in a garden",
                LocationType.OCEAN: "by the ocean",
                LocationType.TEMPLE_COURTYARD: "in a temple courtyard",
                LocationType.FESTIVAL_GROUND: "at a festival ground",
                LocationType.HOME: "at home",
                LocationType.OFFICE: "in an office"
            }
            desc = location_descriptions.get(request.location, f"at {request.location}")
            prompt_parts.append(desc)
        
        # Add animal type (if generating animal)
        if request.animal_type:
            prompt_parts.append(f"{request.animal_type}")
        
        # Add style
        if request.style:
            style_descriptions = {
                "realistic": "photorealistic, high quality, detailed",
                "artistic": "artistic style, painterly, vibrant colors",
                "cinematic": "cinematic lighting, dramatic, professional photography",
                "traditional": "traditional art style, classical Indian art"
            }
            prompt_parts.append(style_descriptions.get(request.style, request.style))
        
        return ", ".join(prompt_parts)
    
    async def generate_image(
        self,
        request: ImageGenerationRequest | Dict[str, Any],
        job_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate image(s) based on comprehensive parameters
        
        Args:
            request: Image generation request (typed or dict)
            job_id: Optional job ID for tracking
            
        Returns:
            Dictionary with generated image URLs and metadata
        """
        try:
            # Handle dict input for test compatibility
            if isinstance(request, dict):
                request = ImageGenerationRequest(**request)
            
            if not job_id:
                job_id = f"img_{uuid.uuid4().hex[:12]}"
            
            logger.info(f"Starting image generation for job {job_id}")
            
            # Store job
            self.active_jobs[job_id] = {
                "status": "processing",
                "start_time": asyncio.get_event_loop().time(),
                "request": request
            }
            
            # Build enhanced prompt
            enhanced_prompt = self._build_enhanced_prompt(request)
            
            # Import AI services
            try:
                from src.services.ai.stability_service import StabilityService
                from src.services.ai.openai_service import OpenAIService
            except ImportError:
                logger.warning("AI services not available, using mock generation")
                # Mock generation for testing
                images = []
                for i in range(request.num_images):
                    image_id = str(uuid.uuid4())
                    image = GeneratedImage(
                        image_id=image_id,
                        url=f"s3://ai-film-studio-assets/images/{job_id}/{image_id}.png",
                        prompt=enhanced_prompt,
                        metadata={
                            "age_group": request.age_group,
                            "gender": request.gender,
                            "cultural_region": request.cultural_region,
                            "body_type": request.body_type,
                            "dress_type": request.dress_type,
                            "location": request.location,
                            "animal_type": request.animal_type,
                            "character_type": request.character_type,
                            "character_name": request.character_name,
                            "name_meaning": request.name_meaning,
                            "accessories": request.accessories,
                            "pose": request.pose,
                            "expression": request.expression,
                            "style": request.style,
                            "include_name_overlay": request.include_name_overlay
                        }
                    )
                    self.generated_images[image_id] = image
                    images.append(image)
                
                processing_time = asyncio.get_event_loop().time() - self.active_jobs[job_id]["start_time"]
                self.active_jobs[job_id]["status"] = "completed"
                
                result_data = {
                    "job_id": job_id,
                    "status": "completed",
                    "images": [{"image_id": img.image_id, "url": img.url, "metadata": img.metadata} for img in images],
                    "prompt": enhanced_prompt,
                    "processing_time": processing_time
                }
                
                # Add name overlay information if requested
                if request.include_name_overlay and request.character_name:
                    result_data["name_overlay"] = {
                        "name": request.character_name,
                        "meaning": request.name_meaning,
                        "style": "pink_rectangular_box",
                        "position": "center_chest"
                    }
                
                return result_data
            
            # Use Stability AI or OpenAI based on style
            images = []
            if request.style in ["realistic", "cinematic"]:
                stability_service = StabilityService()
                for i in range(request.num_images):
                    result = await stability_service.generate_image(
                        prompt=enhanced_prompt,
                        style=request.style,
                        width=int(request.resolution.split('x')[0]),
                        height=int(request.resolution.split('x')[1])
                    )
                    image_id = str(uuid.uuid4())
                    image = GeneratedImage(
                        image_id=image_id,
                        url=result.get("url", f"s3://ai-film-studio-assets/images/{job_id}/{image_id}.png"),
                        prompt=enhanced_prompt,
                        metadata={
                            "age_group": request.age_group,
                            "gender": request.gender,
                            "cultural_region": request.cultural_region,
                            "body_type": request.body_type,
                            "dress_type": request.dress_type,
                            "location": request.location,
                            "animal_type": request.animal_type,
                            "character_type": request.character_type,
                            "character_name": request.character_name,
                            "name_meaning": request.name_meaning,
                            "accessories": request.accessories,
                            "pose": request.pose,
                            "expression": request.expression,
                            "style": request.style,
                            "provider": "stability_ai",
                            "include_name_overlay": request.include_name_overlay
                        }
                    )
                    self.generated_images[image_id] = image
                    images.append(image)
            else:
                # Use OpenAI DALL-E for artistic styles
                openai_service = OpenAIService()
                for i in range(request.num_images):
                    result = await openai_service.generate_image(
                        prompt=enhanced_prompt,
                        model="dall-e-3",
                        size=request.resolution,
                        quality="standard"
                    )
                    image_id = str(uuid.uuid4())
                    image = GeneratedImage(
                        image_id=image_id,
                        url=result.get("url", f"s3://ai-film-studio-assets/images/{job_id}/{image_id}.png"),
                        prompt=enhanced_prompt,
                        metadata={
                            "age_group": request.age_group,
                            "gender": request.gender,
                            "cultural_region": request.cultural_region,
                            "body_type": request.body_type,
                            "dress_type": request.dress_type,
                            "location": request.location,
                            "animal_type": request.animal_type,
                            "character_type": request.character_type,
                            "character_name": request.character_name,
                            "name_meaning": request.name_meaning,
                            "accessories": request.accessories,
                            "pose": request.pose,
                            "expression": request.expression,
                            "style": request.style,
                            "provider": "openai_dalle",
                            "include_name_overlay": request.include_name_overlay
                        }
                    )
                    self.generated_images[image_id] = image
                    images.append(image)
            
            processing_time = asyncio.get_event_loop().time() - self.active_jobs[job_id]["start_time"]
            self.active_jobs[job_id]["status"] = "completed"
            
            result_data = {
                "job_id": job_id,
                "status": "completed",
                "images": [{"image_id": img.image_id, "url": img.url, "metadata": img.metadata} for img in images],
                "prompt": enhanced_prompt,
                "processing_time": processing_time
            }
            
            # Add name overlay information if requested
            if request.include_name_overlay and request.character_name:
                result_data["name_overlay"] = {
                    "name": request.character_name,
                    "meaning": request.name_meaning,
                    "style": "pink_rectangular_box",
                    "position": "center_chest"
                }
            
            return result_data
            
        except Exception as e:
            logger.error(f"Error generating image for job {job_id}: {str(e)}")
            if job_id and job_id in self.active_jobs:
                self.active_jobs[job_id]["status"] = "failed"
            
            return {
                "job_id": job_id or "unknown",
                "status": "failed",
                "error_message": str(e)
            }
    
    def get_supported_age_groups(self) -> List[Dict[str, Any]]:
        """Get list of supported age groups"""
        return [
            {"value": AgeGroup.INFANT, "label": "Infant (0-3 years)", "description": "Babies and toddlers"},
            {"value": AgeGroup.CHILD, "label": "Child (4-8 years)", "description": "Young children"},
            {"value": AgeGroup.PRE_TEEN, "label": "Pre-teen (8-12 years)", "description": "Older children"},
            {"value": AgeGroup.TEEN, "label": "Teenager (13-19 years)", "description": "Teenagers"},
            {"value": AgeGroup.YOUNG_ADULT, "label": "Young Adult (20-21 years)", "description": "Young adults"},
            {"value": AgeGroup.ADULT, "label": "Adult (22-35 years)", "description": "Adults"},
            {"value": AgeGroup.MIDDLE_AGE, "label": "Middle Age (35-50 years)", "description": "Middle-aged"},
            {"value": AgeGroup.SENIOR, "label": "Senior (50+ years)", "description": "Senior citizens"}
        ]
    
    def get_supported_genders(self) -> List[Dict[str, Any]]:
        """Get list of supported gender options"""
        return [
            {"value": Gender.BOY, "label": "Boy"},
            {"value": Gender.GIRL, "label": "Girl"},
            {"value": Gender.MAN, "label": "Man"},
            {"value": Gender.WOMAN, "label": "Woman"},
            {"value": Gender.CHILD, "label": "Child (gender-neutral)"},
            {"value": Gender.NON_BINARY, "label": "Non-binary"}
        ]
    
    def get_supported_cultures(self) -> List[Dict[str, Any]]:
        """Get list of supported cultural regions"""
        return [
            {"value": CulturalRegion.SOUTH_INDIAN, "label": "South Indian"},
            {"value": CulturalRegion.NORTH_INDIAN, "label": "North Indian"},
            {"value": CulturalRegion.BENGALI, "label": "Bengali"},
            {"value": CulturalRegion.PUNJABI, "label": "Punjabi"},
            {"value": CulturalRegion.CHINESE, "label": "Chinese"},
            {"value": CulturalRegion.JAPANESE, "label": "Japanese"},
            {"value": CulturalRegion.KOREAN, "label": "Korean"},
            {"value": CulturalRegion.AMERICAN, "label": "American"},
            {"value": CulturalRegion.EUROPEAN, "label": "European"},
            {"value": CulturalRegion.ARABIC, "label": "Arabic/Middle Eastern"},
            {"value": CulturalRegion.AFRICAN, "label": "African"},
            {"value": CulturalRegion.LATIN_AMERICAN, "label": "Latin American"},
            {"value": CulturalRegion.MIXED, "label": "Mixed Heritage"},
            {"value": CulturalRegion.UNIVERSAL, "label": "Universal"}
        ]
    
    def get_supported_animals(self) -> List[Dict[str, Any]]:
        """Get list of supported animal types"""
        return [
            {"value": AnimalCategory.DOG, "label": "Dog"},
            {"value": AnimalCategory.CAT, "label": "Cat"},
            {"value": AnimalCategory.COW, "label": "Cow"},
            {"value": AnimalCategory.PEACOCK, "label": "Peacock"},
            {"value": AnimalCategory.ELEPHANT, "label": "Elephant"},
            {"value": AnimalCategory.LION, "label": "Lion"},
            {"value": AnimalCategory.TIGER, "label": "Tiger"},
            {"value": AnimalCategory.DOLPHIN, "label": "Dolphin"},
            {"value": AnimalCategory.PANDA, "label": "Panda"},
            {"value": AnimalCategory.HORSE, "label": "Horse"},
            # Add more as needed
        ]
    
    def get_supported_body_types(self) -> List[Dict[str, Any]]:
        """Get list of supported body types"""
        return [
            {"value": BodyType.SLIM, "label": "Slim"},
            {"value": BodyType.AVERAGE, "label": "Average"},
            {"value": BodyType.ATHLETIC, "label": "Athletic"},
            {"value": BodyType.CURVY, "label": "Curvy"},
            {"value": BodyType.MUSCULAR, "label": "Muscular"},
            {"value": BodyType.PLUS_SIZE, "label": "Plus Size"},
            {"value": BodyType.PETITE, "label": "Petite"},
            {"value": BodyType.TALL, "label": "Tall"},
            {"value": BodyType.SHORT, "label": "Short"}
        ]
    
    def get_supported_character_types(self) -> List[Dict[str, Any]]:
        """Get list of supported character types"""
        return [
            {"value": CharacterType.KRISHNA, "label": "Lord Krishna", "description": "Hindu deity with peacock feather and flute"},
            {"value": CharacterType.RADHA, "label": "Radha", "description": "Consort of Krishna"},
            {"value": CharacterType.SHIVA, "label": "Lord Shiva", "description": "Hindu deity"},
            {"value": CharacterType.PARVATI, "label": "Goddess Parvati", "description": "Hindu goddess"},
            {"value": CharacterType.GANESHA, "label": "Lord Ganesha", "description": "Elephant-headed deity"},
            {"value": CharacterType.LAKSHMI, "label": "Goddess Lakshmi", "description": "Goddess of wealth"},
            {"value": CharacterType.SARASWATI, "label": "Goddess Saraswati", "description": "Goddess of knowledge"},
            {"value": CharacterType.HANUMAN, "label": "Lord Hanuman", "description": "Monkey god"},
            {"value": CharacterType.RAMA, "label": "Lord Rama", "description": "Hindu deity"},
            {"value": CharacterType.SITA, "label": "Goddess Sita", "description": "Consort of Rama"},
            {"value": CharacterType.DURGA, "label": "Goddess Durga", "description": "Warrior goddess"},
            {"value": CharacterType.KALI, "label": "Goddess Kali", "description": "Goddess of time"},
            {"value": CharacterType.BUDDHA, "label": "Buddha", "description": "Enlightened one"},
            {"value": CharacterType.JESUS, "label": "Jesus Christ", "description": "Christian deity"},
            {"value": CharacterType.ANGEL, "label": "Angel", "description": "Celestial being"},
            {"value": CharacterType.FAIRY, "label": "Fairy", "description": "Mythical being"},
            {"value": CharacterType.PRINCE, "label": "Prince", "description": "Royal character"},
            {"value": CharacterType.PRINCESS, "label": "Princess", "description": "Royal character"},
            {"value": CharacterType.WARRIOR, "label": "Warrior", "description": "Fighter character"},
            {"value": CharacterType.SAGE, "label": "Sage", "description": "Wise person"},
            {"value": CharacterType.MONK, "label": "Monk", "description": "Religious figure"},
            {"value": CharacterType.NUN, "label": "Nun", "description": "Religious figure"},
            {"value": CharacterType.GENERIC_CHARACTER, "label": "Generic Character", "description": "Custom character"}
        ]
    
    def get_supported_dress_types(self) -> List[Dict[str, Any]]:
        """Get list of supported dress types"""
        return [
            {"value": DressType.TRADITIONAL, "label": "Traditional"},
            {"value": DressType.SARI, "label": "Sari"},
            {"value": DressType.KURTA, "label": "Kurta"},
            {"value": DressType.DHOTI, "label": "Dhoti"},
            {"value": DressType.KIMONO, "label": "Kimono"},
            {"value": DressType.CASUAL, "label": "Casual"},
            {"value": DressType.FORMAL, "label": "Formal"},
            {"value": DressType.SUIT, "label": "Suit"},
            {"value": DressType.WEDDING, "label": "Wedding Attire"},
            {"value": DressType.FESTIVAL, "label": "Festival Clothes"},
            {"value": DressType.SPORTS, "label": "Sports Wear"},
            {"value": DressType.PLAY_CLOTHES, "label": "Play Clothes (Children)"},
            {"value": DressType.KRISHNA_ATTIRE, "label": "Krishna Attire", "description": "Yellow dhoti, peacock feather, golden jewelry"},
            {"value": DressType.RADHA_ATTIRE, "label": "Radha Attire", "description": "Traditional lehenga with dupatta"},
            {"value": DressType.DEITY_ATTIRE, "label": "Deity Attire", "description": "Traditional deity clothing"},
            {"value": DressType.SAINT_ATTIRE, "label": "Saint Attire", "description": "Simple, spiritual clothing"}
        ]
    
    def get_supported_accessories(self) -> List[Dict[str, Any]]:
        """Get list of supported accessories"""
        return [
            {"value": "crown", "label": "Crown", "description": "Golden crown"},
            {"value": "peacock_feather", "label": "Peacock Feather", "description": "Peacock feather in crown"},
            {"value": "jewelry", "label": "Jewelry", "description": "Golden jewelry"},
            {"value": "necklace", "label": "Necklace", "description": "Golden necklace"},
            {"value": "bangles", "label": "Bangles", "description": "Golden bangles"},
            {"value": "anklets", "label": "Anklets", "description": "Golden anklets"},
            {"value": "armlets", "label": "Armlets", "description": "Golden armlets"},
            {"value": "earrings", "label": "Earrings", "description": "Golden earrings"},
            {"value": "flute", "label": "Flute", "description": "Bamboo flute"},
            {"value": "garland", "label": "Garland", "description": "Flower garland"},
            {"value": "tilak", "label": "Tilak", "description": "Forehead mark"},
            {"value": "dupatta", "label": "Dupatta", "description": "Traditional scarf"},
            {"value": "mala", "label": "Mala", "description": "Prayer beads"}
        ]
    
    def get_supported_poses(self) -> List[Dict[str, Any]]:
        """Get list of supported poses"""
        return [
            {"value": "standing", "label": "Standing", "description": "Standing gracefully"},
            {"value": "sitting", "label": "Sitting", "description": "Sitting cross-legged"},
            {"value": "playing_flute", "label": "Playing Flute", "description": "Holding and playing flute"},
            {"value": "blessing", "label": "Blessing", "description": "Hand raised in blessing"},
            {"value": "meditating", "label": "Meditating", "description": "In meditation pose"},
            {"value": "dancing", "label": "Dancing", "description": "Dancing pose"},
            {"value": "smiling", "label": "Smiling", "description": "Smiling joyfully"},
            {"value": "serene", "label": "Serene", "description": "Serene expression"},
            {"value": "laughing", "label": "Laughing", "description": "Laughing heartily"},
            {"value": "looking_up", "label": "Looking Up", "description": "Looking upwards"},
            {"value": "looking_at_camera", "label": "Looking at Camera", "description": "Direct eye contact"}
        ]
    
    def get_supported_expressions(self) -> List[Dict[str, Any]]:
        """Get list of supported expressions"""
        return [
            {"value": "smiling", "label": "Smiling", "description": "Warm smile"},
            {"value": "joyful", "label": "Joyful", "description": "Very happy"},
            {"value": "serene", "label": "Serene", "description": "Peaceful"},
            {"value": "laughing", "label": "Laughing", "description": "Laughing"},
            {"value": "blessing", "label": "Blessing", "description": "Blessing expression"},
            {"value": "meditative", "label": "Meditative", "description": "Deep meditation"},
            {"value": "playful", "label": "Playful", "description": "Playful and fun"},
            {"value": "divine", "label": "Divine", "description": "Divine aura"},
            {"value": "innocent", "label": "Innocent", "description": "Innocent expression"},
            {"value": "wise", "label": "Wise", "description": "Wise and knowing"}
        ]
    
    def get_supported_locations(self) -> List[Dict[str, Any]]:
        """Get list of supported locations"""
        return [
            {"value": LocationType.HOME, "label": "Home"},
            {"value": LocationType.TEMPLE, "label": "Temple"},
            {"value": LocationType.TEMPLE_COURTYARD, "label": "Temple Courtyard"},
            {"value": LocationType.BEACH, "label": "Beach"},
            {"value": LocationType.OCEAN, "label": "Ocean"},
            {"value": LocationType.GARDEN, "label": "Garden"},
            {"value": LocationType.PARK, "label": "Park"},
            {"value": LocationType.MOUNTAIN, "label": "Mountain"},
            {"value": LocationType.FOREST, "label": "Forest"},
            {"value": LocationType.CITY, "label": "City"},
            {"value": LocationType.VILLAGE, "label": "Village"},
            {"value": LocationType.FESTIVAL_GROUND, "label": "Festival Ground"},
            {"value": LocationType.WEDDING_VENUE, "label": "Wedding Venue"},
            {"value": LocationType.OFFICE, "label": "Office"},
            {"value": LocationType.SCHOOL, "label": "School"}
        ]
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status of an image generation job"""
        if job_id not in self.active_jobs:
            return {"status": "not_found"}
        return self.active_jobs[job_id]
    
    def get_image(self, image_id: str) -> Optional[GeneratedImage]:
        """Get generated image by ID"""
        return self.generated_images.get(image_id)
