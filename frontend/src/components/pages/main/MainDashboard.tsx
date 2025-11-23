import BacktestRunButton from "./BacktestRunButton";

export default function MainDashboard() {
    return (
      <main className="flex-1 p-8 bg-gray-50">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">
          Bitsrobot Dashboard
        </h1>
  
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
                <h2 className="text-2xl font-semibold mb-4 text-gray-700">
                    알고리즘 최적화 및 백테스팅
                </h2>
                <BacktestRunButton /> 
            </div>
       
      </main>
    );
  }