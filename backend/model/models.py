from pydantic import BaseModel
from typing import List, Dict, Any

class BacktestSummary(BaseModel):
    """최종 수익률, 최대 낙폭 등 핵심 KPI"""
    final_revenue: float
    buy_and_hold_return: float
    best_config: Dict[str, Any]
    total_trades: int

class CandleData(BaseModel):
    """캔들 차트 및 지표 라인 데이터"""
    timestamp: str 
    c: float       
    wma7: float
    vwap: float


class BacktestResponse(BaseModel):
    summary: BacktestSummary
    chart_data: List[CandleData]