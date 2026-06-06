import { useWebSocket } from './hooks/useWebSocket';
import { Layout } from './components/Layout';
import { MetricCard } from './components/MetricCard';
import { WorkerList } from './components/WorkerList';
import { ProjectList } from './components/ProjectList';
import { Users, FolderKanban, CheckCircle, AlertCircle } from 'lucide-react';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

function App() {
  const { connected, metrics, workers, projects, lastUpdate, error, refresh } = useWebSocket(WS_URL);

  return (
    <Layout connected={connected} lastUpdate={lastUpdate} error={error}>
      {/* Overview Section */}
      <section className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-800">Overview</h2>
          <button
            onClick={refresh}
            className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
          >
            Refresh Data
          </button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Total Workers"
            value={metrics?.total_workers ?? 0}
            icon={<Users className="w-6 h-6" />}
            color="blue"
          />
          <MetricCard
            title="Active Projects"
            value={metrics?.active_projects ?? 0}
            icon={<FolderKanban className="w-6 h-6" />}
            color="green"
            subtitle={`of ${metrics?.total_projects ?? 0} total`}
          />
          <MetricCard
            title="Completed Projects"
            value={metrics?.completed_projects ?? 0}
            icon={<CheckCircle className="w-6 h-6" />}
            color="purple"
          />
          <MetricCard
            title="Available Workers"
            value={metrics?.available_workers ?? 0}
            icon={<AlertCircle className="w-6 h-6" />}
            color="amber"
            subtitle={`of ${metrics?.total_workers ?? 0} total`}
          />
        </div>

        {/* Department Breakdown */}
        {metrics?.department_breakdown && Object.keys(metrics.department_breakdown).length > 0 && (
          <div className="mt-6 bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Department Breakdown</h3>
            <div className="flex flex-wrap gap-3">
              {Object.entries(metrics.department_breakdown).map(([dept, count]) => (
                <div
                  key={dept}
                  className="px-4 py-2 bg-gray-100 rounded-full text-sm font-medium text-gray-700"
                >
                  {dept}: {count}
                </div>
              ))}
            </div>
          </div>
        )}
      </section>

      {/* Workers Section */}
      <section className="mb-8">
        <WorkerList workers={workers} />
      </section>

      {/* Projects Section */}
      <section className="mb-8">
        <ProjectList projects={projects} />
      </section>
    </Layout>
  );
}

export default App;
