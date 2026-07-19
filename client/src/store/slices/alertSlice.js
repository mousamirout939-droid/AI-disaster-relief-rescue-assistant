/** Disaster/weather alerts. */
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { alertApi } from '../../api/endpoints';

export const fetchAlerts = createAsyncThunk('alerts/fetchAll', async (_, { rejectWithValue }) => {
  try {
    const { data } = await alertApi.list();
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not fetch alerts');
  }
});

export const createAlert = createAsyncThunk('alerts/create', async (payload, { rejectWithValue }) => {
  try {
    const { data } = await alertApi.create(payload);
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not create alert');
  }
});

const alertSlice = createSlice({
  name: 'alerts',
  initialState: { items: [], status: 'idle', error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchAlerts.pending, (state) => { state.status = 'loading'; })
      .addCase(fetchAlerts.fulfilled, (state, action) => { state.status = 'succeeded'; state.items = action.payload; })
      .addCase(fetchAlerts.rejected, (state, action) => { state.status = 'failed'; state.error = action.payload; })
      .addCase(createAlert.fulfilled, (state, action) => { state.items.unshift(action.payload); });
  },
});

export default alertSlice.reducer;
