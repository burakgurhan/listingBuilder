import React from 'react';
import { CheckCircle, XCircle, Info } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

function Toast() {
  const { toast } = useAuth();

  if (!toast) return null;

  const icons = {
    success: CheckCircle,
    error: XCircle,
    info: Info,
  };

  const colors = {
    success: 'bg-green-50 text-green-800 border-green-200',
    error: 'bg-red-50 text-red-800 border-red-200',
    info: 'bg-blue-50 text-blue-800 border-blue-200',
  };

  const Icon = icons[toast.type];

  return (
    <div className="fixed top-4 right-4 z-50 animate-in slide-in-from-right duration-300">
      <div className={`flex items-center p-4 rounded-lg border shadow-lg ${colors[toast.type]}`}>
        <Icon className="h-5 w-5 mr-2 flex-shrink-0" />
        <p className="text-sm font-medium">{toast.message}</p>
      </div>
    </div>
  );
}

export default Toast;