def chunk_text(text: str, sentences_per_slide=5) -> list[str]:  
    sentences = text.split('. ')
    chunks = [
        '. '.join(sentences[i:i+sentences_per_slide]).strip()
        for i in range(0, len(sentences), sentences_per_slide)
    ]
    
    # Only return chunks that have substance
    return [c for c in chunks if c and len(c) > 50]