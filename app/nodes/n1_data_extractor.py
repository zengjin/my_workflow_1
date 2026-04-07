import pandas as pd
from typing import Dict, Any
from app.core.state import WorkflowState

def extract_diff_data_node(state: WorkflowState) -> Dict[str, Any]:
    print("--- 节点 1: 正在对比 Excel ---")
    df1 = pd.read_excel(state['file_path_v1'])
    df2 = pd.read_excel(state['file_path_v2'])
    
    all_data = df2.to_dict(orient='records')
    
    # 定义批次大小，例如每批处理 20 条数据
    BATCH_SIZE = 1
    data_chunks = [all_data[i:i + BATCH_SIZE] for i in range(0, len(all_data), BATCH_SIZE)]
    
    print(f"总计 {len(all_data)} 条数据，已切分为 {len(data_chunks)} 个批次。")
    
    # 注意：我们需要在 WorkflowState 中增加一个 data_chunks 字段
    return {"data_chunks": data_chunks}