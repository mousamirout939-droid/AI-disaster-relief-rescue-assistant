/** Root Redux Toolkit store — combines every feature slice. */
import { configureStore } from '@reduxjs/toolkit';

import authReducer from './slices/authSlice';
import uiReducer from './slices/uiSlice';
import reportReducer from './slices/reportSlice';
import shelterReducer from './slices/shelterSlice';
import hospitalReducer from './slices/hospitalSlice';
import rescueReducer from './slices/rescueSlice';
import alertReducer from './slices/alertSlice';
import notificationReducer from './slices/notificationSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    ui: uiReducer,
    reports: reportReducer,
    shelters: shelterReducer,
    hospitals: hospitalReducer,
    rescue: rescueReducer,
    alerts: alertReducer,
    notifications: notificationReducer,
  },
});

export default store;
