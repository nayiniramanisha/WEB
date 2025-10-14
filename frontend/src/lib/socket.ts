import { io } from 'socket.io-client'

const socketUrl = import.meta.env.VITE_SOCKET_URL || 'http://localhost:8000'
console.log('🔍 Socket connecting to:', socketUrl)

export const socket = io(socketUrl, {
  autoConnect: true,
  // Simplified configuration for better compatibility
  path: '/socket.io',
  // Connection settings - increased for AI processing
  timeout: 120000, // 2 minutes timeout for AI processing
  forceNew: false,
  transports: ['polling', 'websocket'],
  upgrade: true,
  rememberUpgrade: false,
  // Extended timeout settings for AI processing
  pingTimeout: 120000, // 2 minutes - enough for AI processing
  pingInterval: 30000, // 30 seconds - less frequent pings
  // Reconnection settings
  reconnection: true,
  reconnectionAttempts: 15, // More attempts
  reconnectionDelay: 2000, // Longer initial delay
  reconnectionDelayMax: 15000, // Longer max delay
  // Additional stability settings
  randomizationFactor: 0.5,
  maxReconnectionAttempts: 15,
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


