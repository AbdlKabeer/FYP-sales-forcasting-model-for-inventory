"use client";

import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from "recharts";

interface ForecastData {
    date: string;
    predicted_quantity: number;
}

export default function ForecastChart({ data, title }: { data: ForecastData[], title?: string }) {
    // Format dates for display
    const formattedData = data.map((item) => ({
        ...item,
        date: new Date(item.date).toLocaleDateString(),
    }));

    return (
        <div className="h-[400px] w-full bg-white p-4 rounded-lg shadow-sm">
            <h3 className="text-lg font-semibold mb-4">{title || "7-Day Sales Forecast"}</h3>
            <ResponsiveContainer width="100%" height="100%">
                <LineChart
                    data={formattedData}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line
                        type="monotone"
                        dataKey="predicted_quantity"
                        stroke="#8884d8"
                        activeDot={{ r: 8 }}
                        name="Predicted Sales"
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
