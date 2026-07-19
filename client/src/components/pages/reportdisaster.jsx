import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Camera, Send, LocateFixed } from 'lucide-react';
import { submitReport } from '../../store/slices/reportSlice';
import { DISASTER_TYPES } from '../../utils/constants';
import useGeolocation from '../../hooks/useGeolocation';

export default function ReportDisaster() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { register, handleSubmit, setValue, formState: { errors } } = useForm();
  const { position, requestLocation, loading: locating } = useGeolocation();
  const [image, setImage] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  if (position) {
    setValue('lat', position.lat);
    setValue('lng', position.lng);
  }

  const onSubmit = async (values) => {
    setSubmitting(true);
    const formData = new FormData();
    formData.append('disaster_type', values.disaster_type);
    formData.append('description', values.description);
    formData.append('lat', values.lat);
    formData.append('lng', values.lng);
    if (values.address) formData.append('address', values.address);
    if (image) formData.append('image', image);

    const result = await dispatch(submitReport(formData));
    setSubmitting(false);

    if (submitReport.fulfilled.match(result)) {
      toast.success('Report submitted — thank you for helping keep others safe.');
      navigate('/dashboard');
    } else {
      toast.error(result.payload || 'Could not submit report');
    }
  };

  return (
    <div className="mx-auto max-w-xl px-4 py-10">
      <h1 className="text-2xl font-bold">Report a Disaster</h1>
      <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
        Add a photo if you can — our AI will analyze it to help estimate severity.
      </p>

      <form onSubmit={handleSubmit(onSubmit)} className="card mt-6 space-y-4">
        <div>
          <label className="label">Disaster type</label>
          <select className="input" {...register('disaster_type', { required: true })}>
            {DISASTER_TYPES.map((t) => <option key={t.value} value={t.value}>{t.label}</option>)}
          </select>
        </div>

        <div>
          <label className="label">Description</label>
          <textarea className="input" rows={4} {...register('description', { required: 'Description is required', minLength: 5 })} />
          {errors.description && <p className="mt-1 text-xs text-primary-600">{errors.description.message}</p>}
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="label">Latitude</label>
            <input className="input" type="number" step="any" {...register('lat', { required: true })} />
          </div>
          <div>
            <label className="label">Longitude</label>
            <input className="input" type="number" step="any" {...register('lng', { required: true })} />
          </div>
        </div>
        <button type="button" className="btn-secondary text-sm" onClick={requestLocation} disabled={locating}>
          <LocateFixed size={16} /> {locating ? 'Locating…' : 'Use my current location'}
        </button>

        <div>
          <label className="label">Address (optional)</label>
          <input className="input" {...register('address')} />
        </div>

        <div>
          <label className="label">Photo (optional)</label>
          <label className="flex cursor-pointer items-center gap-2 rounded-lg border border-dashed border-gray-300 dark:border-gray-700 p-3 text-sm text-gray-500 hover:border-primary-400">
            <Camera size={18} />
            {image ? image.name : 'Upload a photo of the scene'}
            <input type="file" accept="image/*" className="hidden" onChange={(e) => setImage(e.target.files?.[0] || null)} />
          </label>
        </div>

        <button type="submit" className="btn-primary w-full" disabled={submitting}>
          <Send size={16} /> {submitting ? 'Submitting…' : 'Submit Report'}
        </button>
      </form>
    </div>
  );
}
