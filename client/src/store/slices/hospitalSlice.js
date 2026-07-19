/** Hospitals: list + nearby geo search. */
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { hospitalApi } from '../../api/endpoints';

export const fetchHospitals = createAsyncThunk('hospitals/fetchAll', async (_, { rejectWithValue }) => {
  try {
    const { data } = await hospitalApi.list();
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not fetch hospitals');
  }
});

export const fetchNearbyHospitals = createAsyncThunk('hospitals/fetchNearby', async ({ lat, lng, radius_km }, { rejectWithValue }) => {
  try {
    const { data } = await hospitalApi.nearby(lat, lng, radius_km);
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not fetch nearby hospitals');
  }
});

const hospitalSlice = createSlice({
  name: 'hospitals',
  initialState: { items: [], status: 'idle', error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchHospitals.pending, (state) => { state.status = 'loading'; })
      .addCase(fetchHospitals.fulfilled, (state, action) => { state.status = 'succeeded'; state.items = action.payload; })
      .addCase(fetchHospitals.rejected, (state, action) => { state.status = 'failed'; state.error = action.payload; })
      .addCase(fetchNearbyHospitals.fulfilled, (state, action) => { state.items = action.payload; });
  },
});

export default hospitalSlice.reducer;
