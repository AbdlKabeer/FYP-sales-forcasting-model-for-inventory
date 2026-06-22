"use client";

import { useEffect, useState, FormEvent } from "react";
import { fetchAPI } from "@/lib/api";
import ForecastChart from "@/components/ForecastChart";

type Product = {
  id: number;
  name: string;
  category: string;
  cost_price: number;
  selling_price: number;
  stock_quantity: number;
};

type ForecastPoint = {
  date: string;
  predicted_quantity: number;
};

type Metrics = {
  training_rmse: number;
  training_mae: number;
  r2_score: number;
};

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProductId, setSelectedProductId] = useState<number | null>(null);
  
  const [forecast, setForecast] = useState<ForecastPoint[]>([]);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [modelType, setModelType] = useState("linear");

  // New Product Form State
  const [isAddingProduct, setIsAddingProduct] = useState(false);
  const [newProductName, setNewProductName] = useState("");
  const [newProductCategory, setNewProductCategory] = useState("Electronics");
  const [newProductCost, setNewProductCost] = useState("");
  const [newProductSelling, setNewProductSelling] = useState("");
  const [newProductStock, setNewProductStock] = useState("");

  // Fetch Products
  const loadProducts = async () => {
    try {
      const data = await fetchAPI("products/");
      setProducts(data);
      if (data.length > 0 && selectedProductId === null) {
        setSelectedProductId(data[0].id);
      }
    } catch (e) {
      console.error("Failed to fetch products", e);
    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

  // Fetch Forecast when selected product or model changes
  useEffect(() => {
    async function loadForecast() {
      if (!selectedProductId) return;
      setLoading(true);
      try {
        const data = await fetchAPI("forecast/", {
          method: "POST",
          body: JSON.stringify({ product_id: selectedProductId, days: 7, model_type: modelType }),
        });
        setForecast(data.forecast || []);
        setMetrics(data.metrics || null);
      } catch (e) {
        console.error("Failed to load forecast", e);
        setForecast([]);
        setMetrics(null);
      } finally {
        setLoading(false);
      }
    }
    loadForecast();
  }, [selectedProductId, modelType]);

  const handleAddProduct = async (e: FormEvent) => {
    e.preventDefault();
    const prod = {
      name: newProductName,
      category: newProductCategory,
      cost_price: parseFloat(newProductCost),
      selling_price: parseFloat(newProductSelling),
      stock_quantity: parseInt(newProductStock, 10),
    };

    try {
      const data = await fetchAPI("products/", {
        method: "POST",
        body: JSON.stringify(prod),
      });
      // Refresh products and select new one
      await loadProducts();
      setSelectedProductId(data.id);
      setIsAddingProduct(false);
      // Reset form
      setNewProductName("");
      setNewProductCost("");
      setNewProductSelling("");
      setNewProductStock("");
    } catch (error) {
      console.error("Failed to add product", error);
      alert("Failed to add product.");
    }
  };

  // Compute total predicted
  const totalPredicted = forecast.reduce((acc, curr) => acc + curr.predicted_quantity, 0);

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Sales & Budget Dashboard
            </h1>
            <p className="text-gray-500">Overview of inventory and predictions</p>
          </div>
          
          {/* Controls: Model & Product Selection */}
          <div className="flex flex-col md:flex-row gap-4 items-center w-full md:w-auto">
            <select 
              className="bg-white border rounded-lg px-4 py-2 shadow-sm text-gray-700 w-full md:w-auto"
              value={selectedProductId || ""}
              onChange={(e) => setSelectedProductId(Number(e.target.value))}
            >
              <option value="" disabled>Select a product</option>
              {products.map(p => (
                <option key={p.id} value={p.id}>{p.name} (ID: {p.id})</option>
              ))}
            </select>
            
            <div className="flex gap-2 bg-white p-1 rounded-lg shadow-sm border w-full md:w-auto justify-center">
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
            
            <button 
              onClick={() => setIsAddingProduct(!isAddingProduct)}
              className="px-4 py-2 bg-gray-900 text-white rounded-lg shadow-sm text-sm font-medium hover:bg-gray-800 transition-colors w-full md:w-auto"
            >
              {isAddingProduct ? 'Cancel' : '+ Add Product'}
            </button>
          </div>
        </header>

        {/* Add Product Form Panel */}
        {isAddingProduct && (
          <section className="mb-8 bg-white p-6 rounded-xl shadow-sm border">
            <h2 className="text-lg font-semibold mb-4 text-gray-800">Add New Product</h2>
            <form onSubmit={handleAddProduct} className="grid grid-cols-1 md:grid-cols-6 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">Product Name</label>
                <input required type="text" value={newProductName} onChange={e => setNewProductName(e.target.value)} className="w-full border rounded-md px-3 py-2 text-sm text-gray-900" placeholder="e.g. Wireless Mouse" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                <input required type="text" value={newProductCategory} onChange={e => setNewProductCategory(e.target.value)} className="w-full border rounded-md px-3 py-2 text-sm text-gray-900" placeholder="Electronics" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Cost Price ($)</label>
                <input required type="number" step="0.01" value={newProductCost} onChange={e => setNewProductCost(e.target.value)} className="w-full border rounded-md px-3 py-2 text-sm text-gray-900" placeholder="10.00" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Selling Price ($)</label>
                <input required type="number" step="0.01" value={newProductSelling} onChange={e => setNewProductSelling(e.target.value)} className="w-full border rounded-md px-3 py-2 text-sm text-gray-900" placeholder="25.00" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Initial Stock</label>
                <input required type="number" value={newProductStock} onChange={e => setNewProductStock(e.target.value)} className="w-full border rounded-md px-3 py-2 text-sm text-gray-900" placeholder="100" />
              </div>
              <div className="md:col-span-6 flex justify-end mt-2">
                <button type="submit" className="bg-blue-600 text-white px-6 py-2 rounded-md font-medium text-sm hover:bg-blue-700 transition-colors">
                  Save Product
                </button>
              </div>
            </form>
          </section>
        )}

        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-sm border">
            <h3 className="text-sm font-medium text-gray-500">Total Products</h3>
            <p className="text-2xl font-bold text-gray-900">{products.length}</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border">
            <h3 className="text-sm font-medium text-gray-500">
              Projected Revenue (7 days)
            </h3>
            <p className="text-2xl font-bold text-green-600">$7,240</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border">
            <h3 className="text-sm font-medium text-gray-500">Budget Status</h3>
            <p className="text-2xl font-bold text-blue-600">On Track</p>
          </div>
        </section>

        <section className="mb-8">
          {!loading ? (
            <ForecastChart
              data={forecast}
              title={`7-Day Sales Forecast (${modelType === 'linear' ? 'Linear Regression' : 'SARIMA Model'})`}
            />
          ) : (
            <div className="h-[400px] flex items-center justify-center bg-white rounded-lg shadow-sm border">
              <div className="animate-pulse text-gray-400 font-medium">Loading Forecast...</div>
            </div>
          )}
        </section>

        {/* Forecast Breakdown */}
        {!loading && forecast.length > 0 && (
          <section className="bg-white p-6 rounded-xl shadow-sm border">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-2">Forecast Breakdown</h2>
                <p className="text-gray-600 text-sm max-w-2xl">
                  {modelType === 'linear' 
                    ? "Linear Regression fits a straight line through the historical sales data. It is excellent for identifying general growth or decline trends, but it does not account for recurring weekly patterns."
                    : "The SARIMA model analyzes both the overall trend and seasonal cycles. It is designed to capture complex patterns, such as sales spiking every Friday, resulting in a more nuanced prediction."}
                </p>
              </div>
              <div className="mt-4 md:mt-0 flex gap-6 text-right">
                {metrics && (
                  <>
                    <div>
                      <p className="text-sm text-gray-500 font-medium" title="Root Mean Squared Error">RMSE</p>
                      <p className="text-lg font-bold text-gray-900">{metrics.training_rmse}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 font-medium" title="Mean Absolute Error">MAE</p>
                      <p className="text-lg font-bold text-gray-900">{metrics.training_mae}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 font-medium" title="R-Squared Score">R² Score</p>
                      <p className="text-lg font-bold text-gray-900">{metrics.r2_score}</p>
                    </div>
                  </>
                )}
                <div>
                  <p className="text-sm text-gray-500 font-medium">Total Predicted Units</p>
                  <p className="text-lg font-bold text-blue-600">{totalPredicted}</p>
                </div>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="py-3 px-4 text-sm font-semibold text-gray-600">Date</th>
                    <th className="py-3 px-4 text-sm font-semibold text-gray-600">Predicted Quantity</th>
                  </tr>
                </thead>
                <tbody>
                  {forecast.map((point, i) => {
                    const d = new Date(point.date);
                    return (
                      <tr key={i} className="border-b border-gray-100 last:border-0 hover:bg-gray-50">
                        <td className="py-3 px-4 text-sm text-gray-800">
                          {d.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })}
                        </td>
                        <td className="py-3 px-4 text-sm font-medium text-gray-900">
                          {point.predicted_quantity} units
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </div>
    </main>
  );
}
