import { useState, useEffect } from 'react';
import axios from 'axios';
import Charts from '@/components/pages/backtest/Charts';

export default function BacktestResults() {

  const BACKEND_URL = 'http://localhost:8000';
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const TEST_ID = "optimized_run_1"; 

  useEffect(() => {
      const fetchResults = async () => {
          try {
              const response = await axios.get(`${BACKEND_URL}/api/backtest/results/${TEST_ID}`);
              setResults(response.data);
              setLoading(false);
          } catch (error) {
              console.error("Error fetching backtest results:", error);
              setLoading(false);
              setResults(null);
          }
      };
      fetchResults();
  }, [TEST_ID]);

  if (loading) return <div>데이터 로딩 중...</div>;
  if (!results) return <div>결과를 찾을 수 없습니다.</div>;

  return (
  
    <div className="flex-1 p-8 bg-white min-h-screen">
      <h1 className="text-3xl font-bold text-blue-700 mb-6">
        📊 백테스트 결과 분석
      </h1>
      <div className="p-8">
            <h2>최종 수익: {results.summary.final_revenue}</h2>
            <Charts data={results.chart_data} />
        </div>
      
    </div>
  
  );
}  