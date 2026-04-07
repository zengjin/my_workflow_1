import os
import pandas as pd
from dotenv import load_dotenv
from app.core.agent import create_workflow

load_dotenv()

def prepare_test_excel():
    os.makedirs('data', exist_ok=True)
    df1 = pd.DataFrame({'ID': ['101'], '姓名': ['张三'], '工资': [5000]})
    df2 = pd.DataFrame({'ID': ['101', '102'], '姓名': ['张三', '李四'], '工资': [5200, 0]})
    df1.to_excel('data/v1.xlsx', index=False)
    df2.to_excel('data/v2.xlsx', index=False)

if __name__ == "__main__":
    prepare_test_excel()
    app = create_workflow()
    app.invoke({
        "file_path_v1": "data/v1.xlsx",
        "file_path_v2": "data/v2.xlsx",
        "data_chunks": [],       # 必须包含这个初始化字段，取代原来的 diff_data
        "llm_raw_response": {}, 
        "error_message": None
    })
    print("执行成功！请查看 data/output_marked.xlsx")