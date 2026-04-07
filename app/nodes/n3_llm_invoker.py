import json
from app.core.state import WorkflowState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

def invoke_gemini_node(state: WorkflowState) -> dict:
    print("--- 节点 3: 启动分批调用 Gemini ---")
    
    # 1. 安全获取数据分片
    chunks = state.get('data_chunks', [])
    if not chunks:
        print("警告: 没有发现待处理的数据分片 (data_chunks)")
        return {"llm_raw_response": {}}

    # 2. 读取规则文件
    with open('config/rules.txt', 'r', encoding='utf-8') as f:
        rules = f.read()

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    all_combined_results = {}

    # 3. 开始串行循环
    for i, chunk in enumerate(chunks):
        print(f"正在处理第 {i+1}/{len(chunks)} 批数据...")
        
        # 这里的 batch_prompt 是局部变量，不需要从 state 获取
        batch_prompt = f"规则：\n{rules}\n\n待校验数据：\n{json.dumps(chunk, ensure_ascii=False)}\n\n请返回JSON:{{'ID':{{'is_error':bool, 'reason':str}}}}"
        
        # 调试打印（可选）
        print(f"DEBUG - Batch {i+1} Prompt Preview: {batch_prompt[:100]}...")

        try:
            response = llm.invoke([HumanMessage(content=batch_prompt)])

            print*(f"DEBUG - Batch {i+1} Raw Response: {response.content[:100]}...")

            content = response.content.replace("```json", "").replace("```", "").strip()
            batch_json = json.loads(content)
            
            # 合并结果到总表
            all_combined_results.update(batch_json)
        except Exception as e:
            print(f"批次 {i+1} 发生错误: {e}")
            continue

    # 4. 返回最终合并后的结果，这会更新 state['llm_raw_response']
    return {"llm_raw_response": all_combined_results}