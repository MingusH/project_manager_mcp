import { ReactNode } from 'react';
import { LayoutDashboard, Wifi, WifiOff, AlertCircle } from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
  connected: boolean;
  lastUpdate: string | null;
  error: string | null;
}

export function Layout({ children, connected, lastUpdate, error }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <LayoutDashboard className="w-8 h-8 text-primary-600" />
              <h1 className="text-2xl font-bold text-gray-900">
                Project Manager Dashboard
              </h1>
            </div>
            
            <div className="flex items-center gap-4">
              {/* Connection Status */}
              <div className="flex items-center gap-2">
                {connected ? (
                  <>
                    <Wifi className="w-5 h-5 text-green-500" />
                    <span className="text-sm text-green-600 font-medium">Connected</span>
                  </>
                ) : (
                  <>
                    <WifiOff className="w-5 h-5 text-red-500" />
                    <span className="text-sm text-red-600 font-medium">Disconnected</span>
                  </>
                )}
              </div>
              
              {/* Last Update */}
              {lastUpdate && (
                <span className="text-sm text-gray-500">
                  Last update: {new Date(lastUpdate).toLocaleTimeString()}
                </span>
              )}
              
              {/* Error */}
              {error && (
                <div className="flex items-center gap-2 text-red-600">
                  <AlertCircle className="w-5 h-5" />
                  <span className="text-sm">{error}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-sm text-gray-500">
            Project Manager MCP Server Dashboard • Real-time updates via WebSocket
          </p>
        </div>
      </footer>
    </div>
  );
}
