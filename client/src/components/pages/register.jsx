import { useForm } from 'react-hook-form';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { UserPlus } from 'lucide-react';
import { registerUser } from '../../store/slices/authSlice';

export default function Register() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { status } = useSelector((s) => s.auth);
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = async (values) => {
    const result = await dispatch(registerUser(values));
    if (registerUser.fulfilled.match(result)) {
      toast.success('Account created!');
      navigate('/dashboard');
    } else {
      toast.error(result.payload || 'Registration failed');
    }
  };

  return (
    <div className="mx-auto flex min-h-[80vh] max-w-md flex-col justify-center px-4 py-12">
      <div className="card">
        <h1 className="mb-1 text-2xl font-bold">Create an account</h1>
        <p className="mb-6 text-sm text-gray-500 dark:text-gray-400">Join to report disasters and access emergency tools.</p>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="label">Full name</label>
            <input className="input" {...register('name', { required: 'Name is required', minLength: { value: 2, message: 'Too short' } })} />
            {errors.name && <p className="mt-1 text-xs text-primary-600">{errors.name.message}</p>}
          </div>
          <div>
            <label className="label">Email</label>
            <input className="input" type="email" {...register('email', { required: 'Email is required' })} />
            {errors.email && <p className="mt-1 text-xs text-primary-600">{errors.email.message}</p>}
          </div>
          <div>
            <label className="label">Phone</label>
            <input className="input" {...register('phone')} />
          </div>
          <div>
            <label className="label">Password</label>
            <input
              className="input" type="password"
              {...register('password', {
                required: 'Password is required',
                minLength: { value: 8, message: 'At least 8 characters' },
                pattern: { value: /(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, message: 'Needs upper, lower, and a digit' },
              })}
            />
            {errors.password && <p className="mt-1 text-xs text-primary-600">{errors.password.message}</p>}
          </div>
          <button type="submit" className="btn-primary w-full" disabled={status === 'loading'}>
            <UserPlus size={16} /> {status === 'loading' ? 'Creating account…' : 'Create account'}
          </button>
        </form>

        <p className="mt-5 text-center text-sm text-gray-500 dark:text-gray-400">
          Already have an account? <Link to="/login" className="font-medium text-primary-600">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
