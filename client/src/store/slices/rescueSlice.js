/** Rescue teams: list + nearby geo search + dispatch action. */
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { rescueApi } from '../../api/endpoints';

export const fetchRescueTeams = createAsyncThunk('rescue/fetchAll', async (_, { rejectWithValue }) => {
  try {
    const { data } = await rescueApi.list();
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not fetch rescue teams');
  }
});

export const fetchNearbyRescueTeams = createAsyncThunk('rescue/fetchNearby', async ({ lat, lng, radius_km }, { rejectWithValue }) => {
  try {
    const { data } = await rescueApi.nearby(lat, lng, radius_km);
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not fetch nearby rescue teams');
  }
});

export const dispatchRescueTeam = createAsyncThunk('rescue/dispatch', async ({ teamId, reportId }, { rejectWithValue }) => {
  try {
    const { data } = await rescueApi.dispatch(teamId, reportId);
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not dispatch team');
  }
});

const rescueSlice = createSlice({
  name: 'rescue',
  initialState: { items: [], status: 'idle', error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchRescueTeams.pending, (state) => { state.status = 'loading'; })
      .addCase(fetchRescueTeams.fulfilled, (state, action) => { state.status = 'succeeded'; state.items = action.payload; })
      .addCase(fetchRescueTeams.rejected, (state, action) => { state.status = 'failed'; state.error = action.payload; })
      .addCase(fetchNearbyRescueTeams.fulfilled, (state, action) => { state.items = action.payload; })
      .addCase(dispatchRescueTeam.fulfilled, (state, action) => {
        const idx = state.items.findIndex((t) => t.id === action.payload.id);
        if (idx !== -1) state.items[idx] = action.payload;
      });
  },
});

export default rescueSlice.reducer;
