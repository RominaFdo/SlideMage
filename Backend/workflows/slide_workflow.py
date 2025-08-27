# from langgraph import Graph, Node

# from connectors.wikipedia_connector import fetch_wikipedia_summary
# from agents.summarizer_agent import summarize
# from agents.designer_agent import design_slide
# from agents.export_agent import export_to_pptx

# def build_workflow(topic:str):

#     graph = Graph()

#     # Research Node
#     def research_node(_):
#         return fetch_wikipedia_summary(topic)
    
#     # Summarize Node
#     def summarize_node(text):
#         return summarize(text)
    
#     # Design Node
#     def design_node(bullets):
#         return design_slide(title=topic, bullets=bullets)

#     # Export Node
#     def export_node(slide):
#         export_to_pptx([slide], filename="SlideMage_LangGraph.pptx")
#         return "Done"

#     graph.add_node(Node(research_node, "Research"))
#     graph.add_node(Node(summarize_node, "Summarize"))
#     graph.add_node(Node(design_node, "Design"))
#     graph.add_node(Node(export_node, "Export"))


#     graph.add_edge("Research", "Summarize")
#     graph.add_edge("Summarize", "Design")
#     graph.add_edge("Design", "Export")

#     graph.run(None)
    
# ------------------------------------------

# from pptx import Presentation
# from agents.research_agent import research
# from agents.summarizer_agent import summarize
# from agents.designer_agent import design_slides
# from agents.export_agent import export_to_pptx
# from utils.helpers import chunk_bullets


# def build_workflow(topic: str)-> str:
#     research_text = research(topic)

#     summary = summarize(research_text)

#     chunks = chunk_bullets(summary, bullets_per_slide=3)

#     slides =    [design_slides(title=f"{topic} (Slide {i+1})", bullets=chunk) 
#               for i, chunk in enumerate(chunks)]

#     filename = f"{topic}_slides.pptx"
#     export_to_pptx(slides, filename)

#     return filename

import os
import logging
from typing import List, Dict
from agents.research_agent import research
from agents.summarizer_agent import summarize_with_context
from agents.designer_agent import design_slides
from agents.export_agent import export_to_pptx
from utils.helpers import chunk_bullets, clean_filename

logger = logging.getLogger(__name__)

def build_workflow(topic: str, bullets_per_slide: int = 4) -> str:

    try:
        logger.info(f"Starting workflow for topic: {topic}")
        
        # Step 1: Research
        logger.info("Step 1: Researching topic...")
        research_text = research(topic)
        
        if not research_text or research_text == "Error":
            raise ValueError(f"Failed to research topic: {topic}")
        
        # Step 2: Summarize with context
        logger.info("Step 2: Summarizing content...")
        bullets = summarize_with_context(research_text, topic, max_bullets=12)
        
        if not bullets:
            raise ValueError("Failed to generate summary bullets")
        
        # Step 3: Chunk bullets into slides
        logger.info("Step 3: Organizing content into slides...")
        slide_chunks = chunk_bullets(bullets, bullets_per_slide=bullets_per_slide)
        
        # Step 4: Design slides
        logger.info("Step 4: Designing slides...")
        slides = []
        for i, chunk in enumerate(slide_chunks):
            slide_title = f"{topic}" if len(slide_chunks) == 1 else f"{topic} - Part {i+1}"
            slide = design_slides(title=slide_title, bullets=chunk)
            slides.append(slide)
        
        # Step 5: Export to PowerPoint
        logger.info("Step 5: Exporting to PowerPoint...")
        safe_topic = clean_filename(topic)
        filename = f"{safe_topic}_slides.pptx"
        export_to_pptx(slides, filename)
        
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Failed to create PowerPoint file: {filename}")
        
        logger.info(f"Workflow completed successfully! Generated {len(slides)} slides")
        return filename
        
    except Exception as e:
        logger.error(f" Workflow failed: {str(e)}")
        raise

def build_workflow_from_text(text: str, title: str = "Presentation", bullets_per_slide: int = 4) -> str:
    
    try:
        logger.info(f"Starting text-based workflow for: {title}")
        
        # Skip research step, go directly to summarization
        logger.info("Step 1: Summarizing provided text...")
        bullets = summarize_with_context(text, title, max_bullets=12)
        
        if not bullets:
            raise ValueError("Failed to generate summary bullets from text")
        
        # Step 2: Chunk bullets into slides
        logger.info("Step 2: Organizing content into slides...")
        slide_chunks = chunk_bullets(bullets, bullets_per_slide=bullets_per_slide)
        
        # Step 3: Design slides
        logger.info("Step 3: Designing slides...")
        slides = []
        for i, chunk in enumerate(slide_chunks):
            slide_title = f"{title}" if len(slide_chunks) == 1 else f"{title} - Part {i+1}"
            slide = design_slides(title=slide_title, bullets=chunk)
            slides.append(slide)
        
        # Step 4: Export to PowerPoint
        logger.info("Step 4: Exporting to PowerPoint...")
        safe_title = clean_filename(title)
        filename = f"{safe_title}_slides.pptx"
        export_to_pptx(slides, filename)
        
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Failed to create PowerPoint file: {filename}")
        
        logger.info(f"Text-based workflow completed! Generated {len(slides)} slides")
        return filename
        
    except Exception as e:
        logger.error(f"Text-based workflow failed: {str(e)}")
        raise

def validate_workflow_requirements() -> Dict[str, bool]:
    """
    Validate that all workflow requirements are met.
    
    Returns:
        Dict[str, bool]: Status of each requirement
    """
    requirements = {
        "gemini_api_key": bool(os.getenv("GEMINI_API_KEY")),
        "wikipedia_available": True,  # Assume available for now
        "pptx_library": True,  # Check if python-pptx is available
    }
    
    try:
        import pptx
        requirements["pptx_library"] = True
    except ImportError:
        requirements["pptx_library"] = False
    
    try:
        import wikipedia
        requirements["wikipedia_available"] = True
    except ImportError:
        requirements["wikipedia_available"] = False
    
    return requirements
