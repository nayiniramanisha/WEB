import { io } from 'socket.io-client'

const socketUrl = import.meta.env.VITE_SOCKET_URL || 'http://localhost:8000'
console.log('🔍 Socket connecting to:', socketUrl)

export const socket = io(socketUrl, {
  autoConnect: true,
  // Simplified configuration for better compatibility
  path: '/socket.io',
  // Connection settings
  timeout: 20000,
  forceNew: false,
  transports: ['polling', 'websocket'],
  upgrade: true,
  rememberUpgrade: false, // Don't remember upgrades to avoid conflicts
  // Timeout settings
  pingTimeout: 60000,
  pingInterval: 25000,
  // Reconnection settings
  reconnection: true,
  reconnectionAttempts: 10, // More attempts
  reconnectionDelay: 1000,
  reconnectionDelayMax: 10000, // Longer max delay
  // Additional stability settings
  randomizationFactor: 0.5,
  maxReconnectionAttempts: 10,
})

// Add connection event listeners for debugging
socket.on('connect', () => {
  console.log('🔍 Socket connected successfully!', socket.id)
})

socket.on('connect_error', (error) => {
  console.error('🔍 Socket connection error:', error)
})

socket.on('disconnect', (reason) => {
  console.log('🔍 Socket disconnected:', reason)
  // Auto-reconnect on disconnect
  if (reason === 'ping timeout' || reason === 'transport close') {
    console.log('🔍 Attempting to reconnect...')
    socket.connect()
  }
})

// Make socket available globally for debugging
if (typeof window !== 'undefined') {
  (window as any).socket = socket
}


