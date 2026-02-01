'use client';

import React from 'react';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';
import { Calendar, Users, CheckCircle } from 'lucide-react';

interface ProjectCardProps {
  id: string;
  title: string;
  description: string;
  status: 'active' | 'completed' | 'pending' | 'on-hold' | 'in-progress';
  progress: number;
  dueDate: string;
  team: Array<{ name: string; avatar: string }>;
  members: number;
  onClick?: () => void;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({
  id,
  title,
  description,
  status,
  progress,
  dueDate,
  team,
  members,
  onClick,
}) => {
  const statusColors: Record<ProjectCardProps['status'], string> = {
    active: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    pending: 'bg-yellow-100 text-yellow-800',
    'on-hold': 'bg-gray-100 text-gray-800',
    'in-progress': 'bg-purple-100 text-purple-800',
  };

  return (
    <Card
      onClick={onClick}
      className="p-6 hover:shadow-xl transition-all duration-300 cursor-pointer border border-gray-200 bg-white"
    >
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-start justify-between">
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          <Badge className={statusColors[status]}>{status}</Badge>
        </div>

        {/* Description */}
        <p className="text-sm text-gray-600 line-clamp-2">{description}</p>

        {/* Progress Bar */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Progress</span>
            <span className="font-semibold text-gray-900">{progress}%</span>
          </div>
          <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Footer Info */}
        <div className="flex items-center justify-between pt-2 border-t border-gray-100">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Calendar className="w-4 h-4" />
            {dueDate}
          </div>
          <div className="flex items-center gap-2">
            <div className="flex -space-x-2">
              {team.slice(0, 2).map((member, idx) => (
                <div
                  key={idx}
                  className="w-6 h-6 rounded-full bg-gray-300 border-2 border-white flex items-center justify-center text-xs font-bold"
                  title={member.name}
                >
                  {member.name.charAt(0)}
                </div>
              ))}
            </div>
            {members > 2 && <span className="text-xs text-gray-600">+{members - 2}</span>}
          </div>
        </div>
      </div>
    </Card>
  );
};
