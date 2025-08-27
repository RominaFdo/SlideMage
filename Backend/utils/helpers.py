# def chunk_text(text: str, sentences_per_slide=5) -> list[str]:  
#     sentences = text.split('. ')
#     chunks = [
#         '. '.join(sentences[i:i+sentences_per_slide]).strip()
#         for i in range(0, len(sentences), sentences_per_slide)
#     ]
    
#     # Only return chunks that have substance
#     return [c for c in chunks if c and len(c) > 50]


# def chunk_bullets(bullets: list[str], bullets_per_slide: int=5) -> list[list[str]]:
#     return [bullets[i: i + bullets_per_slide] for i in range(0, len(bullets), bullets_per_slide)]


import re
import os
import unicodedata
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def chunk_bullets(bullets: List[str], bullets_per_slide: int = 5) -> List[List[str]]:
    if not bullets:
        return [[]]
    
    valid_bullets = [bullet.strip() for bullet in bullets if bullet and bullet.strip()]
    
    if not valid_bullets:
        return [["No content available"]]
    
    chunks = []
    for i in range(0, len(valid_bullets), bullets_per_slide):
        chunk = valid_bullets[i:i + bullets_per_slide]
        chunks.append(chunk)
    
    logger.info(f"Created {len(chunks)} slide chunks from {len(valid_bullets)} bullets")
    return chunks

def chunk_text(text: str, max_chunk_size: int = 1000) -> List[str]:
    
    if not text or len(text) <= max_chunk_size:
        return [text] if text else [""]
    
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) > max_chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
        else:
            current_chunk += ("\n\n" if current_chunk else "") + paragraph
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= max_chunk_size:
            final_chunks.append(chunk)
        else:
            sentences = re.split(r'[.!?]+', chunk)
            current_sentence_chunk = ""
            
            for sentence in sentences:
                if len(current_sentence_chunk) + len(sentence) > max_chunk_size and current_sentence_chunk:
                    final_chunks.append(current_sentence_chunk.strip())
                    current_sentence_chunk = sentence
                else:
                    current_sentence_chunk += sentence + ". "
            
            if current_sentence_chunk:
                final_chunks.append(current_sentence_chunk.strip())
    
    logger.info(f"Split text into {len(final_chunks)} chunks")
    return final_chunks if final_chunks else [text]

def clean_filename(filename: str) -> str:
   
    cleaned = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    cleaned = re.sub(r'\s+', '_', cleaned)
    
    cleaned = unicodedata.normalize('NFD', cleaned)
    cleaned = ''.join(c for c in cleaned if unicodedata.category(c) != 'Mn')
    
    if len(cleaned) > 100:
        cleaned = cleaned[:100]
    
    if not cleaned:
        cleaned = "presentation"
    
    return cleaned

def validate_slide_data(slide_data: Dict[str, Any]) -> Dict[str, Any]:

    validated = {
        "title": str(slide_data.get("title", "Untitled Slide")).strip(),
        "bullets": [],
        "image": slide_data.get("image"),
        "notes": slide_data.get("notes", "")
    }
    
    bullets = slide_data.get("bullets", [])
    if isinstance(bullets, str):
        bullets = [bullets]
    
    for bullet in bullets:
        if bullet and str(bullet).strip():
            bullet_text = str(bullet).strip()
            if len(bullet_text) > 200:
                bullet_text = bullet_text[:197] + "..."
            validated["bullets"].append(bullet_text)
    
    if not validated["bullets"]:
        validated["bullets"] = ["Content not available"]
    
    if len(validated["title"]) > 100:
        validated["title"] = validated["title"][:97] + "..."
    
    return validated

def format_topic(topic: str) -> str:
   
    if not topic:
        return "Untitled Topic"
    
    formatted = topic.strip()
    
    if formatted.isupper() or formatted.islower():
        formatted = formatted.title()
    
    abbreviations = {
        'Ai': 'AI',
        'Ml': 'ML',
        'Usa': 'USA',
        'Uk': 'UK',
        'Eu': 'EU',
        'Un': 'UN',
        'Nasa': 'NASA',
        'Fbi': 'FBI',
        'Cia': 'CIA'
    }
    
    for old, new in abbreviations.items():
        formatted = re.sub(r'\b' + old + r'\b', new, formatted)
    
    return formatted

def create_backup_content(topic: str) -> List[Dict[str, Any]]:
    
    logger.warning(f"Creating backup content for topic: {topic}")
    
    return [
        {
            "title": f"Introduction to {format_topic(topic)}",
            "bullets": [
                f"Overview of {topic}",
                "Key concepts and definitions",
                "Historical context and background",
                "Current relevance and applications"
            ],
            "image": None
        },
        {
            "title": f"Key Aspects of {format_topic(topic)}",
            "bullets": [
                "Main characteristics and features",
                "Important components or elements",
                "Relationships and connections",
                "Significant developments"
            ],
            "image": None
        },
        {
            "title": f"Conclusion - {format_topic(topic)}",
            "bullets": [
                "Summary of main points",
                "Key takeaways",
                "Future implications",
                "Areas for further exploration"
            ],
            "image": None
        }
    ]

def log_workflow_metrics(start_time: float, topic: str, slides_count: int, success: bool):
    
    import time
    duration = time.time() - start_time
    
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"WORKFLOW {status}: Topic='{topic}', Slides={slides_count}, Duration={duration:.2f}s")