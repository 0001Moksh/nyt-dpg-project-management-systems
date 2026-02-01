'use client';

import React, { useState } from 'react';
import { StatCard } from '@/components/premium/StatCard';
import { DollarSign, TrendingUp, TrendingDown, FileText, Filter, Plus, Download } from 'lucide-react';

export default function AccountantDashboard() {
  const [dateRange, setDateRange] = useState('month');

  const stats = [
    {
      title: 'Total Revenue',
      value: '$125,430',
      subtitle: 'This Month',
      icon: <DollarSign className="w-6 h-6" />,
      trend: { value: 12.5, isPositive: true },
      variant: 'success' as const,
    },
    {
      title: 'Total Expenses',
      value: '$45,280',
      subtitle: 'This Month',
      icon: <TrendingDown className="w-6 h-6" />,
      trend: { value: 3.2, isPositive: false },
      variant: 'warning' as const,
    },
    {
      title: 'Net Profit',
      value: '$80,150',
      subtitle: 'This Month',
      icon: <TrendingUp className="w-6 h-6" />,
      trend: { value: 18.3, isPositive: true },
      variant: 'success' as const,
    },
    {
      title: 'Pending Invoices',
      value: '12',
      subtitle: 'Amount: $35,600',
      icon: <FileText className="w-6 h-6" />,
      trend: { value: 5, isPositive: false },
      variant: 'danger' as const,
    },
  ];

  const transactions = [
    { id: '1', type: 'Invoice', description: 'Project ABC - Monthly Fee', amount: '$5,000', date: 'Feb 1', status: 'Paid' },
    { id: '2', type: 'Expense', description: 'Software Licenses', amount: '-$1,200', date: 'Feb 2', status: 'Approved' },
    { id: '3', type: 'Invoice', description: 'Project XYZ - Milestone 1', amount: '$8,500', date: 'Feb 3', status: 'Pending' },
    { id: '4', type: 'Expense', description: 'Office Supplies', amount: '-$450', date: 'Feb 4', status: 'Pending' },
    { id: '5', type: 'Invoice', description: 'Maintenance Service', amount: '$2,300', date: 'Feb 5', status: 'Paid' },
  ];

  const budgetCategories = [
    { category: 'Salaries', allocated: '$50,000', spent: '$48,500', percentage: 97 },
    { category: 'Operations', allocated: '$15,000', spent: '$12,300', percentage: 82 },
    { category: 'Marketing', allocated: '$10,000', spent: '$8,750', percentage: 87 },
    { category: 'Technology', allocated: '$8,000', spent: '$5,600', percentage: 70 },
    { category: 'Miscellaneous', allocated: '$5,000', spent: '$3,200', percentage: 64 },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900">Finance Dashboard</h1>
              <p className="text-gray-600 mt-2">Monitor revenue, expenses, and budgets</p>
            </div>
            <div className="flex gap-3">
              <button className="border border-gray-300 text-gray-700 font-medium py-2 px-4 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                <Download className="w-4 h-4" />
                Export
              </button>
              <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg flex items-center gap-2">
                <Plus className="w-4 h-4" />
                New Invoice
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

        {/* Filters */}
        <div className="flex gap-4 mb-8">
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <option value="week">This Week</option>
            <option value="month">This Month</option>
            <option value="quarter">This Quarter</option>
            <option value="year">This Year</option>
          </select>
          <input type="search" placeholder="Search transactions..." className="w-64 border border-gray-300 rounded-lg py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        {/* Transactions */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Transactions</h2>
          <div className="bg-white dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-slate-700 border-b border-gray-200 dark:border-slate-600">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Type</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Description</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Amount</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Date</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Status</th>
                    <th className="px-6 py-3 text-right text-sm font-semibold text-gray-900 dark:text-white">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-slate-700">
                  {transactions.map((tx) => (
                    <tr key={tx.id} className="hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors">
                      <td className="px-6 py-4 text-sm font-medium">
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${ tx.type === 'Invoice' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'}`}>
                          {tx.type}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">{tx.description}</td>
                      <td className="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white">{tx.amount}</td>
                      <td className="px-6 py-4 text-sm text-gray-600 dark:text-gray-300">{tx.date}</td>
                      <td className="px-6 py-4 text-sm">
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                          tx.status === 'Paid'
                            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                            : tx.status === 'Approved'
                              ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                              : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                        }`}>
                          {tx.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button className="text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium">
                          Details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Budget Overview */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Budget Overview</h2>
          <div className="bg-white dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700 p-6">
            <div className="space-y-6">
              {budgetCategories.map((budget, idx) => (
                <div key={idx} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-semibold text-gray-900">{budget.category}</h4>
                      <p className="text-sm text-gray-600">
                        {budget.spent} of {budget.allocated}
                      </p>
                    </div>
                    <span className="text-sm font-semibold text-gray-900">{budget.percentage}%</span>
                  </div>
                  <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full"
                      style={{ width: `${budget.percentage}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
