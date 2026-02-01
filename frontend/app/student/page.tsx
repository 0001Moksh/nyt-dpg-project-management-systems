'use client';

import React, { useState } from 'react';
import { StatCard } from '@/components/premium/StatCard';
import { ProjectCard } from '@/components/premium/ProjectCard';
import { TaskCard } from '@/components/premium/TaskCard';
import { BookOpen, FileText, CheckCircle, Clock, AlertCircle, Search, Plus } from 'lucide-react';

export default function StudentDashboard() {
  const [selectedProject, setSelectedProject] = useState<string | null>(null);

  const stats = [
    {
      title: 'Active Projects',
      value: '5',
      subtitle: 'In Progress',
      icon: <BookOpen className="w-6 h-6" />,
      trend: { value: 12, isPositive: true },
      variant: 'default' as const,
    },
    {
      title: 'Tasks Completed',
      value: '24',
      subtitle: 'This Month',
      icon: <CheckCircle className="w-6 h-6" />,
      trend: { value: 8, isPositive: true },
      variant: 'success' as const,
    },
    {
      title: 'Pending Submissions',
      value: '3',
      subtitle: 'Due Soon',
      icon: <Clock className="w-6 h-6" />,
      trend: { value: 5, isPositive: false },
      variant: 'warning' as const,
    },
    {
      title: 'Overdue Items',
      value: '1',
      subtitle: 'Needs Attention',
      icon: <AlertCircle className="w-6 h-6" />,
      trend: { value: 2, isPositive: false },
      variant: 'danger' as const,
    },
  ];

  const projects = [
    {
      id: '1',
      title: 'Web Development Project',
      description: 'Build a responsive e-commerce platform using Next.js and React',
      status: 'active' as const,
      progress: 65,
      dueDate: 'Mar 15, 2026',
      team: [
        { name: 'Alex', avatar: 'A' },
        { name: 'Bob', avatar: 'B' },
        { name: 'Carol', avatar: 'C' },
      ],
      members: 3,
    },
    {
      id: '2',
      title: 'Data Analytics Report',
      description: 'Analyze quarterly sales data and create visualizations',
      status: 'in-progress' as const,
      progress: 45,
      dueDate: 'Mar 20, 2026',
      team: [{ name: 'David', avatar: 'D' }, { name: 'Eve', avatar: 'E' }],
      members: 2,
    },
    {
      id: '3',
      title: 'Mobile App Design',
      description: 'UI/UX design for iOS and Android applications',
      status: 'pending' as const,
      progress: 20,
      dueDate: 'Apr 1, 2026',
      team: [{ name: 'Frank', avatar: 'F' }],
      members: 1,
    },
  ];

  const upcomingTasks = [
    {
      id: '1',
      title: 'Complete API Integration',
      description: 'Integrate with payment gateway',
      assignee: 'You',
      priority: 'high' as const,
      dueDate: 'Today',
      status: 'in-progress' as const,
    },
    {
      id: '2',
      title: 'Code Review',
      description: 'Review pull requests from team',
      assignee: 'Team Lead',
      priority: 'medium' as const,
      dueDate: 'Tomorrow',
      status: 'todo' as const,
    },
    {
      id: '3',
      title: 'Documentation Update',
      description: 'Update API documentation',
      assignee: 'You',
      priority: 'medium' as const,
      dueDate: 'Mar 10',
      status: 'review' as const,
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-gray-600 mt-2">Welcome back! Here's your project overview.</p>
            </div>
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg flex items-center gap-2">
              <Plus className="w-4 h-4" />
              New Project
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, idx) => (
            <StatCard
              key={idx}
              {...stat}
              onClick={() => {}}
            />
          ))}
        </div>

        {/* Projects Section */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Your Projects</h2>
            <button className="border border-gray-300 text-gray-700 font-medium py-2 px-4 rounded-lg hover:bg-gray-50">View All</button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <ProjectCard
                key={project.id}
                {...project}
                onClick={() => setSelectedProject(project.id)}
              />
            ))}
          </div>
        </div>

        {/* Tasks Section */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Upcoming Tasks</h2>
            <div className="relative w-64">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search tasks..."
                className="pl-10 w-full border border-gray-300 rounded-lg py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {upcomingTasks.map((task) => (
              <TaskCard key={task.id} {...task} />
            ))}
          </div>
        </div>

        {/* Submissions */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Submissions</h2>
          <div className="bg-white dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-slate-700 border-b border-gray-200 dark:border-slate-600">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">Title</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Project</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Status</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Submitted</th>
                    <th className="px-6 py-3 text-right text-sm font-semibold text-gray-900">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-slate-700">
                  {[
                    { title: 'Project Report', project: 'Web Dev', status: 'Approved', submitted: '3 days ago' },
                    { title: 'Code Submission', project: 'Web Dev', status: 'Under Review', submitted: '1 day ago' },
                    { title: 'Documentation', project: 'Data Analytics', status: 'Pending', submitted: 'Today' },
                  ].map((submission, idx) => (
                    <tr key={idx} className="hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors">
                      <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white">{submission.title}</td>
                      <td className="px-6 py-4 text-sm text-gray-600 dark:text-gray-300">{submission.project}</td>
                      <td className="px-6 py-4 text-sm">
                        <span
                          className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                            submission.status === 'Approved'
                              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                              : submission.status === 'Under Review'
                                ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                                : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                          }`}
                        >
                          {submission.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600 dark:text-gray-300">{submission.submitted}</td>
                      <td className="px-6 py-4 text-right">
                        <button className="text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium">
                          View
                        </button>
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
