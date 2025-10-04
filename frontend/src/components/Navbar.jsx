import { Link, useLocation } from 'react-router-dom'
import { Brain } from 'lucide-react'
import { cn } from '../lib/utils'

export default function Navbar() {
  const location = useLocation()
  
  const navItems = [
    { name: 'Home', path: '/' },
    { name: 'Subjects', path: '/subjects' },
    { name: 'Dashboard', path: '/dashboard' },
  ]
  
  return (
    <nav className="border-b border-border bg-black/80 backdrop-blur-md sticky top-0 z-50 transition-smooth">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <Link to="/" className="text-xl sm:text-2xl font-bold flex items-center gap-2 transition-smooth hover:scale-105" style={{ color: 'hsl(var(--logo-yellow))' }}>
              <Brain className="w-6 h-6 sm:w-7 sm:h-7 animate-pulse" />
              <span className="hidden xs:inline">AdaptLearn</span>
              <span className="xs:hidden">AL</span>
            </Link>
          </div>
          
          <div className="flex space-x-4 sm:space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  "text-xs sm:text-sm font-medium transition-smooth hover:text-yellow-400 relative group",
                  location.pathname === item.path
                    ? "text-yellow-400"
                    : "text-muted-foreground"
                )}
              >
                {item.name}
                <span className={cn(
                  "absolute -bottom-1 left-0 w-0 h-0.5 bg-yellow-400 transition-all duration-300",
                  location.pathname === item.path ? "w-full" : "group-hover:w-full"
                )}></span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}
