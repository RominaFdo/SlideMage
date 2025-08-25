from connectors.wikipedia_connector import fetch_wikipedia_summary
from agents.designer_agent import design_slide
from agents.export_agent import export_to_pptx
from agents.summarizer_agent import summarize
from utils.helpers import chunk_text

def run(topic: str):
    print("Running slide generation for topic:", topic)

    text = fetch_wikipedia_summary(topic)

    chunks = chunk_text(text)
    slides = []
    for i, c in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}")
        summary = summarize(c)
        bullets = [b.strip() for b in summary.split("\n") if b.strip()]
        slide = design_slide(title=f"{topic} - Part {i+1}", bullets=bullets)
        slides.append(slide)

    # Export ALL slides, not just the last one
    export_to_pptx(slides, filename=f"{topic}_presentation.pptx")
    print(f"Generated {len(slides)} slides!")

if __name__ == "__main__":
    run("Ancient Egypt")