import json
from typing import Dict, Any
from app.core.state import WorkflowState

def build_prompt_node(state: WorkflowState) -> Dict[str, Any]:
    print("--- 节点 2: 拼接提示词 ---")
    with open('config/rules.txt', 'r', encoding='utf-8') as f:
        rules = f.read()
    
    data_str = json.dumps(state['diff_data'], ensure_ascii=False, indent=2)
    prompt = f"请根据规则校验数据。规则:\n{rules}\n\n数据:\n{data_str}\n\n请返回JSON:{{'ID':{{'is_error':bool, 'reason':str}}}}"
    return {"final_prompt": prompt}