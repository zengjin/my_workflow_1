from langgraph.graph import StateGraph, END
from app.core.state import WorkflowState
from app.nodes.n1_data_extractor import extract_diff_data_node
from app.nodes.n2_prompt_builder import build_prompt_node
from app.nodes.n3_llm_invoker import invoke_gemini_node
from app.nodes.n4_excel_editor import edit_and_save_excel_node

def create_workflow():
    workflow = StateGraph(WorkflowState)
    workflow.add_node("n1", extract_diff_data_node)
    workflow.add_node("n2", build_prompt_node)
    workflow.add_node("n3", invoke_gemini_node)
    workflow.add_node("n4", edit_and_save_excel_node)
    
    workflow.set_entry_point("n1")
    workflow.add_edge("n1", "n2")
    workflow.add_edge("n2", "n3")
    workflow.add_edge("n3", "n4")
    workflow.add_edge("n4", END)
    return workflow.compile()