/** Convenience hook exposing auth state + the logout action. */
import { useDispatch, useSelector } from 'react-redux';
import { logout as logoutAction } from '../store/slices/authSlice';

export default function useAuth() {
  const dispatch = useDispatch();
  const { user, isAuthenticated, status, error } = useSelector((s) => s.auth);

  const logout = () => dispatch(logoutAction());

  return { user, isAuthenticated, status, error, logout, role: user?.role };
}
