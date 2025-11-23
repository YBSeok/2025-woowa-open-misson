
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = "http://localhost:8000"; 

const DEFAULT_CONFIG = {
    'revenue_rate': 0.014,
    'max_loss_rate': 0.2,
    'increase_rate': 0.2,
    'buy_cnt_limit': 7,
    'buy_amt_unit': 4.5
};

export default function BacktestRunButton() {
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate(); 

    const handleRunTest = async () => {
        setIsLoading(true);
        
        try {
            const response = await axios.post(`${BACKEND_URL}/api/backtest`, DEFAULT_CONFIG);
            
            const testId = response.data.test_id; 

            if (testId) {
                alert(`✅ 최적화 완료! 결과 ID: ${testId}`);
                navigate(`/results/${testId}`); 
            } else {
                alert("❌ 오류: 백테스트는 완료되었으나 결과 ID를 받지 못했습니다.");
            }

        } catch (error) {
            console.error("백테스트 실행 중 오류 발생:", error);
            alert(`❌ 테스트 실행 실패: ${error instanceof Error ? error.message : '알 수 없는 오류'}`);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <button
            onClick={handleRunTest}
            disabled={isLoading}
            className={`
                px-8 py-3 text-lg font-bold text-white rounded-lg shadow-xl transition duration-300
                ${isLoading 
                    ? 'bg-gray-500 cursor-not-allowed flex items-center justify-center' 
                    : 'bg-green-600 hover:bg-green-700 transform hover:scale-105'
                }
            `}
        >
            {isLoading ? (
                <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    최적화 실행 중...
                </>
            ) : (
                '🚀 최적화 테스트 시작'
            )}
        </button>
    );
}