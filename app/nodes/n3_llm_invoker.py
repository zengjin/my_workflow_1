import json
import time
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.core.state import WorkflowState

# --- 开发调试开关 ---
# True: 模拟 LLM 返回，不消耗 API 额度
# False: 真实调用 Gemini API
MOCK_MODE = True 

def invoke_gemini_node(state: WorkflowState) -> Dict[str, Any]:
    print(f"\n--- 节点 3: 开始处理数据分批 (共 {len(state['data_chunks'])} 批) ---")
    
    if MOCK_MODE:
        print("⚠️ [MOCK 模式] 激活：将模拟 AI 逻辑生成结果，不产生 API 调用。")

    chunks = state.get('data_chunks', [])
    all_combined_results = {}

    # 预设规则用于 Mock 模拟 (与 config/rules.txt 保持逻辑一致)
    valid_depts = ['技术部', '市场部', '财务部', '行政部']

    for i, chunk in enumerate(chunks):
        print(f"正在处理第 {i+1}/{len(chunks)} 批数据... (包含 {len(chunk)} 条记录)")
        
        if MOCK_MODE:
            # --- 模拟 LLM 返回逻辑 ---
            time.sleep(0.3)  # 模拟网络延迟感
            batch_json = {}
            
            for row in chunk:
                emp_id = str(row.get('员工ID', 'Unknown'))
                salary = row.get('工资', 0)
                dept = row.get('部门', '')
                join_date = str(row.get('入职日期', ''))
                
                # 逻辑模拟：根据数据特征判断是否报错
                is_error = False
                reason = ""

                if salary <= 0:
                    is_error = True
                    reason = "工资必须大于 0"
                elif dept not in valid_depts:
                    is_error = True
                    reason = f"部门 [{dept}] 非法，不在许可名单内"
                elif "2027" in join_date or "2028" in join_date:
                    is_error = True
                    reason = "入职日期逻辑错误（晚于2026年）"
                # 模拟涨幅校验 (简单模拟：如果工资 > 18000 且 ID 为 EMP002 则报错)
                elif emp_id == 'EMP002' and salary > 18000:
                    is_error = True
                    reason = "工资涨幅疑似超过 50% 基准"

                batch_json[emp_id] = {
                    "is_error": is_error,
                    "reason": f"[MOCK] {reason}" if is_error else ""
                }
            
            all_combined_results.update(batch_json)

        else:
            # --- 真实调用 Gemini 逻辑 ---
            with open('config/rules.txt', 'r', encoding='utf-8') as f:
                rules = f.read()

            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
            
            # 使用你测试成功的强约束 Prompt
            batch_prompt = (
                f"请根据以下规则校验数据。只需返回纯 JSON 格式对象，不要任何解释说明。\n\n"
                f"[校验规则]\n{rules}\n\n"
                f"[待校验数据]\n{json.dumps(chunk, ensure_ascii=False)}\n\n"
                f"返回格式必须为: {{'ID': {{'is_error': bool, 'reason': str}}}}"
            )

            max_retries = 2
            for attempt in range(max_retries):
                try:
                    response = llm.invoke([HumanMessage(content=batch_prompt)])
                    # 清洗 Markdown 标签并解析
                    clean_content = response.content.replace("```json", "").replace("```", "").strip()
                    batch_json = json.loads(clean_content)
                    all_combined_results.update(batch_json)
                    break 
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"  第 {i+1} 批调用失败，正在重试... ({e})")
                        time.sleep(2)
                    else:
                        print(f"  ❌ 第 {i+1} 批处理最终失败。")

    print(f"--- 节点 3 处理完成，已汇总 {len(all_combined_results)} 条结果 ---\n")
    return {"llm_raw_response": all_combined_results}