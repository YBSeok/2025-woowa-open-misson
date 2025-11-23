import './index.css';
import Main from './pages/Main';
import BacktestResults from './pages/BacktestResults';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './components/common/layout/MainLayout';

export default function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes> 
          <Route path="/" element={
            <MainLayout>
              <Main />
            </MainLayout>
          } />
          <Route path="/backtest" element={
            <MainLayout>
              <BacktestResults />
            </MainLayout>
          } />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
