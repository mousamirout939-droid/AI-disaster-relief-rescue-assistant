import { useForm } from 'react-hook-form';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { LogIn } from 'lucide-react';
import { loginUser } from '../../store/slices/authSlice';

export default function Login() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { status } = useSelector((s) => s.auth);
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = async (values) => {
    const result = await dispatch(loginUser(values));
    if (loginUser.fulfilled.match(result)) {
      toast.success('Welcome back!');
      navigate('/dashboard');
    } else {
      toast.error(result.payload || 'Login failed');
    }
  };

  return (
    <div className="mx-auto flex min-h-[80vh] max-w-md flex-col justify-center px-4 py-12">
      <div className="card">
        <h1 className="mb-1 text-2xl font-bold">Sign in</h1>
        <p className="mb-6 text-sm text-gray-500 dark:text-gray-400">Access your dashboard and emergency tools.</p>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="label">Email</label>
            <input className="input" type="email" {...register('email', { required: 'Email is required' })} />
            {errors.email && <p className="mt-1 text-xs text-primary-600">{errors.email.message}</p>}
          </div>
          <div>
            <label className="label">Password</label>
            <input className="input" type="password" {...register('password', { required: 'Password is required' })} />
            {errors.password && <p className="mt-1 text-xs text-primary-600">{errors.password.message}</p>}
          </div>
          <button type="submit" className="btn-primary w-full" disabled={status === 'loading'}>
            <LogIn size={16} /> {status === 'loading' ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <p className="mt-5 text-center text-sm text-gray-500 dark:text-gray-400">
          Don't have an account? <Link to="/register" className="font-medium text-primary-600">Register</Link>
        </p>
      </div>
    </div>
  );
}
