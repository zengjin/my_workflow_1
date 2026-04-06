import json
import os
from typing import Dict, Any
from urllib import response
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.core import state
from app.core.state import WorkflowState

def invoke_gemini_node(state: WorkflowState) -> Dict[str, Any]:
    print("--- 节点 3: 调用 Gemini ---")
    # 新增下面这一行，利用 f-string 配合分隔符让输出更清晰
    print(f"DEBUG - Final Prompt:\n{'-'*50}\n{state['final_prompt']}\n{'-'*50}")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    response = llm.invoke([HumanMessage(content=state['final_prompt'])])
    
    print(f"DEBUG - LLM Response:\n{'-'*50}\n{response.content}\n{'-'*50}")

    # 简单清洗并解析 JSON
    text = response.content.replace("```json", "").replace("```", "").strip()
    return {"llm_raw_response": json.loads(text)}