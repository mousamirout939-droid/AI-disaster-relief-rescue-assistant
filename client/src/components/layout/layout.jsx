import { Outlet } from 'react-router-dom';
import Navbar from '../navbar';
import Sidebar from '../sidebar';
import Footer from '../footer';
import AIChat from '../AIchat';
import SOSButton from '../sosbutton';

/** Shared app shell: navbar + sidebar + page content + footer + floating widgets. */
export default function Layout() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1">
          <Outlet />
        </main>
      </div>
      <Footer />
      <AIChat />
      <SOSButton />
    </div>
  );
}
