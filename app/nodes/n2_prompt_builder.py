import json
from typing import Dict, Any
from app.core.state import WorkflowState

def build_prompt_node(state: WorkflowState) -> Dict[str, Any]:
    print("--- 节点 2: 准备提示词模板 ---")
    # 这里不再读取数据，只确保 rules 文件存在，或者从 state 获取 data_chunks 长度
    if 'data_chunks' not in state:
        raise KeyError("State 中缺失 'data_chunks'，请检查节点 1 的输出。")
    return {} # 串行模式下，具体拼接逻辑移到了 n3 的循环里