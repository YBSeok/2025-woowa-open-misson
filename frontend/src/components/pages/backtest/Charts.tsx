

import React from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  Line,
  ReferenceArea 
} from 'recharts';

interface Props {
  data: any[];
}

export default function Charts({ data }: Props) {
  if (!data || data.length === 0) {
    return <div className="text-center py-10 text-gray-500">데이터를 불러올 수 없습니다.</div>;
  }

  const processedData = data.map(item => ({
    ...item,
    candle_y1: Math.min(item.o, item.c),
    candle_y2: Math.max(item.o, item.c),
  }));

  const yAxisDomain = [
    Math.min(...processedData.map(d => d.l)), 
    Math.max(...processedData.map(d => d.h))  
  ];

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mt-8">
      <h3 className="text-xl font-semibold mb-4 text-gray-700">가격 및 지표 추이</h3>
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart
          data={processedData}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis 
            dataKey="timestamp" 
            tickFormatter={(tick) => new Date(tick).toLocaleDateString()} 
            minTickGap={30} 
          />
          <YAxis 
            yAxisId="price" 
            domain={yAxisDomain} 
            orientation="right" 
            tickFormatter={(tick) => tick.toLocaleString()}
            allowDataOverflow={true}
          />
          <Tooltip 
            formatter={(value, name: string | number, props) => {
              if (typeof name === "string" && name.includes('candle')) return null; 
              return [value.toLocaleString(), name];
            }}
            labelFormatter={(label) => `날짜: ${new Date(label).toLocaleString()}`}
          />
          <Legend />

          {processedData.map((entry, index) => (
            <React.Fragment key={`candle-${index}`}>
              <ReferenceArea
                yAxisId="price"
                x={entry.timestamp}
                x2={entry.timestamp}
                y1={entry.candle_y1}
                y2={entry.candle_y2}
                fill={entry.o < entry.c ? "#4CAF50" : "#F44336"} 
                fillOpacity={0.8}
                stroke="none"
              />
              <Line 
                yAxisId="price"
                dataKey="h" 
                dot={false} 
                stroke="transparent" 
                isAnimationActive={false}
              />
               <Line 
                yAxisId="price"
                dataKey="l" 
                dot={false} 
                stroke="transparent" 
                isAnimationActive={false}
              />
            </React.Fragment>
          ))}
            <Line
                yAxisId="price"
                dataKey="h"
                stroke="#ccc"
                strokeWidth={1}
                dot={false}
                isAnimationActive={false}
            />
            <Line
                yAxisId="price"
                dataKey="l"
                stroke="#ccc"
                strokeWidth={1}
                dot={false}
                isAnimationActive={false}
            />


          <Line 
            yAxisId="price" 
            type="monotone" 
            dataKey="wma7" 
            stroke="#8884d8" 
            strokeWidth={2} 
            dot={false} 
            name="WMA 7"
          />
          
          <Line 
            yAxisId="price" 
            type="monotone" 
            dataKey="vwap" 
            stroke="#82ca9d" 
            strokeWidth={2} 
            dot={false} 
            name="VWAP"
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}