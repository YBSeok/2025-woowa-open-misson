from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
from __test__.back_test import run_test
from utils.test_result import load_backtest_results

app = FastAPI()

origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "FastAPI server is running."}


@app.post("/api/backtest", response_model=BacktestResponse, tags=["Backtesting"])
async def run_backtest_optimization(config: dict):
    """
    클라이언트가 전달한 설정(config)으로 백테스팅/최적화를 실행하고 결과를 반환합니다.
    """
    try:
        start_time = time.time()
        
        final_revenue = run_test(config)

        summary = BacktestSummary(
            final_revenue=final_revenue,
            buy_and_hold_return=10.5, 
            best_config=config,
            total_trades=50 
        )

        chart_df = df.iloc[-100:].copy() 
        chart_data = chart_df[['c', 'wma7', 'vwap']].to_dict(orient="records")

        print(f"Backtest completed in {time.time() - start_time:.2f}s")
        
        return BacktestResponse(
            summary=summary,
            chart_data=chart_data
        )

    except Exception as e:
        return {"error": str(e)}

@app.get("/api/backtest/results/{test_id}", tags=["Backtesting"])
async def get_backtest_results(test_id: str):
    """
    저장된 특정 ID의 백테스트 결과를 로드하여 반환합니다.
    """
    results = load_backtest_results(test_id)
    
    if results is None:
        raise HTTPException(status_code=404, detail=f"Test results for ID {test_id} not found.")
        
    return results