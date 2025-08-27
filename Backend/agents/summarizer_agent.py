# import google.generativeai as genai
# import os
# import time 

# genai.configure(api_key = "AIzaSyBr8ZeUFqGUT9dF4N8j-DcJk8CoctyFfq0")

# def summarize(text: str) -> list[str]:
#     model = genai.GenerativeModel("models/gemini-2.5-pro")

#     prompt = f"Summarize this into  3-4 bullet points for a presentation:\n\n {text}"

#     try:
#         response = model.generate_content(prompt)
#         print("✅ AI summary worked!")
#         time.sleep(1)
#         bullets = [line.strip("•- ") for line in response.text.splitlines() if line.strip()]
#         return bullets[:4] if bullets else [response.text]
    

#     except Exception as e:
#         print("⚠️ AI failed, using backup method")
#         print("Error:", e)
#         sentences = text.split('.')[:4]
#         return [s.strip() for s in sentences if len(s.strip()) > 10]



import google.generativeai as genai
import os
import time
import logging
from typing import List

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable not set")
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=GEMINI_API_KEY)

def summarize(text: str, max_bullets: int = 4) -> List[str]:
   
    if not text or not text.strip():
        logger.warning("Empty text provided to summarize")
        return ["No content available"]
    
    model = genai.GenerativeModel("models/gemini-2.5-pro")
    
    prompt = f"""
    Create {max_bullets} concise bullet points from the following text for a presentation slide.
    Each bullet point should be:
    - Clear and informative
    - Between 10-20 words
    - Self-contained and understandable
    - Focused on key information
    
    Text to summarize:
    {text}
    
    Format: Return only the bullet points, one per line, without bullet symbols.
    """

    try:
        response = model.generate_content(prompt)
        logger.info("AI summarization successful")
        
        time.sleep(1)
        
        if response.text:
            bullets = [
                line.strip().lstrip("•-* ").strip() 
                for line in response.text.splitlines() 
                if line.strip() and len(line.strip()) > 5
            ]
            
            # Ensure we don't exceed max_bullets
            bullets = bullets[:max_bullets] if bullets else [response.text.strip()]
            
            # Validate bullets aren't too long
            processed_bullets = []
            for bullet in bullets:
                if len(bullet.split()) > 25:  # Too long, truncate
                    words = bullet.split()[:20]
                    bullet = " ".join(words) + "..."
                processed_bullets.append(bullet)
            
            return processed_bullets if processed_bullets else ["Unable to generate summary"]
        
        else:
            logger.warning("Empty response from AI model")
            return _fallback_summarize(text, max_bullets)
    
    except Exception as e:
        logger.error(f"⚠️ AI summarization failed: {str(e)}")
        return _fallback_summarize(text, max_bullets)

def _fallback_summarize(text: str, max_bullets: int = 4) -> List[str]:
    
    logger.info("Using fallback summarization method")
    
    sentences = [
        s.strip() 
        for s in text.replace('!', '.').replace('?', '.').split('.')
        if len(s.strip()) > 10
    ]
    
    bullets = sentences[:max_bullets]
    
    if not bullets:
        bullets = [text[:100] + "..." if len(text) > 100 else text]
    
    return bullets

def summarize_with_context(text: str, topic: str, max_bullets: int = 4) -> List[str]:
   
    if not GEMINI_API_KEY:
        return _fallback_summarize(text, max_bullets)
    
    model = genai.GenerativeModel("models/gemini-2.5-pro")
    
    prompt = f"""
    Topic: {topic}
    
    Create {max_bullets} bullet points about "{topic}" from the following text.
    Focus on the most important and relevant information related to {topic}.
    
    Text:
    {text}
    
    Requirements:
    - Each bullet should be 10-20 words
    - Focus on facts, key concepts, or important details
    - Make them presentation-ready
    - Return only the bullet points, no formatting symbols
    """
    
    try:
        response = model.generate_content(prompt)
        logger.info(f"Contextual summarization successful for topic: {topic}")
        time.sleep(1)
        
        if response.text:
            bullets = [
                line.strip().lstrip("•-* ").strip()
                for line in response.text.splitlines()
                if line.strip() and len(line.strip()) > 5
            ]
            return bullets[:max_bullets] if bullets else _fallback_summarize(text, max_bullets)
        
    except Exception as e:
        logger.error(f"Contextual summarization failed: {str(e)}")
    
    return _fallback_summarize(text, max_bullets)