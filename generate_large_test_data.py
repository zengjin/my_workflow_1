import pandas as pd
import numpy as np
import os

def generate_large_test_data():
    os.makedirs('data', exist_ok=True)
    
    # 基础配置
    departments = ['技术部', '市场部', '财务部', '行政部']
    base_count = 100
    
    # --- 1. 生成 V1 (基准数据) ---
    data_v1 = {
        '员工ID': [f'EMP{str(i).zfill(3)}' for i in range(1, base_count + 1)],
        '姓名': [f'员工_{i}' for i in range(1, base_count + 1)],
        '部门': [np.random.choice(departments) for _ in range(base_count)],
        '工资': [np.random.randint(5000, 20000) for _ in range(base_count)],
        '入职日期': pd.date_range(start='2020-01-01', periods=base_count).strftime('%Y-%m-%d').tolist()
    }
    df_v1 = pd.DataFrame(data_v1)
    df_v1.to_excel('data/v1.xlsx', index=False)
    
    # --- 2. 生成 V2 (包含变更与追加) ---
    df_v2 = df_v1.copy()
    
    # A. 模拟工资变更 (符合规则 vs 不符合规则)
    # 修改前 5 人的工资：EMP001 正常涨幅，EMP002 涨幅过大(>50%)
    df_v2.loc[0, '工资'] = df_v1.loc[0, '工资'] + 500  # 正常
    df_v2.loc[1, '工资'] = df_v1.loc[1, '工资'] * 2    # 错误：涨幅过大
    
    # B. 模拟部门错误
    # 修改 EMP010 的部门为一个不存在的部门
    df_v2.loc[9, '部门'] = '魔法部' # 错误：部门不存在
    
    # C. 模拟工资为 0
    # 修改 EMP020
    df_v2.loc[19, '工资'] = 0 # 错误：工资必须大于0
    
    # D. 模拟日期错误
    # 修改 EMP030
    df_v2.loc[29, '入职日期'] = '2027-01-01' # 错误：晚于2026年
    
    # E. 追加 5 条新数据 (EMP101 - EMP105)
    new_rows = []
    for i in range(101, 106):
        new_rows.append({
            '员工ID': f'EMP{i}',
            '姓名': f'新员工_{i}',
            '部门': np.random.choice(departments),
            '工资': np.random.randint(5000, 15000),
            '入职日期': '2026-05-01'
        })
    df_v2 = pd.concat([df_v2, pd.DataFrame(new_rows)], ignore_index=True)
    
    df_v2.to_excel('data/v2.xlsx', index=False)
    print(f"成功生成测试数据：")
    print(f"- V1: {len(df_v1)} 条记录")
    print(f"- V2: {len(df_v2)} 条记录 (包含变更和追加)")
    print(f"预期错误点：EMP002(涨幅), EMP010(部门), EMP020(工资0), EMP030(日期)")

if __name__ == "__main__":
    generate_large_test_data()