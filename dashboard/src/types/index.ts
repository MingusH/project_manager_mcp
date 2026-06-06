export interface Worker {
  id: string;
  name: string;
  department: string;
  role: string;
  years_experience: number;
  availability: boolean;
  current_workload: number;
  created_at?: string;
  updated_at?: string;
  resume?: string;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  timeline_start?: string;
  timeline_end?: string;
  budget?: number;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'planned' | 'in_progress' | 'completed' | 'on_hold' | 'cancelled';
  created_at?: string;
  updated_at?: string;
  worker_count: number;
  workers?: Array<{
    id: string;
    role_in_project?: string;
  }>;
}

export interface Metrics {
  total_workers: number;
  total_projects: number;
  active_projects: number;
  completed_projects: number;
  available_workers: number;
  department_breakdown: Record<string, number>;
}

export interface Department {
  name: string;
  worker_count: number;
}

export interface WebSocketMessage {
  type: string;
  timestamp: string;
  data: unknown;
}
