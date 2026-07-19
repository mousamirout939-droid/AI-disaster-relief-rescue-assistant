import { NavLink } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { X, Home, MapPin, Hospital, Users, Bell, ShieldAlert, BookOpen, HeartHandshake } from 'lucide-react';
import { closeSidebar } from '../../store/slices/uiSlice';
import useAuth from '../../hooks/useAuth';
import './sidebar.css';

const LINKS = [
  { to: '/', label: 'Home', icon: Home },
  { to: '/dashboard', label: 'Dashboard', icon: ShieldAlert, auth: true },
  { to: '/report-disaster', label: 'Report Disaster', icon: MapPin, auth: true },
  { to: '/shelters', label: 'Shelters', icon: Home },
  { to: '/hospitals', label: 'Hospitals', icon: Hospital },
  { to: '/rescue-teams', label: 'Rescue Teams', icon: Users },
  { to: '/alerts', label: 'Alerts', icon: Bell },
  { to: '/safe-route', label: 'Safe Route', icon: MapPin },
  { to: '/emergency-guide', label: 'Emergency Guide', icon: BookOpen },
  { to: '/volunteer', label: 'Volunteer', icon: HeartHandshake },
];

export default function Sidebar() {
  const dispatch = useDispatch();
  const open = useSelector((s) => s.ui.sidebarOpen);
  const { isAuthenticated } = useAuth();

  const links = LINKS.filter((l) => !l.auth || isAuthenticated);

  return (
    <>
      {open && <div className="sidebar__overlay lg:hidden" onClick={() => dispatch(closeSidebar())} />}
      <aside className={`sidebar ${open ? 'sidebar--open' : ''}`}>
        <div className="flex items-center justify-between px-4 py-4 lg:hidden">
          <span className="font-bold text-primary-600">Menu</span>
          <button onClick={() => dispatch(closeSidebar())} aria-label="Close menu">
            <X size={20} />
          </button>
        </div>
        <nav className="sidebar__nav">
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              onClick={() => dispatch(closeSidebar())}
              className={({ isActive }) => `sidebar__link ${isActive ? 'sidebar__link--active' : ''}`}
            >
              <Icon size={17} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>
      </aside>
    </>
  );
}
