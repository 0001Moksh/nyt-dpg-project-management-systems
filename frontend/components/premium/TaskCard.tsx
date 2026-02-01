'use client';

import React from 'react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { AlertCircle, CheckCircle, Clock, User } from 'lucide-react';

interface TaskCardProps {
  id: string;
  title: string;
  description?: string;
  assignee: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  dueDate: string;
  status: 'todo' | 'in-progress' | 'review' | 'done';
  onClick?: () => void;
  onStatusChange?: (newStatus: string) => void;
}

export const TaskCard: React.FC<TaskCardProps> = ({
  id,
  title,
  description,
  assignee,
  priority,
  dueDate,
  status,
  onClick,
  onStatusChange,
}) => {
  const priorityColors = {
    low: 'bg-blue-100 text-blue-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    critical: 'bg-red-100 text-red-800',
  };

  const statusIcons = {
    todo: <Clock className="w-4 h-4" />,
    'in-progress': <Clock className="w-4 h-4" />,
    review: <AlertCircle className="w-4 h-4" />,
    done: <CheckCircle className="w-4 h-4" />,
  };

  return (
    <Card
      onClick={onClick}
      className="p-5 hover:shadow-lg transition-all duration-300 cursor-pointer border border-gray-200 bg-white"
    >
      <div className="space-y-3">
        {/* Title & Priority */}
        <div className="flex items-start justify-between gap-3">
          <h4 className="font-semibold text-gray-900 flex-1">{title}</h4>
          <Badge className={priorityColors[priority]}>{priority}</Badge>
        </div>

        {/* Description */}
        {description && <p className="text-sm text-gray-600 line-clamp-2">{description}</p>}

        {/* Meta Info */}
        <div className="flex items-center justify-between text-sm text-gray-600 pt-2 border-t border-gray-100">
          <div className="flex items-center gap-2">
            <User className="w-4 h-4" />
            {assignee}
          </div>
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4" />
            {dueDate}
          </div>
        </div>

        {/* Status */}
        <div className="flex items-center justify-between pt-2">
          <div className="flex items-center gap-2 text-sm">
            {statusIcons[status as keyof typeof statusIcons]}
            <span className="capitalize font-medium text-gray-700">{status.replace('-', ' ')}</span>
          </div>
        </div>
      </div>
    </Card>
  );
};
