import { useState, useMemo } from 'react';
import type { Project } from '../types';
import { FolderKanban, Search, Calendar, DollarSign, Users, AlertCircle } from 'lucide-react';

interface ProjectListProps {
  projects: Project[];
}

const priorityColors = {
  low: 'bg-gray-100 text-gray-700',
  medium: 'bg-blue-100 text-blue-700',
  high: 'bg-orange-100 text-orange-700',
  critical: 'bg-red-100 text-red-700',
};

const statusColors = {
  planned: 'bg-gray-100 text-gray-700',
  in_progress: 'bg-blue-100 text-blue-700',
  completed: 'bg-green-100 text-green-700',
  on_hold: 'bg-yellow-100 text-yellow-700',
  cancelled: 'bg-red-100 text-red-700',
};

export function ProjectList({ projects }: ProjectListProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [filterPriority, setFilterPriority] = useState('');

  const statuses = ['planned', 'in_progress', 'completed', 'on_hold', 'cancelled'];
  const priorities = ['low', 'medium', 'high', 'critical'];

  const filteredProjects = useMemo(() => {
    return projects.filter(project => {
      const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          project.description.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = !filterStatus || project.status === filterStatus;
      const matchesPriority = !filterPriority || project.priority === filterPriority;
      
      return matchesSearch && matchesStatus && matchesPriority;
    });
  }, [projects, searchTerm, filterStatus, filterPriority]);

  const overdueProjects = useMemo(() => {
    const today = new Date().toISOString().split('T')[0];
    return projects.filter(p => 
      p.timeline_end && p.timeline_end < today && p.status !== 'completed'
    );
  }, [projects]);

  return (
    <div className="bg-white rounded-lg shadow-md">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center gap-2 mb-4">
          <FolderKanban className="w-6 h-6 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-800">Projects</h2>
          <span className="ml-2 px-2 py-1 bg-gray-100 text-gray-600 text-sm rounded-full">
            {filteredProjects.length} of {projects.length}
          </span>
          {overdueProjects.length > 0 && (
            <span className="ml-2 px-2 py-1 bg-red-100 text-red-600 text-sm rounded-full flex items-center gap-1">
              <AlertCircle className="w-4 h-4" />
              {overdueProjects.length} overdue
            </span>
          )}
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div className="relative flex-1 min-w-[200px]">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search projects..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
          
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All Statuses</option>
            {statuses.map(status => (
              <option key={status} value={status}>
                {status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </option>
            ))}
          </select>

          <select
            value={filterPriority}
            onChange={(e) => setFilterPriority(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All Priorities</option>
            {priorities.map(priority => (
              <option key={priority} value={priority}>
                {priority.charAt(0).toUpperCase() + priority.slice(1)}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Project Grid */}
      <div className="p-6">
        {filteredProjects.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No projects found matching your filters.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredProjects.map(project => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function ProjectCard({ project }: { project: Project }) {
  const isOverdue = project.timeline_end && 
    project.timeline_end < new Date().toISOString().split('T')[0] && 
    project.status !== 'completed';

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <h3 className="font-semibold text-gray-900 line-clamp-1">{project.name}</h3>
        {isOverdue && (
          <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
        )}
      </div>

      {/* Description */}
      <p className="text-sm text-gray-600 mb-3 line-clamp-2">{project.description}</p>

      {/* Badges */}
      <div className="flex flex-wrap gap-2 mb-3">
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${priorityColors[project.priority]}`}>
          {project.priority.charAt(0).toUpperCase() + project.priority.slice(1)}
        </span>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[project.status]}`}>
          {project.status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
        </span>
      </div>

      {/* Details */}
      <div className="space-y-2 text-sm">
        {project.timeline_start && (
          <div className="flex items-center gap-2 text-gray-600">
            <Calendar className="w-4 h-4" />
            <span>
              {new Date(project.timeline_start).toLocaleDateString()}
              {project.timeline_end && ` - ${new Date(project.timeline_end).toLocaleDateString()}`}
            </span>
            {isOverdue && <span className="text-red-600 font-medium">(Overdue)</span>}
          </div>
        )}

        {project.budget && (
          <div className="flex items-center gap-2 text-gray-600">
            <DollarSign className="w-4 h-4" />
            <span>${project.budget.toLocaleString()}</span>
          </div>
        )}

        <div className="flex items-center gap-2 text-gray-600">
          <Users className="w-4 h-4" />
          <span>{project.worker_count} workers assigned</span>
        </div>
      </div>

      {/* Worker Avatars */}
      {project.workers && project.workers.length > 0 && (
        <div className="mt-3 flex -space-x-2">
          {project.workers.slice(0, 5).map((worker, idx) => (
            <div
              key={worker.id}
              className="w-8 h-8 rounded-full bg-primary-500 text-white flex items-center justify-center text-xs font-medium border-2 border-white"
              style={{ zIndex: 5 - idx }}
            >
              {worker.id.charAt(0).toUpperCase()}
            </div>
          ))}
          {project.workers.length > 5 && (
            <div className="w-8 h-8 rounded-full bg-gray-300 text-gray-700 flex items-center justify-center text-xs font-medium border-2 border-white">
              +{project.workers.length - 5}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
