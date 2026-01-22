# Character Image Generation Guide

## Overview

The Image Creation Engine now supports generating character images (like Krishna, Radha, and other deities) for **ALL age groups** (0-3, 4-8, 8-12, teens, 20-21, 22-35, 35-50, 50+), with traditional attire, accessories, and name overlays.

## Features

### 1. Character Types
- **Hindu Deities**: Krishna, Radha, Shiva, Parvati, Ganesha, Lakshmi, Saraswati, Hanuman, Rama, Sita, Durga, Kali
- **Religious Figures**: Buddha, Jesus, Angels
- **Mythical**: Fairies, Princes, Princesses
- **Other**: Warriors, Sages, Monks, Nuns
- **Generic**: Custom characters

### 2. Age Groups (All Supported)
- **0-3 years**: Infants/babies
- **4-8 years**: Young children
- **8-12 years**: Pre-teens
- **13-19 years**: Teenagers
- **20-21 years**: Young adults
- **22-35 years**: Adults
- **35-50 years**: Middle-aged
- **50+ years**: Seniors

### 3. Traditional Attire
- **Krishna Attire**: Yellow dhoti, golden crown with peacock feather, golden jewelry, flute
- **Radha Attire**: Traditional lehenga with dupatta, golden jewelry, crown
- **Deity Attire**: Traditional deity clothing with elaborate jewelry
- **Saint Attire**: Simple, spiritual clothing
- **Other**: Sari, Kurta, Dhoti, and more

### 4. Accessories
- Crown, Peacock Feather, Jewelry (necklace, bangles, anklets, armlets, earrings)
- Flute, Garland, Tilak, Dupatta, Mala (prayer beads)

### 5. Poses
- Standing, Sitting, Playing Flute, Blessing, Meditating, Dancing, Smiling, Serene, Laughing, Looking Up, Looking at Camera

### 6. Expressions
- Smiling, Joyful, Serene, Laughing, Blessing, Meditative, Playful, Divine, Innocent, Wise

### 7. Name Overlay
- Generate images with name and meaning overlays (pink rectangular boxes)
- Supports custom names and meanings

## API Usage Examples

### Example 1: Baby Krishna (0-3 years)
```json
{
  "character_type": "krishna",
  "age_group": "0-3",
  "gender": "boy",
  "character_name": "Krishna",
  "name_meaning": "The Divine",
  "include_name_overlay": true,
  "accessories": ["crown", "peacock_feather", "jewelry", "flute"],
  "pose": "playing_flute",
  "expression": "joyful",
  "location": "temple_courtyard",
  "style": "artistic"
}
```

### Example 2: Child Radha (4-8 years)
```json
{
  "character_type": "radha",
  "age_group": "4-8",
  "gender": "girl",
  "character_name": "Radha",
  "name_meaning": "Prosperity",
  "include_name_overlay": true,
  "accessories": ["crown", "jewelry", "dupatta", "garland"],
  "pose": "standing",
  "expression": "serene",
  "location": "garden",
  "style": "artistic"
}
```

### Example 3: Teen Krishna (13-19 years)
```json
{
  "character_type": "krishna",
  "age_group": "13-19",
  "gender": "boy",
  "character_name": "Krishna",
  "name_meaning": "The All-Attractive",
  "include_name_overlay": true,
  "accessories": ["crown", "peacock_feather", "jewelry", "flute"],
  "pose": "playing_flute",
  "expression": "divine",
  "location": "ocean",
  "style": "cinematic"
}
```

### Example 4: Adult Krishna (22-35 years)
```json
{
  "character_type": "krishna",
  "age_group": "22-35",
  "gender": "man",
  "character_name": "Krishna",
  "name_meaning": "The Supreme Personality",
  "include_name_overlay": true,
  "accessories": ["crown", "peacock_feather", "jewelry", "flute"],
  "pose": "standing",
  "expression": "serene",
  "location": "temple",
  "style": "realistic"
}
```

### Example 5: Senior Krishna (50+ years)
```json
{
  "character_type": "krishna",
  "age_group": "50+",
  "gender": "man",
  "character_name": "Krishna",
  "name_meaning": "The Eternal",
  "include_name_overlay": true,
  "accessories": ["crown", "peacock_feather", "jewelry", "flute"],
  "pose": "sitting",
  "expression": "wise",
  "location": "temple",
  "style": "traditional"
}
```

### Example 6: Custom Name with Character
```json
{
  "character_type": "krishna",
  "age_group": "4-8",
  "gender": "boy",
  "character_name": "Ansh",
  "name_meaning": "Part of God",
  "include_name_overlay": true,
  "accessories": ["crown", "peacock_feather", "jewelry"],
  "pose": "smiling",
  "expression": "joyful",
  "location": "garden",
  "style": "artistic"
}
```

## API Endpoints

### Generate Image
```
POST /api/v1/images/generate
```

### Get Options
```
GET /api/v1/images/options/character-types
GET /api/v1/images/options/age-groups
GET /api/v1/images/options/genders
GET /api/v1/images/options/accessories
GET /api/v1/images/options/poses
GET /api/v1/images/options/expressions
GET /api/v1/images/options/dress-types
GET /api/v1/images/options/locations
```

## Character-Specific Details

### Krishna
- **Default Attire**: Yellow dhoti, golden crown with peacock feather, golden jewelry
- **Accessories**: Flute, peacock feather, crown, jewelry
- **Common Poses**: Playing flute, standing, blessing
- **Common Expressions**: Joyful, serene, divine

### Radha
- **Default Attire**: Traditional lehenga with dupatta, golden jewelry, crown
- **Accessories**: Crown, jewelry, dupatta, garland
- **Common Poses**: Standing, dancing, sitting
- **Common Expressions**: Serene, joyful, loving

### Other Deities
- Each deity has specific traditional attire and accessories
- Can be customized with age, gender, and other parameters

## Name Overlay

When `include_name_overlay: true`:
- Name appears in a pink rectangular box on the chest
- Meaning appears in a smaller pink box below the name
- Style matches social media posts (like Instagram/TikTok)

## Best Practices

1. **Age-Appropriate Details**: 
   - Babies (0-3): Simpler jewelry, softer expressions
   - Children (4-12): Playful poses, joyful expressions
   - Teens (13-19): More mature poses, confident expressions
   - Adults (22+): Sophisticated poses, wise expressions

2. **Character Consistency**:
   - Use appropriate accessories for each character type
   - Match attire to character (e.g., Krishna = yellow dhoti, peacock feather)

3. **Cultural Sensitivity**:
   - Use appropriate cultural regions
   - Respect traditional attire and accessories

4. **Image Quality**:
   - Use "artistic" or "cinematic" style for best results
   - Higher resolution (1920x1080) for detailed images

## Integration with Frontend

The frontend component at `/images` supports all these features:
- Character type selection
- Age group selection
- Accessory selection
- Pose and expression selection
- Name overlay toggle
- Real-time preview

## Next Steps

1. **Name Overlay Rendering**: Implement actual text overlay on generated images
2. **Template System**: Pre-defined templates for popular character/age combinations
3. **Batch Generation**: Generate multiple age groups at once
4. **Style Presets**: Save and reuse favorite combinations
5. **Image Editing**: Post-process images to add overlays, adjust colors, etc.
