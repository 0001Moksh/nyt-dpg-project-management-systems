'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter, usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  FileText,
  Users,
  Settings,
  LogOut,
  Menu,
  X,
  BookOpen,
  DollarSign,
  Shield,
  ChevronDown,
} from 'lucide-react';
import { Button } from '../ui/button';

interface NavItem {
  label: string;
  href: string;
  icon: React.ReactNode;
  badge?: string;
}

interface RoleNavConfig {
  [key: string]: {
    title: string;
    navItems: NavItem[];
    color: string;
  };
}

const roleNavConfig: RoleNavConfig = {
  student: {
    title: 'Student',
    color: 'from-pink-500 to-rose-500',
    navItems: [
      { label: 'Dashboard', href: '/student', icon: <LayoutDashboard className="w-5 h-5" /> },
      { label: 'Projects', href: '/student/projects', icon: <BookOpen className="w-5 h-5" /> },
      { label: 'Submissions', href: '/student/submissions', icon: <FileText className="w-5 h-5" /> },
      { label: 'Progress', href: '/student/progress', icon: <LayoutDashboard className="w-5 h-5" /> },
      { label: 'Messages', href: '/student/messages', icon: <Users className="w-5 h-5" />, badge: '3' },
    ],
  },
  accountant: {
    title: 'Accountant',
    color: 'from-blue-500 to-cyan-500',
    navItems: [
      { label: 'Finance Dashboard', href: '/accountant', icon: <DollarSign className="w-5 h-5" /> },
      { label: 'Invoices', href: '/accountant/invoices', icon: <FileText className="w-5 h-5" /> },
      { label: 'Expenses', href: '/accountant/expenses', icon: <DollarSign className="w-5 h-5" /> },
      { label: 'Reports', href: '/accountant/reports', icon: <LayoutDashboard className="w-5 h-5" /> },
      { label: 'Budgets', href: '/accountant/budgets', icon: <Users className="w-5 h-5" /> },
    ],
  },
  admin: {
    title: 'Admin',
    color: 'from-green-500 to-emerald-500',
    navItems: [
      { label: 'Dashboard', href: '/admin', icon: <Shield className="w-5 h-5" /> },
      { label: 'Users', href: '/admin/users', icon: <Users className="w-5 h-5" /> },
      { label: 'Projects', href: '/admin/projects', icon: <BookOpen className="w-5 h-5" /> },
      { label: 'Approvals', href: '/admin/approvals', icon: <FileText className="w-5 h-5" />, badge: '7' },
      { label: 'Settings', href: '/admin/settings', icon: <Settings className="w-5 h-5" /> },
    ],
  },
};

interface RoleNavigationProps {
  role?: 'student' | 'accountant' | 'admin';
}

export const RoleNavigation: React.FC<RoleNavigationProps> = ({ role = 'student' }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const pathname = usePathname();
  const router = useRouter();

  const config = roleNavConfig[role];
  if (!config) return null;

  const handleLogout = () => {
    // TODO: Implement logout logic
    router.push('/auth/login');
  };

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className={`hidden lg:fixed lg:inset-y-0 lg:left-0 lg:w-64 lg:bg-white lg:border-r lg:border-gray-200 lg:flex lg:flex-col`}>
        {/* Logo */}
        <div className="flex items-center gap-2 px-6 py-6 border-b border-gray-200">
          <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${config.color} flex items-center justify-center text-white font-bold`}>
            DPG
          </div>
          <div>
            <h1 className="font-bold text-gray-900">DPG PMS</h1>
            <p className="text-xs text-gray-600">{config.title}</p>
          </div>
        </div>

        {/* Nav Items */}
        <nav className="flex-1 px-3 py-6 space-y-2">
          {config.navItems.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive
                    ? `bg-gradient-to-r ${config.color} text-white`
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                {item.icon}
                <span className="font-medium">{item.label}</span>
                {item.badge && (
                  <span className="ml-auto bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">
                    {item.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>

        {/* Profile & Logout */}
        <div className="border-t border-gray-200 p-4">
          <div className="relative">
            <button
              onClick={() => setIsProfileOpen(!isProfileOpen)}
              className="w-full flex items-center gap-3 p-3 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-gray-300 to-gray-400 flex items-center justify-center text-white font-bold">
                U
              </div>
              <div className="text-left flex-1">
                <p className="font-semibold text-sm text-gray-900">User Name</p>
                <p className="text-xs text-gray-600">user@college.edu</p>
              </div>
              <ChevronDown className="w-4 h-4 text-gray-600" />
            </button>

            {isProfileOpen && (
              <div className="absolute bottom-full left-0 right-0 mb-2 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                <Link
                  href="/profile"
                  className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-t-lg"
                >
                  Profile Settings
                </Link>
                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-b-lg flex items-center gap-2"
                >
                  <LogOut className="w-4 h-4" />
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </aside>

      {/* Mobile Top Bar */}
      <div className="lg:hidden sticky top-0 z-40 bg-white border-b border-gray-200">
        <div className="flex items-center justify-between px-4 py-4">
          <div className="flex items-center gap-2">
            <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${config.color} flex items-center justify-center text-white font-bold`}>
              DPG
            </div>
            <div>
              <h1 className="font-bold text-gray-900">DPG PMS</h1>
              <p className="text-xs text-gray-600">{config.title}</p>
            </div>
          </div>
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="border-t border-gray-200 bg-white">
            <nav className="px-3 py-4 space-y-2">
              {config.navItems.map((item) => {
                const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                      isActive
                        ? `bg-gradient-to-r ${config.color} text-white`
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    {item.icon}
                    <span className="font-medium">{item.label}</span>
                    {item.badge && (
                      <span className="ml-auto bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">
                        {item.badge}
                      </span>
                    )}
                  </Link>
                );
              })}
            </nav>
            <div className="border-t border-gray-200 p-4">
              <Button
                onClick={handleLogout}
                variant="ghost"
                className="w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Main Content Wrapper - Add padding for sidebar */}
      <div className="lg:ml-64" />
    </>
  );
};
