from langgraph import Graph, Node

from connectors.wikipedia_connector import fetch_wikipedia_summary
from agents.summarizer_agent import summarize
from agents.designer_agent import design_slide
from agents.export_agent import export_to_pptx

def build_workflow(topic:str):

    graph = Graph()

    # Research Node
    def research_node(_):
        return fetch_wikipedia_summary(topic)
    
    # Summarize Node
    def summarize_node(text):
        return summarize(text)
    
    # Design Node
    def design_node(bullets):
        return design_slide(title=topic, bullets=bullets)

    # Export Node
    def export_node(slide):
        export_to_pptx([slide], filename="SlideMage_LangGraph.pptx")
        return "Done"

    graph.add_node(Node(research_node, "Research"))
    graph.add_node(Node(summarize_node, "Summarize"))
    graph.add_node(Node(design_node, "Design"))
    graph.add_node(Node(export_node, "Export"))


    graph.add_edge("Research", "Summarize")
    graph.add_edge("Summarize", "Design")
    graph.add_edge("Design", "Export")

    graph.run(None)
    