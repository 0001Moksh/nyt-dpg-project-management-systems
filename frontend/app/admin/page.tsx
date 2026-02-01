'use client';

import React, { useState } from 'react';
import { StatCard } from '@/components/premium/StatCard';
import { Users, Shield, CheckCircle, AlertCircle, Settings, Plus, Search } from 'lucide-react';

export default function AdminDashboard() {
  const [searchUser, setSearchUser] = useState('');

  const stats = [
    {
      title: 'Total Users',
      value: '342',
      subtitle: 'Active accounts',
      icon: <Users className="w-6 h-6" />,
      trend: { value: 15, isPositive: true },
      variant: 'default' as const,
    },
    {
      title: 'Active Projects',
      value: '28',
      subtitle: 'In Progress',
      icon: <CheckCircle className="w-6 h-6" />,
      trend: { value: 8, isPositive: true },
      variant: 'success' as const,
    },
    {
      title: 'Pending Approvals',
      value: '7',
      subtitle: 'Needs Action',
      icon: <AlertCircle className="w-6 h-6" />,
      trend: { value: 2, isPositive: false },
      variant: 'warning' as const,
    },
    {
      title: 'System Health',
      value: '99.8%',
      subtitle: 'Uptime',
      icon: <Shield className="w-6 h-6" />,
      trend: { value: 0.2, isPositive: true },
      variant: 'success' as const,
    },
  ];

  const users = [
    { id: '1', name: 'Alice Johnson', email: 'alice@college.edu', role: 'Student', status: 'Active', joined: 'Jan 15, 2026' },
    { id: '2', name: 'Bob Smith', email: 'bob@college.edu', role: 'Accountant', status: 'Active', joined: 'Dec 20, 2025' },
    { id: '3', name: 'Carol White', email: 'carol@college.edu', role: 'Admin', status: 'Active', joined: 'Oct 1, 2025' },
    { id: '4', name: 'David Brown', email: 'david@college.edu', role: 'Student', status: 'Inactive', joined: 'Jan 10, 2026' },
    { id: '5', name: 'Eve Davis', email: 'eve@college.edu', role: 'Student', status: 'Active', joined: 'Jan 20, 2026' },
  ];

  const pendingApprovals = [
    { id: '1', type: 'Project', title: 'AI Research Initiative', requester: 'Prof. Smith', status: 'Pending', date: 'Feb 4' },
    { id: '2', type: 'User', title: 'New User Registration', requester: 'Frank Wilson', status: 'Pending', date: 'Feb 3' },
    { id: '3', type: 'Budget', title: 'Department Budget Increase', requester: 'Finance Dept', status: 'Reviewing', date: 'Feb 2' },
    { id: '4', type: 'Project', title: 'Mobile App Development', requester: 'Tech Team', status: 'Pending', date: 'Feb 1' },
  ];

  const systemLogs = [
    { id: '1', action: 'User Login', user: 'alice@college.edu', timestamp: '2 mins ago', status: 'Success' },
    { id: '2', action: 'Project Created', user: 'bob@college.edu', timestamp: '15 mins ago', status: 'Success' },
    { id: '3', action: 'Invoice Generated', user: 'carol@college.edu', timestamp: '1 hour ago', status: 'Success' },
    { id: '4', action: 'Budget Approved', user: 'admin@college.edu', timestamp: '3 hours ago', status: 'Success' },
    { id: '5', action: 'User Deactivated', user: 'carol@college.edu', timestamp: '1 day ago', status: 'Success' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900">Admin Dashboard</h1>
              <p className="text-gray-600 mt-2">System overview and user management</p>
            </div>
            <div className="flex gap-3">
              <button className="border border-gray-300 text-gray-700 font-medium py-2 px-4 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                <Settings className="w-4 h-4" />
                Settings
              </button>
              <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg flex items-center gap-2">
                <Plus className="w-4 h-4" />
                Add User
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, idx) => (
            <StatCard key={idx} {...stat} />
          ))}
        </div>

        {/* Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* User Management */}
          <div className="lg:col-span-2">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">User Management</h2>
            <div className="bg-white dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700 overflow-hidden">
              <div className="p-4 border-b border-gray-200 dark:border-slate-700">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search users..."
                    value={searchUser}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchUser(e.target.value)}
                    className="pl-10 w-full border border-gray-300 rounded-lg py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 dark:bg-slate-700 border-b border-gray-200 dark:border-slate-600">
                    <tr>
                      <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Name</th>
                      <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Role</th>
                      <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Status</th>
                      <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Joined</th>
                      <th className="px-6 py-3 text-right text-sm font-semibold text-gray-900 dark:text-white">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 dark:divide-slate-700">
                    {users.map((user) => (
                      <tr key={user.id} className="hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors">
                        <td className="px-6 py-4">
                          <div>
                            <p className="font-medium text-gray-900 dark:text-white">{user.name}</p>
                            <p className="text-sm text-gray-600 dark:text-gray-300">{user.email}</p>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm">
                          <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${ 
                            user.role === 'Admin'
                              ? 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
                              : user.role === 'Accountant'
                                ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                                : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
                          }`}>
                            {user.role}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm">
                          <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${user.status === 'Active' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'}`}>
                            {user.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600 dark:text-gray-300">{user.joined}</td>
                        <td className="px-6 py-4 text-right">
                          <button className="text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium">
                            Edit
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Pending Approvals */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Pending Approvals</h2>
            <div className="bg-white dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700 space-y-4 p-6">
              {pendingApprovals.map((approval) => (
                <div key={approval.id} className="pb-4 border-b border-gray-200 dark:border-slate-600 last:border-0 last:pb-0">
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div className="flex-1">
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200 mb-2">{approval.type}</span>
                      <h4 className="font-medium text-gray-900 dark:text-white text-sm">{approval.title}</h4>
                      <p className="text-xs text-gray-600 dark:text-gray-300 mt-1">{approval.requester}</p>
                    </div>
                  </div>
                  <div className="flex items-center justify-between mt-3">
                    <span className="text-xs text-gray-500 dark:text-gray-400">{approval.date}</span>
                    <div className="flex gap-2">
                      <button className="border border-gray-300 dark:border-slate-600 text-gray-700 dark:text-gray-300 font-medium py-1 px-3 rounded text-xs hover:bg-gray-50 dark:hover:bg-slate-700">
                        Reject
                      </button>
                      <button className="text-xs bg-green-600 hover:bg-green-700 text-white font-medium py-1 px-3 rounded">
                        Approve
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* System Logs */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">System Activity Logs</h2>
          <div className="bg-white dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-slate-700 border-b border-gray-200 dark:border-slate-600">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Action</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">User</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Timestamp</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-slate-700">
                  {systemLogs.map((log) => (
                    <tr key={log.id} className="hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors">
                      <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white">{log.action}</td>
                      <td className="px-6 py-4 text-sm text-gray-600 dark:text-gray-300">{log.user}</td>
                      <td className="px-6 py-4 text-sm text-gray-600 dark:text-gray-300">{log.timestamp}</td>
                      <td className="px-6 py-4 text-sm">
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">{log.status}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
