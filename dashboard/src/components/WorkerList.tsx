import { useState, useMemo } from 'react';
import type { Worker } from '../types';
import { Users, Search, Briefcase, Clock, CheckCircle, XCircle } from 'lucide-react';

interface WorkerListProps {
  workers: Worker[];
}

export function WorkerList({ workers }: WorkerListProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterDept, setFilterDept] = useState('');
  const [filterAvailability, setFilterAvailability] = useState<boolean | null>(null);

  const departments = useMemo(() => {
    const depts = new Set(workers.map(w => w.department));
    return Array.from(depts).sort();
  }, [workers]);

  const filteredWorkers = useMemo(() => {
    return workers.filter(worker => {
      const matchesSearch = worker.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          worker.role.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesDept = !filterDept || worker.department === filterDept;
      const matchesAvailability = filterAvailability === null || worker.availability === filterAvailability;
      
      return matchesSearch && matchesDept && matchesAvailability;
    });
  }, [workers, searchTerm, filterDept, filterAvailability]);

  return (
    <div className="bg-white rounded-lg shadow-md">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center gap-2 mb-4">
          <Users className="w-6 h-6 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-800">Workers</h2>
          <span className="ml-2 px-2 py-1 bg-gray-100 text-gray-600 text-sm rounded-full">
            {filteredWorkers.length} of {workers.length}
          </span>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div className="relative flex-1 min-w-[200px]">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search by name or role..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
          
          <select
            value={filterDept}
            onChange={(e) => setFilterDept(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All Departments</option>
            {departments.map(dept => (
              <option key={dept} value={dept}>{dept}</option>
            ))}
          </select>

          <select
            value={filterAvailability === null ? '' : filterAvailability.toString()}
            onChange={(e) => {
              const val = e.target.value;
              setFilterAvailability(val === '' ? null : val === 'true');
            }}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All Availability</option>
            <option value="true">Available</option>
            <option value="false">Unavailable</option>
          </select>
        </div>
      </div>

      {/* Worker Grid */}
      <div className="p-6">
        {filteredWorkers.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No workers found matching your filters.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredWorkers.map(worker => (
              <WorkerCard key={worker.id} worker={worker} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function WorkerCard({ worker }: { worker: Worker }) {
  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-semibold text-gray-900">{worker.name}</h3>
          <p className="text-sm text-gray-500">{worker.department}</p>
        </div>
        {worker.availability ? (
          <CheckCircle className="w-5 h-5 text-green-500" />
        ) : (
          <XCircle className="w-5 h-5 text-red-500" />
        )}
      </div>

      <div className="space-y-2">
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <Briefcase className="w-4 h-4" />
          <span>{worker.role}</span>
        </div>
        
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <Clock className="w-4 h-4" />
          <span>{worker.years_experience} years experience</span>
        </div>

        {/* Workload Bar */}
        <div className="mt-3">
          <div className="flex justify-between text-xs text-gray-500 mb-1">
            <span>Workload</span>
            <span>{worker.current_workload}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full ${
                worker.current_workload > 80 ? 'bg-red-500' :
                worker.current_workload > 50 ? 'bg-yellow-500' :
                'bg-green-500'
              }`}
              style={{ width: `${worker.current_workload}%` }}
            />
          </div>
        </div>

        {/* Status Badge */}
        <div className="mt-3">
          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
            worker.availability 
              ? 'bg-green-100 text-green-800' 
              : 'bg-red-100 text-red-800'
          }`}>
            {worker.availability ? 'Available' : 'Unavailable'}
          </span>
        </div>
      </div>
    </div>
  );
}
