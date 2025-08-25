import google.generativeai as genai
import os
import time 

genai.configure(api_key = "AIzaSyBr8ZeUFqGUT9dF4N8j-DcJk8CoctyFfq0")

def summarize(text: str) -> str:
    model = genai.GenerativeModel("models/gemini-2.5-pro")

    prompt = f"Summarize this into  3-4 bullet points for a presentation:\n\n {text}"

    try:
        response = model.generate_content(prompt)
        print("✅ AI summary worked!")
        
        # Add delay to avoid quota issues
        time.sleep(1)
        
        return response.text
    except Exception as e:
        print("⚠️ AI failed, using backup method")
        print("Error:", e)
        
        # Better backup: make bullet points from sentences
        sentences = text.split('.')[:4]  # Take 4 sentences
        bullets = []
        for s in sentences:
            if s.strip() and len(s.strip()) > 10:
                bullets.append(f"• {s.strip()}")
        
        return '\n'.join(bullets) if bullets else f"• {text[:100]}..."