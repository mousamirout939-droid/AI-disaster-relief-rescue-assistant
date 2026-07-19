import { Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import useDarkMode from './hooks/useDarkMode';
import ProtectedRoute from './context/ProtectedRoute';
import Layout from './components/layout';

import Home from './components/pages/home';
import Login from './components/pages/login';
import Register from './components/pages/register';
import Dashboard from './components/pages/dashboard';
import Profile from './components/pages/profile';
import ReportDisaster from './components/pages/reportdisaster';
import ShelterLocator from './components/pages/shelterlocator';
import HospitalLocator from './components/pages/hospitallocator';
import RescueTeams from './components/pages/rescueteams';
import Alerts from './components/pages/alerts';
import SafeRoute from './components/pages/saferoute';
import EmergencyGuide from './components/pages/emergencyguide';
import Volunteer from './components/pages/volunteer';
import Admin from './components/pages/admin';
import NotFound from './components/pages/notfound';

import './App.css';

export default function App() {
  useDarkMode();

  return (
    <>
      <Toaster position="top-right" toastOptions={{ duration: 4000 }} />
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/shelters" element={<ShelterLocator />} />
          <Route path="/hospitals" element={<HospitalLocator />} />
          <Route path="/rescue-teams" element={<RescueTeams />} />
          <Route path="/alerts" element={<Alerts />} />
          <Route path="/safe-route" element={<SafeRoute />} />
          <Route path="/emergency-guide" element={<EmergencyGuide />} />
          <Route path="/volunteer" element={<Volunteer />} />

          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/report-disaster" element={<ReportDisaster />} />
          </Route>

          <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
            <Route path="/admin" element={<Admin />} />
          </Route>

          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </>
  );
}
