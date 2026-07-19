import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useDispatch, useSelector } from 'react-redux';
import toast from 'react-hot-toast';
import { Save } from 'lucide-react';
import { fetchCurrentUser, updateUserProfile } from '../../store/slices/authSlice';

export default function Profile() {
  const dispatch = useDispatch();
  const { user } = useSelector((s) => s.auth);
  const { register, handleSubmit, reset } = useForm();

  useEffect(() => {
    dispatch(fetchCurrentUser());
  }, [dispatch]);

  useEffect(() => {
    if (user) reset({ name: user.name, phone: user.phone || '', preferred_language: user.preferred_language || 'en' });
  }, [user, reset]);

  const onSubmit = async (values) => {
    const result = await dispatch(updateUserProfile(values));
    if (updateUserProfile.fulfilled.match(result)) {
      toast.success('Profile updated');
    } else {
      toast.error(result.payload || 'Update failed');
    }
  };

  return (
    <div className="mx-auto max-w-lg px-4 py-10">
      <h1 className="text-2xl font-bold">Your Profile</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="card mt-6 space-y-4">
        <div>
          <label className="label">Full name</label>
          <input className="input" {...register('name')} />
        </div>
        <div>
          <label className="label">Email</label>
          <input className="input" value={user?.email || ''} disabled />
        </div>
        <div>
          <label className="label">Phone</label>
          <input className="input" {...register('phone')} />
        </div>
        <button type="submit" className="btn-primary"><Save size={16} /> Save changes</button>
      </form>
    </div>
  );
}
