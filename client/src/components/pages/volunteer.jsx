import { useState } from 'react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { HeartHandshake } from 'lucide-react';
import { volunteerApi } from '../../api/endpoints';

const SKILL_OPTIONS = ['first_aid', 'search_rescue', 'logistics', 'medical', 'translation', 'driving', 'cooking'];

export default function Volunteer() {
  const { register, handleSubmit, reset } = useForm();
  const [submitting, setSubmitting] = useState(false);

  const onSubmit = async (values) => {
    setSubmitting(true);
    const skills = Array.isArray(values.skills) ? values.skills : [values.skills].filter(Boolean);
    try {
      await volunteerApi.register({ ...values, skills });
      toast.success('Thanks for registering — we will review your application.');
      reset();
    } catch (err) {
      toast.error(err.response?.data?.message || 'Could not submit registration');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="mx-auto max-w-xl px-4 py-10">
      <h1 className="flex items-center gap-2 text-2xl font-bold"><HeartHandshake size={24} /> Volunteer With Us</h1>
      <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
        Join our network of volunteers who help during disaster response.
      </p>

      <form onSubmit={handleSubmit(onSubmit)} className="card mt-6 space-y-4">
        <div>
          <label className="label">Full name</label>
          <input className="input" {...register('name', { required: true })} />
        </div>
        <div>
          <label className="label">Email</label>
          <input className="input" type="email" {...register('email', { required: true })} />
        </div>
        <div>
          <label className="label">Phone</label>
          <input className="input" {...register('phone', { required: true })} />
        </div>
        <div>
          <label className="label">Skills</label>
          <div className="grid grid-cols-2 gap-2">
            {SKILL_OPTIONS.map((skill) => (
              <label key={skill} className="flex items-center gap-2 text-sm capitalize">
                <input type="checkbox" value={skill} {...register('skills')} />
                {skill.replace('_', ' ')}
              </label>
            ))}
          </div>
        </div>
        <div>
          <label className="label">Availability</label>
          <select className="input" {...register('availability')}>
            <option value="weekends">Weekends</option>
            <option value="weekdays">Weekdays</option>
            <option value="anytime">Anytime</option>
          </select>
        </div>
        <div>
          <label className="label">Location</label>
          <input className="input" {...register('location')} />
        </div>
        <button type="submit" className="btn-primary w-full" disabled={submitting}>
          {submitting ? 'Submitting…' : 'Register as Volunteer'}
        </button>
      </form>
    </div>
  );
}
