import { NavLink } from 'react-router-dom';

export default function Sidebar() {
    const getLinkClasses = (isActive: boolean) => {
        const baseClasses = "flex items-center px-4 py-2 rounded-lg font-medium transition duration-150 ease-in-out";
        const activeClasses = "bg-blue-600 text-white shadow-md";
        const inactiveClasses = "text-gray-700 hover:bg-gray-100";
        
        return `${baseClasses} ${isActive ? activeClasses : inactiveClasses}`;
    };

    return (
      <aside className="w-64 bg-white p-4 pt-6 shadow-lg">
          <nav>
              <ul>
                  <li>
                      <NavLink
                          to="/"
                          className={({ isActive }) => getLinkClasses(isActive)}
                          end 
                      >
                          <span className="text-lg">🏠</span>
                          <span className="ml-2">홈</span>
                      </NavLink>
                  </li>

                 
                  <li className="mt-6">
                      <span className="text-gray-400 text-xs uppercase font-semibold">
                          통계 및 분석
                      </span>
                      <ul className="mt-2 space-y-1">
                          <li>
                              <NavLink
                                  to="/backtest"
                                  className={({ isActive }) => getLinkClasses(isActive)}
                              >
                                  <span className="text-lg">📊</span>
                                  <span className="ml-2">백테스트 결과</span>
                              </NavLink>
                          </li>
                      </ul>
                  </li>
              
              </ul>
          </nav>
      </aside>
  );
}