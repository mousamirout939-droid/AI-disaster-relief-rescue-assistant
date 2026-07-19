/** Disaster reports: submission, listing, and "my reports". */
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { reportApi } from '../../api/endpoints';

export const submitReport = createAsyncThunk('reports/submit', async (formData, { rejectWithValue }) => {
  try {
    const { data } = await reportApi.create(formData);
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not submit report');
  }
});

export const fetchReports = createAsyncThunk('reports/fetchAll', async (params, { rejectWithValue }) => {
  try {
    const { data } = await reportApi.list(params);
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not fetch reports');
  }
});

export const fetchMyReports = createAsyncThunk('reports/fetchMine', async (_, { rejectWithValue }) => {
  try {
    const { data } = await reportApi.mine();
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not fetch your reports');
  }
});

const reportSlice = createSlice({
  name: 'reports',
  initialState: { items: [], myReports: [], status: 'idle', error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(submitReport.fulfilled, (state, action) => { state.items.unshift(action.payload); })
      .addCase(fetchReports.pending, (state) => { state.status = 'loading'; })
      .addCase(fetchReports.fulfilled, (state, action) => { state.status = 'succeeded'; state.items = action.payload; })
      .addCase(fetchReports.rejected, (state, action) => { state.status = 'failed'; state.error = action.payload; })
      .addCase(fetchMyReports.fulfilled, (state, action) => { state.myReports = action.payload; });
  },
});

export default reportSlice.reducer;
