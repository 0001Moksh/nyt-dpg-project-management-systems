'use client';

import React from 'react';
import { Card } from '../ui/card';
import { ArrowUp, ArrowDown } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  variant?: 'default' | 'success' | 'warning' | 'danger';
  onClick?: () => void;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  trend,
  variant = 'default',
  onClick,
}) => {
  const variantStyles = {
    default: 'bg-gradient-to-br from-blue-50 to-blue-100/50 border-blue-200',
    success: 'bg-gradient-to-br from-green-50 to-green-100/50 border-green-200',
    warning: 'bg-gradient-to-br from-yellow-50 to-yellow-100/50 border-yellow-200',
    danger: 'bg-gradient-to-br from-red-50 to-red-100/50 border-red-200',
  };

  const textVariant = {
    default: 'text-blue-600',
    success: 'text-green-600',
    warning: 'text-yellow-600',
    danger: 'text-red-600',
  };

  return (
    <Card
      onClick={onClick}
      className={`${variantStyles[variant]} p-6 cursor-pointer hover:shadow-lg transition-all duration-300 border-2`}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-2">{title}</p>
          <div className="flex items-baseline gap-2">
            <h3 className="text-3xl font-bold text-gray-900">{value}</h3>
            {trend && (
              <div className={`flex items-center gap-1 text-sm font-semibold ${trend.isPositive ? 'text-green-600' : 'text-red-600'}`}>
                {trend.isPositive ? <ArrowUp className="w-4 h-4" /> : <ArrowDown className="w-4 h-4" />}
                {trend.value}%
              </div>
            )}
          </div>
          {subtitle && <p className="text-xs text-gray-500 mt-2">{subtitle}</p>}
        </div>
        {icon && <div className={`${textVariant[variant]} opacity-50`}>{icon}</div>}
      </div>
    </Card>
  );
};
