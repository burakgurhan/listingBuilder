import { useState, useEffect } from 'react';
import { History as HistoryIcon, Calendar, ExternalLink, Trash2, Loader2 } from 'lucide-react';
import { apiClient } from '../api/client';
import { useAuth } from '../contexts/AuthContext';

interface HistoryItem {
  id: number;
  url: string;
  date: string;
  title: string | null;
  status: string;
}

function History() {
  const [historyItems, setHistoryItems] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const { showToast } = useAuth();

  const fetchHistory = async () => {
    try {
      const response = await apiClient.get('/history');
      setHistoryItems(response.data);
    } catch (error) {
      showToast('Failed to load history', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleDelete = async (id: number) => {
    try {
      await apiClient.delete(`/history/${id}`);
      setHistoryItems(prev => prev.filter(item => item.id !== id));
      showToast('Item deleted', 'success');
    } catch (error) {
      showToast('Failed to delete item', 'error');
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center mb-8">
        <HistoryIcon className="h-8 w-8 text-blue-600 mr-3" />
        <h1 className="text-3xl font-bold text-gray-900">Generation History</h1>
      </div>

      <div className="bg-white rounded-2xl shadow-lg border border-gray-100">
        {loading ? (
          <div className="p-12 text-center">
            <Loader2 className="animate-spin h-12 w-12 text-blue-600 mx-auto mb-4" />
            <p className="text-gray-600">Loading history...</p>
          </div>
        ) : historyItems.length === 0 ? (
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
                        <div className="text-sm font-medium text-gray-900">
                          {item.title || (item.status === 'pending' || item.status === 'processing' ? 'Generating...' : 'Untitled')}
                        </div>
                        <div className="text-xs mt-1 text-gray-500 uppercase tracking-wide">
                          Status: <span className={item.status === 'completed' ? 'text-green-600' : (item.status === 'failed' ? 'text-red-500' : 'text-blue-500')}>{item.status}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center text-sm text-blue-600">
                          <ExternalLink className="h-4 w-4 mr-1 min-w-4" />
                          <a href={item.url} target="_blank" rel="noopener noreferrer" className="truncate max-w-[200px] inline-block hover:underline">{item.url}</a>
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
                          <button onClick={() => handleDelete(item.id)} className="text-red-600 hover:text-red-900 p-2 hover:bg-red-50 rounded-full transition-colors">
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