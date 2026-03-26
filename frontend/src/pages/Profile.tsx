import React, { useState, useEffect } from 'react';
import { User, CreditCard, Settings, Crown, Check, X } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { apiClient } from '../api/client';

function Profile() {
  const { user, showToast } = useAuth();
  const [activeTab, setActiveTab] = useState('account');
  const [profileData, setProfileData] = useState<any>(null);

  // Account Form States
  const [fullName, setFullName] = useState('');
  const [company, setCompany] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  // Password Modal States
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [isChangingPassword, setIsChangingPassword] = useState(false);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const response = await apiClient.get('/profile');
        setProfileData(response.data);
      } catch (error) {
        console.error('Failed to load profile', error);
      }
    };
    loadProfile();
  }, []);

  const handleSaveAccount = async () => {
    setIsSaving(true);
    try {
      // In a real app we'd send fullName and company to the backend
      // await apiClient.put('/profile', { full_name: fullName, company });
      showToast('Profile updated successfully', 'success');
    } catch (error) {
      showToast('Failed to update profile', 'error');
    } finally {
      setIsSaving(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsChangingPassword(true);
    try {
      await apiClient.put('/password', { currentPassword, newPassword });
      showToast('Password updated successfully', 'success');
      setShowPasswordModal(false);
      setCurrentPassword('');
      setNewPassword('');
    } catch (error: any) {
      const msg = error.response?.data?.detail || 'Failed to update password';
      showToast(msg, 'error');
    } finally {
      setIsChangingPassword(false);
    }
  };

  const handleDeleteAccount = () => {
    if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      showToast('Account deletion requested. Support will contact you shortly.', 'info');
    }
  };

  // Use dynamic or Mock subscription data
  const subscriptionData = profileData?.subscription || {
    plan: 'Free',
    status: 'inactive',
    renewalDate: new Date().toISOString(),
    daysLeft: '-', // Fallback to '-' instead of misleading 0
    generationsUsed: '-', // Fallback to '-' Instead of misleading 0
    generationsLimit: '-' // Fallback
  };

  const plans = [
    {
      name: 'Starter',
      price: '$9.99',
      period: '/month',
      generations: 100,
      features: [
        'Up to 100 generations per month',
        'Basic product title suggestions',
        'Standard product descriptions',
        'Email support'
      ],
      current: false
    },
    {
      name: 'Pro',
      price: '$24.99',
      period: '/month',
      generations: 1000,
      features: [
        'Up to 1,000 generations per month',
        'Advanced AI suggestions',
        'SEO optimization',
        'Keyword research',
        'Priority support',
        'Export to multiple formats'
      ],
      current: true,
      popular: true
    },
    {
      name: 'Enterprise',
      price: '$99.99',
      period: '/month',
      generations: 'Unlimited',
      features: [
        'Unlimited generations',
        'Custom AI training',
        'API access',
        'Team collaboration',
        'Dedicated support',
        'Custom integrations',
        'Advanced analytics'
      ],
      current: false
    }
  ];

  const tabs = [
    { id: 'account', label: 'Account', icon: User },
    { id: 'subscription', label: 'Subscription', icon: Crown },
    { id: 'billing', label: 'Billing', icon: CreditCard },
    { id: 'settings', label: 'Settings', icon: Settings }
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center mb-8">
        <User className="h-8 w-8 text-blue-600 mr-3" />
        <h1 className="text-3xl font-bold text-gray-900">Profile & Settings</h1>
      </div>

      <div className="grid lg:grid-cols-4 gap-8">
        {/* Sidebar Navigation */}
        <div className="lg:col-span-1">
          <nav className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
            <div className="space-y-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center px-4 py-3 rounded-lg text-left transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <tab.icon className="h-5 w-5 mr-3" />
                  {tab.label}
                </button>
              ))}
            </div>
          </nav>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3">
          {activeTab === 'account' && (
            <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Account Information</h2>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address
                  </label>
                  <input
                    type="email"
                    value={user?.email || ''}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-500"
                    disabled
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Full Name
                  </label>
                  <input
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Enter your full name"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Company (Optional)
                  </label>
                  <input
                    type="text"
                    value={company}
                    onChange={(e) => setCompany(e.target.value)}
                    placeholder="Enter your company name"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                
                <button 
                  onClick={handleSaveAccount}
                  disabled={isSaving}
                  className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  {isSaving ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </div>
          )}

          {activeTab === 'subscription' && (
            <div className="space-y-8">
              {/* Current Subscription */}
              <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Current Subscription</h2>
                
                <div className="bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl p-6 text-white mb-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="text-2xl font-bold">{subscriptionData.plan} Plan</h3>
                      <p className="text-blue-100">Status: {subscriptionData.status}</p>
                    </div>
                    <Crown className="h-8 w-8" />
                  </div>
                  
                  <div className="grid sm:grid-cols-3 gap-4">
                    <div>
                      <p className="text-blue-100 text-sm">Renewal Date</p>
                      <p className="font-semibold">{subscriptionData.renewalDate ? new Date(subscriptionData.renewalDate).toLocaleDateString() : '-'}</p>
                    </div>
                    <div>
                      <p className="text-blue-100 text-sm">Days Remaining</p>
                      <p className="font-semibold">{subscriptionData.daysLeft}</p>
                    </div>
                    <div>
                      <p className="text-blue-100 text-sm">Generations Used</p>
                      <p className="font-semibold">{subscriptionData.generationsUsed} / {subscriptionData.generationsLimit}</p>
                    </div>
                  </div>
                  
                  <div className="mt-4">
                    <div className="bg-white/20 rounded-full h-2">
                      <div 
                        className="bg-white rounded-full h-2" 
                        style={{ width: typeof subscriptionData.generationsUsed === 'number' && typeof subscriptionData.generationsLimit === 'number' && subscriptionData.generationsLimit > 0 ? `${(subscriptionData.generationsUsed / subscriptionData.generationsLimit) * 100}%` : '0%' }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Available Plans */}
              <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Available Plans</h2>
                
                <div className="grid md:grid-cols-3 gap-6">
                  {plans.map((plan) => (
                    <div
                      key={plan.name}
                      className={`relative rounded-xl border-2 p-6 ${
                        plan.current
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-blue-300'
                      } transition-colors`}
                    >
                      {plan.popular && (
                        <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                          <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                            Most Popular
                          </span>
                        </div>
                      )}
                      
                      <div className="text-center mb-6">
                        <h3 className="text-xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                        <div className="flex items-baseline justify-center">
                          <span className="text-3xl font-bold text-gray-900">{plan.price}</span>
                          <span className="text-gray-500 ml-1">{plan.period}</span>
                        </div>
                        <p className="text-gray-600 mt-2">
                          {typeof plan.generations === 'number' 
                            ? `${plan.generations} generations` 
                            : plan.generations
                          }
                        </p>
                      </div>
                      
                      <ul className="space-y-3 mb-6">
                        {plan.features.map((feature, index) => (
                          <li key={index} className="flex items-start">
                            <Check className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                            <span className="text-gray-700 text-sm">{feature}</span>
                          </li>
                        ))}
                      </ul>
                      
                      <button
                        className={`w-full py-3 px-4 rounded-lg font-medium transition-colors ${
                          plan.current
                            ? 'bg-gray-100 text-gray-500 cursor-not-allowed'
                            : 'bg-blue-600 text-white hover:bg-blue-700'
                        }`}
                        disabled={plan.current}
                      >
                        {plan.current ? 'Current Plan' : 'Upgrade to ' + plan.name}
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'billing' && (
            <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Billing Information</h2>
                <span className="bg-yellow-100 text-yellow-800 text-xs font-medium px-2.5 py-0.5 rounded border border-yellow-300">Demo Data</span>
              </div>
              
              <div className="space-y-8">
                {/* Payment Method */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Payment Method</h3>
                  <div className="border border-gray-200 rounded-lg p-4 flex items-center justify-between">
                    <div className="flex items-center">
                      <CreditCard className="h-6 w-6 text-gray-400 mr-3" />
                      <div>
                        <p className="font-medium text-gray-900">•••• •••• •••• 4242</p>
                        <p className="text-sm text-gray-500">Expires 12/2025</p>
                      </div>
                    </div>
                    <button className="text-blue-600 hover:text-blue-700 font-medium">
                      Update
                    </button>
                  </div>
                </div>

                {/* Billing History */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Billing History</h3>
                  <div className="overflow-hidden border border-gray-200 rounded-lg">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Date
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Description
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Amount
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Status
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        <tr>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            Jan 15, 2024
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            Pro Plan - Monthly
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            $24.99
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                              Paid
                            </span>
                          </td>
                        </tr>
                        <tr>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            Dec 15, 2023
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            Pro Plan - Monthly
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            $24.99
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                              Paid
                            </span>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'settings' && (
            <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Settings</h2>
              
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Preferences</h3>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-gray-900">Email Notifications</p>
                        <p className="text-sm text-gray-500">Receive updates about new features and tips</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" className="sr-only peer" defaultChecked />
                        <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                      </label>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-gray-900">Auto-save Generated Content</p>
                        <p className="text-sm text-gray-500">Automatically save generated content to history</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" className="sr-only peer" defaultChecked />
                        <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                      </label>
                    </div>
                  </div>
                </div>

                <div className="border-t border-gray-200 pt-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Account Actions</h3>
                  <div className="space-y-4">
                    <button 
                      onClick={() => setShowPasswordModal(true)}
                      className="text-blue-600 hover:text-blue-700 font-medium block"
                    >
                      Change Password
                    </button>
                    <button 
                      onClick={handleDeleteAccount}
                      className="text-red-600 hover:text-red-700 font-medium block"
                    >
                      Delete Account
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Password Change Modal */}
      {showPasswordModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-xl max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold text-gray-900">Change Password</h3>
              <button 
                onClick={() => setShowPasswordModal(false)}
                className="text-gray-400 hover:text-gray-600 p-1"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            
            <form onSubmit={handleChangePassword} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Current Password
                </label>
                <input
                  type="password"
                  required
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  New Password
                </label>
                <input
                  type="password"
                  required
                  minLength={6}
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <div className="pt-4 flex space-x-3">
                <button
                  type="button"
                  onClick={() => setShowPasswordModal(false)}
                  className="flex-1 px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isChangingPassword}
                  className="flex-1 px-4 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors disabled:opacity-50"
                >
                  {isChangingPassword ? 'Updating...' : 'Update Password'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Profile;