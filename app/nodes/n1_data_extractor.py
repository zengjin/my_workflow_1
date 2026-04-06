import pandas as pd
from typing import Dict, Any
from app.core.state import WorkflowState

def extract_diff_data_node(state: WorkflowState) -> Dict[str, Any]:
    print("--- 节点 1: 正在对比 Excel ---")
    df1 = pd.read_excel(state['file_path_v1'])
    df2 = pd.read_excel(state['file_path_v2'])
    
    # 简单对比：找出 V2 中不在 V1 的行，或者 ID 相同但内容不同的行
    # 这里为了演示，取 V2 全量数据作为待校验项
    diff_list = df2.to_dict(orient='records')
    return {"diff_data": diff_list}