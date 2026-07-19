/** In-app notifications (bell icon dropdown). */
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { notificationApi } from '../../api/endpoints';

export const fetchNotifications = createAsyncThunk('notifications/fetchAll', async (_, { rejectWithValue }) => {
  try {
    const { data } = await notificationApi.list();
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not fetch notifications');
  }
});

export const markNotificationRead = createAsyncThunk('notifications/markRead', async (id, { rejectWithValue }) => {
  try {
    await notificationApi.markRead(id);
    return id;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not update notification');
  }
});

const notificationSlice = createSlice({
  name: 'notifications',
  initialState: { items: [], status: 'idle' },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchNotifications.fulfilled, (state, action) => { state.items = action.payload; })
      .addCase(markNotificationRead.fulfilled, (state, action) => {
        const n = state.items.find((i) => i.id === action.payload);
        if (n) n.read = true;
      });
  },
});

export default notificationSlice.reducer;
