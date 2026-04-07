from typing import TypedDict, List, Dict, Any, Optional

class WorkflowState(TypedDict):
    file_path_v1: str
    file_path_v2: str
    # 新增：存储切分后的批次列表
    data_chunks: List[List[Dict[str, Any]]] 
    final_prompt: str # 串行模式下，这个字段可以变成“当前批次的提示词”或废弃
    llm_raw_response: Dict[str, Any]
    error_message: Optional[str]