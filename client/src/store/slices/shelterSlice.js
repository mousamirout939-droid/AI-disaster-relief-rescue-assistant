/** Shelters: list + nearby geo search. */
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { shelterApi } from '../../api/endpoints';

export const fetchShelters = createAsyncThunk('shelters/fetchAll', async (_, { rejectWithValue }) => {
  try {
    const { data } = await shelterApi.list();
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not fetch shelters');
  }
});

export const fetchNearbyShelters = createAsyncThunk('shelters/fetchNearby', async ({ lat, lng, radius_km }, { rejectWithValue }) => {
  try {
    const { data } = await shelterApi.nearby(lat, lng, radius_km);
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not fetch nearby shelters');
  }
});

const shelterSlice = createSlice({
  name: 'shelters',
  initialState: { items: [], status: 'idle', error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchShelters.pending, (state) => { state.status = 'loading'; })
      .addCase(fetchShelters.fulfilled, (state, action) => { state.status = 'succeeded'; state.items = action.payload; })
      .addCase(fetchShelters.rejected, (state, action) => { state.status = 'failed'; state.error = action.payload; })
      .addCase(fetchNearbyShelters.fulfilled, (state, action) => { state.items = action.payload; });
  },
});

export default shelterSlice.reducer;
