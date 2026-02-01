'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { BookOpen, DollarSign, Shield, ArrowRight } from 'lucide-react';

const roles = [
  {
    id: 'student',
    title: 'Student Dashboard',
    description: 'Track your projects, submissions, and academic progress',
    icon: BookOpen,
    color: 'from-pink-500 to-rose-500',
    lightColor: 'from-pink-50 to-rose-50',
    href: '/student',
    features: ['View Projects', 'Submit Assignments', 'Track Progress', 'Messages'],
  },
  {
    id: 'accountant',
    title: 'Finance Dashboard',
    description: 'Manage invoices, expenses, and financial reports',
    icon: DollarSign,
    color: 'from-blue-500 to-cyan-500',
    lightColor: 'from-blue-50 to-cyan-50',
    href: '/accountant',
    features: ['Invoices', 'Expenses', 'Budgets', 'Reports'],
  },
  {
    id: 'admin',
    title: 'Admin Dashboard',
    description: 'Oversee system, manage users, and approve requests',
    icon: Shield,
    color: 'from-green-500 to-emerald-500',
    lightColor: 'from-green-50 to-emerald-50',
    href: '/admin',
    features: ['User Management', 'Approvals', 'System Logs', 'Settings'],
  },
];

export default function Home() {
  const [hoveredRole, setHoveredRole] = useState<string | null>(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500 opacity-5 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500 opacity-5 rounded-full blur-3xl"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-4">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="flex justify-center mb-8">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-500 rounded-2xl flex items-center justify-center">
              <span className="text-white text-2xl font-bold">DPG</span>
            </div>
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4">
            DPG Project Management System
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl">
            Select your role to access the comprehensive project management platform
          </p>
        </div>

        {/* Role Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mb-16">
          {roles.map((role) => {
            const Icon = role.icon;
            const isHovered = hoveredRole === role.id;

            return (
              <Link key={role.id} href={role.href}>
                <Card
                  onMouseEnter={() => setHoveredRole(role.id)}
                  onMouseLeave={() => setHoveredRole(null)}
                  className={`h-full p-8 cursor-pointer transition-all duration-300 border-0 bg-gradient-to-br ${role.lightColor} ${
                    isHovered ? 'transform scale-105 shadow-2xl' : 'shadow-lg'
                  }`}
                >
                  {/* Icon */}
                  <div className={`mb-6 inline-flex p-4 rounded-xl bg-gradient-to-br ${role.color}`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>

                  {/* Title */}
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{role.title}</h3>

                  {/* Description */}
                  <p className="text-gray-700 mb-6 line-clamp-2">{role.description}</p>

                  {/* Features */}
                  <div className="mb-8 space-y-2">
                    {role.features.map((feature, idx) => (
                      <div key={idx} className="flex items-center gap-2 text-sm text-gray-700">
                        <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${role.color}`}></div>
                        {feature}
                      </div>
                    ))}
                  </div>

                  {/* CTA */}
                  <div className="flex items-center gap-2 text-base font-semibold text-gray-900">
                    Access Dashboard
                    <ArrowRight
                      className={`w-5 h-5 transition-transform duration-300 ${
                        isHovered ? 'translate-x-2' : ''
                      }`}
                    />
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>

        {/* Footer */}
        <div className="text-center text-gray-500 text-sm">
          <p>© 2026 DPG Project Management System by NexyugTech. All rights reserved.</p>
        </div>
      </div>
    </div>
  );
}
