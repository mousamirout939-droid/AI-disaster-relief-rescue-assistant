import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { Menu, Moon, Sun, LogOut, User } from 'lucide-react';
import useAuth from '../../hooks/useAuth';
import { toggleTheme, toggleSidebar } from '../../store/slices/uiSlice';
import LanguageSelector from '../languageselector';
import './navbar.css';

export default function Navbar() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="navbar">
      <div className="navbar__inner">
        <button className="navbar__icon-btn lg:hidden" onClick={() => dispatch(toggleSidebar())} aria-label="Open menu">
          <Menu size={20} />
        </button>

        <Link to="/" className="navbar__brand">
          🛟 <span>Disaster Relief</span>
        </Link>

        <nav className="navbar__links hidden md:flex">
          <Link to="/shelters">Shelters</Link>
          <Link to="/hospitals">Hospitals</Link>
          <Link to="/rescue-teams">Rescue Teams</Link>
          <Link to="/alerts">Alerts</Link>
          <Link to="/emergency-guide">Emergency Guide</Link>
        </nav>

        <div className="navbar__actions">
          <LanguageSelector />
          <button className="navbar__icon-btn" onClick={() => dispatch(toggleTheme())} aria-label="Toggle dark mode">
            <Sun size={18} className="block dark:hidden" />
            <Moon size={18} className="hidden dark:block" />
          </button>

          {isAuthenticated ? (
            <div className="relative">
              <button className="navbar__icon-btn" onClick={() => setMenuOpen((o) => !o)} aria-label="Account menu">
                <User size={18} />
              </button>
              {menuOpen && (
                <div className="navbar__dropdown">
                  <p className="px-3 py-2 text-sm font-medium truncate">{user?.name || user?.email}</p>
                  <Link to="/profile" onClick={() => setMenuOpen(false)}>Profile</Link>
                  <Link to="/dashboard" onClick={() => setMenuOpen(false)}>Dashboard</Link>
                  {user?.role === 'admin' && <Link to="/admin" onClick={() => setMenuOpen(false)}>Admin</Link>}
                  <button onClick={handleLogout} className="navbar__dropdown-logout">
                    <LogOut size={14} /> Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            <Link to="/login" className="btn-primary !py-2 !px-3 text-sm">Sign in</Link>
          )}
        </div>
      </div>
    </header>
  );
}
