from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from typing import Dict, Any
from app.core.state import WorkflowState

def edit_and_save_excel_node(state: WorkflowState) -> Dict[str, Any]:
    print("--- 节点 4: 标记错误并保存 ---")
    results = state['llm_raw_response']
    wb = load_workbook(state['file_path_v2'])
    ws = wb.active
    red_fill = PatternFill(start_color="FFFF0000", end_color="FFFF0000", fill_type="solid")
    
    for row in range(2, ws.max_row + 1):
        emp_id = str(ws.cell(row=row, column=1).value)
        if emp_id in results and results[emp_id].get('is_error'):
            for cell in ws[row]:
                cell.fill = red_fill
            ws.cell(row=row, column=ws.max_column).value = results[emp_id].get('reason')
            
    wb.save("data/output_marked.xlsx")
    return {}