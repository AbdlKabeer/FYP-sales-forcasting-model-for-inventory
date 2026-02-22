"use client";

import { useEffect, useState } from "react";
import { fetchAPI } from "@/lib/api";
import ForecastChart from "@/components/ForecastChart";

export default function Home() {
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modelType, setModelType] = useState("linear");

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        // Hardcoded product ID 2 for demo purposes
        const data = await fetchAPI("/forecast/", {
          method: "POST",
          body: JSON.stringify({ product_id: 2, days: 7, model_type: modelType }),
        });
        setForecast(data);
      } catch (e) {
        console.error("Failed to load forecast", e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [modelType]);

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Sales & Budget Dashboard
            </h1>
            <p className="text-gray-500">Overview of inventory and predictions</p>
          </div>
          <div className="flex gap-2 bg-white p-1 rounded-lg shadow-sm border">
            <button
              onClick={() => setModelType("linear")}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${modelType === 'linear' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              Linear
            </button>
            <button
              onClick={() => setModelType("sarima")}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${modelType === 'sarima' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              SARIMA
            </button>
          </div>
        </header>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-sm">
            <h3 className="text-sm font-medium text-gray-500">Total Products</h3>
            <p className="text-2xl font-bold">1</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm">
            <h3 className="text-sm font-medium text-gray-500">
              Projected Revenue (7 days)
            </h3>
            <p className="text-2xl font-bold text-green-600">$7,240</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm">
            <h3 className="text-sm font-medium text-gray-500">Budget Status</h3>
            <p className="text-2xl font-bold text-blue-600">On Track</p>
          </div>
        </section>

        <section>
          {!loading ? (
            <ForecastChart
              data={forecast}
              title={`7-Day Sales Forecast (${modelType === 'linear' ? 'Linear Regression' : 'SARIMA Model'})`}
            />
          ) : (
            <div className="h-[400px] flex items-center justify-center bg-white rounded-lg shadow-sm border">
              <div className="animate-pulse text-gray-400">Loading Forecast...</div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
