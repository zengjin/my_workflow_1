import json
import time
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.core.state import WorkflowState

# 分批大小 (Batch Size)：在 n1_data_extractor.py 中，如果数据每条都很长，建议把 BATCH_SIZE 设小一点（比如 10-20）；如果数据很短，可以设大一点（50-100），这样能省钱并提高效率。
# API 限制：如果你使用的是 Gemini 的免费额度，会有每分钟调用次数限制（RPM）。如果批次很多，记得在循环里加一个 time.sleep(2)。
# Excel 标记：现在去查看 data/output_marked.xlsx，你应该能看到所有 100 条数据中，凡是违反那 4 条规则的数据都被精准地“染红”了。

def invoke_gemini_node(state: WorkflowState) -> Dict[str, Any]:
    print(f"\n--- 节点 3: 开始串行分批调用 Gemini (共 {len(state['data_chunks'])} 批) ---")
    
    chunks = state.get('data_chunks', [])
    with open('config/rules.txt', 'r', encoding='utf-8') as f:
        rules = f.read()
    
    # 建议使用 gemini-1.5-flash，速度快且对结构化输出支持良好
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    all_combined_results = {}

    for i, chunk in enumerate(chunks):
        print(f"正在处理第 {i+1}/{len(chunks)} 批数据... (包含 {len(chunk)} 条记录)")
        
        # 使用你测试成功的强约束 Prompt
        batch_prompt = (
            f"请根据以下规则校验数据。只需返回纯 JSON，不要任何解释。\n\n"
            f"[校验规则]\n{rules}\n\n"
            f"[待校验数据]\n{json.dumps(chunk, ensure_ascii=False)}\n\n"
            f"请返回JSON格式: {{'ID': {{'is_error': bool, 'reason': str}}}}"
        )

        # 增加简单的重试逻辑，应对网络波动或解析失败
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = llm.invoke([HumanMessage(content=batch_prompt)])
                raw_content = response.content.strip()
                
                # 兼容处理：去掉可能存在的 Markdown 代码块标记
                clean_content = raw_content.replace("```json", "").replace("```", "").strip()
                
                batch_json = json.loads(clean_content)
                all_combined_results.update(batch_json)
                break # 成功则跳出重试循环
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  第 {i+1} 批尝试失败，正在重试 ({attempt + 1}/{max_retries})... 错误: {e}")
                    time.sleep(2) # 等待 2 秒再重试
                else:
                    print(f"  ❌ 第 {i+1} 批最终处理失败，跳过。")

    print(f"--- 节点 3 处理完成，共获取 {len(all_combined_results)} 条校验结果 ---\n")
    return {"llm_raw_response": all_combined_results}