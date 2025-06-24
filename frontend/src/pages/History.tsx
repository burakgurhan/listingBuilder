import React from 'react';
import { History as HistoryIcon, Calendar, ExternalLink, Trash2 } from 'lucide-react';

function History() {
  // Mock data for demonstration
  const historyItems = [
    {
      id: 1,
      url: 'https://www.amazon.com/dp/B0BP7M5F3M',
      date: '2024-01-15',
      title: 'Premium Wireless Bluetooth Headphones',
      status: 'completed'
    },
    {
      id: 2,
      url: 'https://www.amazon.com/dp/B08N5WRWNW',
      date: '2024-01-14',
      title: 'Smart Home Security Camera',
      status: 'completed'
    },
    {
      id: 3,
      url: 'https://www.amazon.com/dp/B07XJ8C8F5',
      date: '2024-01-13',
      title: 'Portable Phone Charger',
      status: 'completed'
    }
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center mb-8">
        <HistoryIcon className="h-8 w-8 text-blue-600 mr-3" />
        <h1 className="text-3xl font-bold text-gray-900">Generation History</h1>
      </div>

      <div className="bg-white rounded-2xl shadow-lg border border-gray-100">
        {historyItems.length === 0 ? (
          <div className="p-12 text-center">
            <HistoryIcon className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No history yet</h3>
            <p className="text-gray-600">Your generated content will appear here</p>
          </div>
        ) : (
          <div className="p-6">
            <div className="overflow-hidden">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Product
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      URL
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {historyItems.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{item.title}</div>
                        <div className="text-sm text-gray-500">Generated content</div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center text-sm text-blue-600">
                          <ExternalLink className="h-4 w-4 mr-1" />
                          <span className="truncate max-w-xs">{item.url}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center text-sm text-gray-500">
                          <Calendar className="h-4 w-4 mr-1" />
                          {new Date(item.date).toLocaleDateString()}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex items-center space-x-3">
                          <button className="text-blue-600 hover:text-blue-900">
                            View
                          </button>
                          <button className="text-red-600 hover:text-red-900">
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default History;