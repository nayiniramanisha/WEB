import { io } from 'socket.io-client'

const socketUrl = import.meta.env.VITE_SOCKET_URL || 'http://localhost:8000'
console.log('🔍 Socket connecting to:', socketUrl)

export const socket = io(socketUrl, {
  autoConnect: true,
  // Let the client negotiate transport (polling -> websocket upgrade) for broader compatibility
  // Explicitly set the default Socket.IO path
  path: '/socket.io',
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
})

// Make socket available globally for debugging
if (typeof window !== 'undefined') {
  (window as any).socket = socket
}


