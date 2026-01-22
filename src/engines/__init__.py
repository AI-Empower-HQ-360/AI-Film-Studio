"""
AI Film Studio - Enterprise Studio Operating System
Core Engine Modules
"""

# Lazy imports to handle missing dependencies in test environments
try:
    from .character_engine import CharacterEngine, Character, CharacterVersion, CharacterIdentity
except ImportError:
    CharacterEngine = Character = CharacterVersion = CharacterIdentity = None

try:
    from .writing_engine import WritingEngine, Script, Scene, Dialogue
except ImportError:
    WritingEngine = Script = Scene = Dialogue = None

try:
    from .preproduction_engine import PreProductionEngine, ProductionPlan, ShootingSchedule
except ImportError:
    PreProductionEngine = ProductionPlan = ShootingSchedule = None

try:
    from .production_management import ProductionManager, Project, Asset, Timeline
except ImportError:
    ProductionManager = Project = Asset = Timeline = None

try:
    from .production_layer import ProductionLayer, Shot
except ImportError:
    ProductionLayer = Shot = None

try:
    from .postproduction_engine import PostProductionEngine
except ImportError:
    PostProductionEngine = None

try:
    from .marketing_engine import MarketingEngine
except ImportError:
    MarketingEngine = None

try:
    from .enterprise_platform import EnterprisePlatform
except ImportError:
    EnterprisePlatform = None

__all__ = [
    "CharacterEngine",
    "Character",
    "CharacterVersion",
    "CharacterIdentity",
    "WritingEngine",
    "Script",
    "Scene",
    "Dialogue",
    "PreProductionEngine",
    "ProductionPlan",
    "ShootingSchedule",
    "ProductionManager",
    "Project",
    "Asset",
    "Timeline",
    "ProductionLayer",
    "Shot",
    "PostProductionEngine",
    "MarketingEngine",
    "EnterprisePlatform",
]
