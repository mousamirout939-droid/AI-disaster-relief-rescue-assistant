/** All backend REST calls, grouped by resource. Every response envelope is { success, message, data }. */
import axiosClient from './axiosClient';

// --- Auth ---
export const authApi = {
  register: (payload) => axiosClient.post('/auth/register', payload),
  login: (payload) => axiosClient.post('/auth/login', payload),
  me: () => axiosClient.get('/auth/me'),
  changePassword: (payload) => axiosClient.post('/auth/change-password', payload),
};

// --- Users ---
export const userApi = {
  getProfile: () => axiosClient.get('/users/profile'),
  updateProfile: (payload) => axiosClient.put('/users/profile', payload),
};

// --- Reports ---
export const reportApi = {
  create: (formData) =>
    axiosClient.post('/reports', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
  list: (params) => axiosClient.get('/reports', { params }),
  mine: () => axiosClient.get('/reports/mine'),
  getById: (id) => axiosClient.get(`/reports/${id}`),
  updateStatus: (id, status) => axiosClient.patch(`/reports/${id}/status`, { status }),
};

// --- Shelters ---
export const shelterApi = {
  list: () => axiosClient.get('/shelters'),
  nearby: (lat, lng, radius_km = 15) => axiosClient.get('/shelters/nearby', { params: { lat, lng, radius_km } }),
  create: (payload) => axiosClient.post('/shelters', payload),
};

// --- Hospitals ---
export const hospitalApi = {
  list: () => axiosClient.get('/hospitals'),
  nearby: (lat, lng, radius_km = 15) => axiosClient.get('/hospitals/nearby', { params: { lat, lng, radius_km } }),
  create: (payload) => axiosClient.post('/hospitals', payload),
};

// --- Rescue teams ---
export const rescueApi = {
  list: () => axiosClient.get('/rescue-teams'),
  nearby: (lat, lng, radius_km = 25) => axiosClient.get('/rescue-teams/nearby', { params: { lat, lng, radius_km } }),
  dispatch: (teamId, reportId) => axiosClient.post(`/rescue-teams/${teamId}/dispatch`, { report_id: reportId }),
};

// --- Alerts ---
export const alertApi = {
  list: () => axiosClient.get('/alerts'),
  create: (payload) => axiosClient.post('/alerts', payload),
};

// --- Notifications ---
export const notificationApi = {
  list: () => axiosClient.get('/notifications'),
  markRead: (id) => axiosClient.patch(`/notifications/${id}/read`),
};

// --- AI ---
export const aiApi = {
  detect: (formData) =>
    axiosClient.post('/ai/detect', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
  chat: (message, history) => axiosClient.post('/ai/chat', { message, history }),
};

// --- Weather ---
export const weatherApi = {
  current: (lat, lng) => axiosClient.get('/weather/current', { params: { lat, lng } }),
};

// --- Translation ---
export const translationApi = {
  corePhrase: (key, lang) => axiosClient.get('/translate/core-phrase', { params: { key, lang } }),
};

// --- Safe route ---
export const routeApi = {
  safe: (origin, destination) => axiosClient.get('/routes/safe', { params: { origin, destination } }),
};

// --- Emergency (SOS + contacts) ---
export const emergencyApi = {
  sos: (lat, lng) => axiosClient.post('/emergency/sos', { lat, lng }),
  listContacts: () => axiosClient.get('/emergency/contacts'),
  addContact: (payload) => axiosClient.post('/emergency/contacts', payload),
  deleteContact: (id) => axiosClient.delete(`/emergency/contacts/${id}`),
};

// --- Volunteers ---
export const volunteerApi = {
  register: (payload) => axiosClient.post('/volunteers', payload),
  list: () => axiosClient.get('/volunteers'),
  approve: (id) => axiosClient.patch(`/volunteers/${id}/approve`),
};

// --- Admin ---
export const adminApi = {
  dashboardStats: () => axiosClient.get('/admin/dashboard'),
  listUsers: () => axiosClient.get('/admin/users'),
  setUserActive: (id, is_active) => axiosClient.patch(`/admin/users/${id}/active`, null, { params: { is_active } }),
};
