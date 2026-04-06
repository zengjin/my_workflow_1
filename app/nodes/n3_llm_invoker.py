import json
import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.core.state import WorkflowState

def invoke_gemini_node(state: WorkflowState) -> Dict[str, Any]:
    print("--- 节点 3: 调用 Gemini ---")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    response = llm.invoke([HumanMessage(content=state['final_prompt'])])
    
    # 简单清洗并解析 JSON
    text = response.content.replace("```json", "").replace("```", "").strip()
    return {"llm_raw_response": json.loads(text)}