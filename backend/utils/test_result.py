import pandas as pd
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "data", "results") 

os.makedirs(RESULTS_DIR, exist_ok=True)

def save_backtest_results(test_id: str, summary: dict, chart_data: pd.DataFrame):
    """ 백테스트 결과를 JSON 파일과 CSV 파일로 분리하여 저장 """
    file_prefix = os.path.join(RESULTS_DIR, test_id)
    
    with open(f"{file_prefix}_summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)
        
    chart_data.to_csv(f"{file_prefix}_chart.csv", index=False)
    print(f"결과 저장 완료: {file_prefix}_*")

def load_backtest_results(test_id: str):
    """ 저장된 결과를 로드하여 프론트엔드에 전달할 JSON 객체로 반환 """
    file_prefix = os.path.join(RESULTS_DIR, test_id)
    
    try:
        with open(f"{file_prefix}_summary.json", 'r', encoding='utf-8') as f:
            summary = json.load(f)
            
        chart_df = pd.read_csv(f"{file_prefix}_chart.csv")
        chart_data = chart_df.to_dict(orient="records")
        
        return {"summary": summary, "chart_data": chart_data}
        
    except FileNotFoundError as e:
        print(f"로드 실패: 파일 경로 문제 발생 - {e}")
        return None