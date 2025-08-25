import wikipediaapi

def fetch_wikipedia_summary(topic: str) ->str:
    wiki = wikipediaapi.Wikipedia(
      user_agent="SlideMage/1.0 (https://github.com/RominaFdo/slidemage)", 
        language="en"  
    )
    page = wiki.page(topic)

    if not page.exists():
        return "No page found for this topic."
    
    return page.summary