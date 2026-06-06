import { useEffect, useRef, useState, useCallback } from 'react';
import type { WebSocketMessage, Metrics, Worker, Project } from '../types';

interface UseWebSocketReturn {
  connected: boolean;
  metrics: Metrics | null;
  workers: Worker[];
  projects: Project[];
  lastUpdate: string | null;
  error: string | null;
  refresh: () => void;
}

export function useWebSocket(url: string): UseWebSocketReturn {
  const [connected, setConnected] = useState(false);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [workers, setWorkers] = useState<Worker[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [lastUpdate, setLastUpdate] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const ws = useRef<WebSocket | null>(null);
  const reconnectTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);

  const connect = useCallback(() => {
    try {
      ws.current = new WebSocket(url);

      ws.current.onopen = () => {
        console.log('WebSocket connected');
        setConnected(true);
        setError(null);
        
        // Subscribe to all channels
        ws.current?.send(JSON.stringify({ action: 'subscribe', channel: 'overview' }));
        ws.current?.send(JSON.stringify({ action: 'subscribe', channel: 'workers' }));
        ws.current?.send(JSON.stringify({ action: 'subscribe', channel: 'projects' }));
      };

      ws.current.onmessage = (event: MessageEvent) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          setLastUpdate(message.timestamp);

          switch (message.type) {
            case 'metrics':
              setMetrics(message.data as Metrics);
              break;
            case 'workers':
              setWorkers(message.data as Worker[]);
              break;
            case 'projects':
              setProjects(message.data as Project[]);
              break;
            case 'heartbeat':
              // Heartbeat received, connection is alive
              break;
            // MCP notification types - trigger refresh
            case 'project_created':
            case 'project_updated':
            case 'project_deleted':
            case 'worker_created':
            case 'worker_updated':
            case 'worker_deleted':
            case 'worker_assigned':
            case 'worker_removed':
            case 'refresh':
              // Re-subscribe to all channels to get fresh data
              ws.current?.send(JSON.stringify({ action: 'subscribe', channel: 'overview' }));
              ws.current?.send(JSON.stringify({ action: 'subscribe', channel: 'workers' }));
              ws.current?.send(JSON.stringify({ action: 'subscribe', channel: 'projects' }));
              break;
            default:
              console.log('Unknown message type:', message.type);
          }
        } catch (err) {
          console.error('Failed to parse message:', err);
        }
      };

      ws.current.onclose = () => {
        console.log('WebSocket disconnected');
        setConnected(false);
        
        // Attempt reconnect after 3 seconds
        reconnectTimeout.current = setTimeout(() => {
          console.log('Attempting to reconnect...');
          connect();
        }, 3000);
      };

      ws.current.onerror = (err: Event) => {
        console.error('WebSocket error:', err);
        setError('Connection error');
      };
    } catch (err: unknown) {
      console.error('Failed to connect:', err);
      setError('Failed to establish connection');
    }
  }, [url]);

  const refresh = useCallback(() => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ action: 'subscribe', channel: 'overview' }));
      ws.current.send(JSON.stringify({ action: 'subscribe', channel: 'workers' }));
      ws.current.send(JSON.stringify({ action: 'subscribe', channel: 'projects' }));
    }
  }, []);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeout.current) {
        clearTimeout(reconnectTimeout.current);
      }
      ws.current?.close();
    };
  }, [connect]);

  return {
    connected,
    metrics,
    workers,
    projects,
    lastUpdate,
    error,
    refresh,
  };
}
