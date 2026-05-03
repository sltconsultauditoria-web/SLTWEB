import { useCallback, useEffect, useSyncExternalStore } from 'react';
import { api } from '@/context/AuthContext';
import { countBadgeAlertas, normalizeAlertas } from '@/lib/alertas';

const DEFAULT_STATE = {
  alertas: [],
  unreadCount: 0,
  connected: false,
  loading: true,
  lastError: null,
  lastNotification: null,
  lastUpdatedAt: null,
};

let state = DEFAULT_STATE;
const listeners = new Set();
let started = false;
let socket = null;
let pollTimer = null;
let reconnectTimer = null;
let visibilityHandler = null;
let reconnectDelay = 1000;

const emit = () => {
  for (const listener of listeners) {
    listener();
  }
};

const setState = (updater) => {
  const nextState = typeof updater === 'function' ? updater(state) : { ...state, ...updater };
  const alertas = normalizeAlertas(nextState.alertas || []);
  state = {
    ...DEFAULT_STATE,
    ...nextState,
    alertas,
    unreadCount: countBadgeAlertas(alertas),
  };
  emit();
};

const getSnapshot = () => state;

const cleanupTimers = () => {
  if (pollTimer) {
    window.clearInterval(pollTimer);
    pollTimer = null;
  }
  if (reconnectTimer) {
    window.clearTimeout(reconnectTimer);
    reconnectTimer = null;
  }
  if (visibilityHandler) {
    document.removeEventListener('visibilitychange', visibilityHandler);
    visibilityHandler = null;
  }
};

const cleanupSocket = () => {
  if (socket) {
    try {
      socket.onopen = null;
      socket.onmessage = null;
      socket.onerror = null;
      socket.onclose = null;
      socket.close();
    } catch (error) {
      // ignore cleanup errors
    }
    socket = null;
  }
};

const resetConnectionState = () => {
  cleanupTimers();
  cleanupSocket();
  started = false;
  reconnectDelay = 1000;
  setState((current) => ({
    ...current,
    connected: false,
  }));
};

const refreshAlertas = async () => {
  try {
    const response = await api.get('/alertas');
    const payload = response.data;
    const items = Array.isArray(payload)
      ? payload
      : Array.isArray(payload?.data)
        ? payload.data
        : Array.isArray(payload?.alertas)
          ? payload.alertas
          : [];

    setState((current) => ({
      ...current,
      alertas: items,
      loading: false,
      lastError: null,
      lastUpdatedAt: new Date().toISOString(),
    }));
    return normalizeAlertas(items);
  } catch (error) {
    setState((current) => ({
      ...current,
      loading: false,
      lastError: error?.message || 'Erro ao carregar alertas',
    }));
    return state.alertas;
  }
};

const getWebSocketUrl = () => {
  if (typeof window === 'undefined') return null;
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${protocol}//${window.location.host}/ws/notificacoes`;
};

const scheduleReconnect = () => {
  if (typeof window === 'undefined' || reconnectTimer) return;
  reconnectTimer = window.setTimeout(() => {
    reconnectTimer = null;
    connectWebSocket();
  }, reconnectDelay);
  reconnectDelay = Math.min(reconnectDelay * 2, 30000);
};

const connectWebSocket = () => {
  if (typeof window === 'undefined') return;
  if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING)) {
    return;
  }

  const url = getWebSocketUrl();
  if (!url) return;

  try {
    socket = new WebSocket(url);

    socket.onopen = () => {
      reconnectDelay = 1000;
      setState((current) => ({
        ...current,
        connected: true,
        lastError: null,
      }));
    };

    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload?.tipo === 'evento' || payload?.tipo === 'alerta') {
          setState((current) => ({
            ...current,
            lastNotification: payload,
          }));
          refreshAlertas();
        }
      } catch (error) {
        // ignore malformed messages
      }
    };

    socket.onerror = () => {
      setState((current) => ({
        ...current,
        connected: false,
      }));
    };

    socket.onclose = () => {
      setState((current) => ({
        ...current,
        connected: false,
      }));
      socket = null;
      scheduleReconnect();
    };
  } catch (error) {
    socket = null;
    scheduleReconnect();
  }
};

const ensureStarted = () => {
  if (started || typeof window === 'undefined') return;
  started = true;
  refreshAlertas();
  connectWebSocket();

  pollTimer = window.setInterval(() => {
    refreshAlertas();
  }, 30000);

  visibilityHandler = () => {
    if (document.visibilityState === 'visible') {
      refreshAlertas();
      if (!socket || socket.readyState === WebSocket.CLOSED) {
        connectWebSocket();
      }
    }
  };

  document.addEventListener('visibilitychange', visibilityHandler);
};

const subscribe = (listener) => {
  listeners.add(listener);
  ensureStarted();
  return () => {
    listeners.delete(listener);
    if (listeners.size === 0) {
      resetConnectionState();
    }
  };
};

const updateAlertas = (updater) => {
  setState((current) => {
    const nextAlertas = typeof updater === 'function' ? updater(current.alertas) : updater;
    return {
      ...current,
      alertas: nextAlertas,
      lastUpdatedAt: new Date().toISOString(),
    };
  });
};

const markAlertAsRead = async (id) => {
  updateAlertas((items) => items.map((alerta) => (alerta.id === id ? { ...alerta, lido: true } : alerta)));
  try {
    await api.put(`/alertas/${id}/lido`);
  } catch (error) {
    // keep local state optimistic
  }
};

const markAlertAsResolved = (id) => {
  updateAlertas((items) => items.map((alerta) => (alerta.id === id ? { ...alerta, resolvido: true, lido: true } : alerta)));
};

export const useNotifications = () => {
  const snapshot = useSyncExternalStore(subscribe, getSnapshot, getSnapshot);

  useEffect(() => {
    ensureStarted();
  }, []);

  const refresh = useCallback(async () => {
    await refreshAlertas();
  }, []);

  return {
    alertas: snapshot.alertas,
    unreadCount: snapshot.unreadCount,
    connected: snapshot.connected,
    loading: snapshot.loading,
    lastError: snapshot.lastError,
    lastNotification: snapshot.lastNotification,
    lastUpdatedAt: snapshot.lastUpdatedAt,
    refresh,
    markAlertAsRead,
    markAlertAsResolved,
  };
};

export default useNotifications;
