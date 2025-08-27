import wikipedia

def research(topic: str) -> str:
    try:
        s = wikipedia.summary(topic, sentences=5)
        print("✅ Research Successful")
        return s
    except Exception as e:
        print("⚠️ Research Failed:", e)
        return "Error"
