"""
Content moderation service.
"""
from typing import Dict, List, Optional
import re


class ModerationResult:
    """Result of content moderation."""
    
    def __init__(
        self,
        is_approved: bool,
        score: float,
        flags: List[str],
        details: Optional[Dict] = None
    ):
        self.is_approved = is_approved
        self.score = score
        self.flags = flags
        self.details = details or {}


class ContentModerator:
    """
    Content moderation pipeline for scripts and generated content.
    
    This is a basic implementation. In production, you would integrate
    with services like OpenAI Moderation API, AWS Rekognition, etc.
    """
    
    # Prohibited keywords (simplified example)
    PROHIBITED_KEYWORDS = [
        "violence", "hate", "explicit", "dangerous", "illegal"
    ]
    
    def __init__(self, threshold: float = 0.8):
        """
        Initialize moderator.
        
        Args:
            threshold: Moderation score threshold (0-1). Lower score = safer content.
        """
        self.threshold = threshold
    
    def moderate_text(self, text: str) -> ModerationResult:
        """
        Moderate text content.
        
        Args:
            text: Text to moderate
        
        Returns:
            ModerationResult with approval status and details
        """
        flags = []
        score = 0.0
        
        # Convert to lowercase for checking
        text_lower = text.lower()
        
        # Check for prohibited keywords
        for keyword in self.PROHIBITED_KEYWORDS:
            if keyword in text_lower:
                flags.append(f"prohibited_keyword:{keyword}")
                score += 0.3
        
        # Check text length (too short might be spam)
        if len(text.strip()) < 10:
            flags.append("text_too_short")
            score += 0.1
        
        # Check for excessive capitalization
        if sum(1 for c in text if c.isupper()) > len(text) * 0.5:
            flags.append("excessive_caps")
            score += 0.1
        
        # Check for excessive special characters
        special_chars = len(re.findall(r'[^a-zA-Z0-9\s]', text))
        if special_chars > len(text) * 0.3:
            flags.append("excessive_special_chars")
            score += 0.1
        
        # Normalize score
        score = min(score, 1.0)
        
        is_approved = score < self.threshold
        
        return ModerationResult(
            is_approved=is_approved,
            score=score,
            flags=flags,
            details={
                "text_length": len(text),
                "threshold": self.threshold
            }
        )
    
    def moderate_image_description(self, description: str) -> ModerationResult:
        """
        Moderate image generation descriptions.
        
        Args:
            description: Image description to moderate
        
        Returns:
            ModerationResult
        """
        # For image descriptions, we can be more strict
        return self.moderate_text(description)
    
    def batch_moderate(self, texts: List[str]) -> List[ModerationResult]:
        """
        Moderate multiple texts in batch.
        
        Args:
            texts: List of texts to moderate
        
        Returns:
            List of ModerationResults
        """
        return [self.moderate_text(text) for text in texts]


# Global moderator instance
moderator = ContentModerator()
