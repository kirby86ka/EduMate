import { Link, useLocation } from 'react-router-dom'
import { cn } from '../lib/utils'

export default function Navbar() {
  const location = useLocation()
  
  const navItems = [
    { name: 'Home', path: '/' },
    { name: 'Subjects', path: '/subjects' },
    { name: 'Dashboard', path: '/dashboard' },
  ]
  
  return (
    <nav className="border-b bg-white/50 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold text-primary">
              AdaptLearn
            </Link>
          </div>
          
          <div className="flex space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  "text-sm font-medium transition-colors hover:text-primary",
                  location.pathname === item.path
                    ? "text-primary"
                    : "text-muted-foreground"
                )}
              >
                {item.name}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}
