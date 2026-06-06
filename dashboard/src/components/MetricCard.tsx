import { ReactNode } from 'react';

interface MetricCardProps {
  title: string;
  value: number;
  icon: ReactNode;
  color: 'blue' | 'green' | 'purple' | 'amber';
  subtitle?: string;
}

const colorClasses = {
  blue: {
    bg: 'bg-blue-50',
    text: 'text-blue-600',
    border: 'border-blue-200',
  },
  green: {
    bg: 'bg-green-50',
    text: 'text-green-600',
    border: 'border-green-200',
  },
  purple: {
    bg: 'bg-purple-50',
    text: 'text-purple-600',
    border: 'border-purple-200',
  },
  amber: {
    bg: 'bg-amber-50',
    text: 'text-amber-600',
    border: 'border-amber-200',
  },
};

export function MetricCard({ title, value, icon, color, subtitle }: MetricCardProps) {
  const colors = colorClasses[color];

  return (
    <div className={`${colors.bg} border ${colors.border} rounded-lg p-6`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className={`text-3xl font-bold ${colors.text} mt-2`}>
            {value.toLocaleString()}
          </p>
          {subtitle && (
            <p className="text-sm text-gray-500 mt-1">{subtitle}</p>
          )}
        </div>
        <div className={`${colors.text}`}>
          {icon}
        </div>
      </div>
    </div>
  );
}
