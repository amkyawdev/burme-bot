import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Burme AI',
  description: 'Myanmar-first intelligent AI assistant',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="my">
      <body className="antialiased">
        <div className="min-h-screen bg-background">
          <div className="fixed inset-0 bg-gradient-radial from-purple-900/20 via-background to-background pointer-events-none" />
          <div className="fixed inset-0 bg-[url('/grid.svg')] opacity-[0.03] pointer-events-none" />
          {children}
        </div>
      </body>
    </html>
  )
}