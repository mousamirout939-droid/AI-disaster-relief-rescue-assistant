/** Auth state: current user, tokens, and login/register/me async thunks. */
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { authApi, userApi } from '../../api/endpoints';

const initialState = {
  user: null,
  accessToken: localStorage.getItem('access_token') || null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  status: 'idle', // idle | loading | succeeded | failed
  error: null,
};

export const registerUser = createAsyncThunk('auth/register', async (payload, { rejectWithValue }) => {
  try {
    const { data } = await authApi.register(payload);
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Registration failed');
  }
});

export const loginUser = createAsyncThunk('auth/login', async (payload, { rejectWithValue }) => {
  try {
    const { data } = await authApi.login(payload);
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Login failed');
  }
});

export const fetchCurrentUser = createAsyncThunk('auth/me', async (_, { rejectWithValue }) => {
  try {
    const { data } = await authApi.me();
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Could not fetch profile');
  }
});

export const updateUserProfile = createAsyncThunk('auth/updateProfile', async (payload, { rejectWithValue }) => {
  try {
    const { data } = await userApi.updateProfile(payload);
    return data.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.message || 'Update failed');
  }
});

const persistTokens = (tokens) => {
  localStorage.setItem('access_token', tokens.access_token);
  localStorage.setItem('refresh_token', tokens.refresh_token);
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout(state) {
      state.user = null;
      state.accessToken = null;
      state.isAuthenticated = false;
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(registerUser.pending, (state) => { state.status = 'loading'; state.error = null; })
      .addCase(registerUser.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.isAuthenticated = true;
        state.accessToken = action.payload.access_token;
        persistTokens(action.payload);
      })
      .addCase(registerUser.rejected, (state, action) => { state.status = 'failed'; state.error = action.payload; })

      .addCase(loginUser.pending, (state) => { state.status = 'loading'; state.error = null; })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.isAuthenticated = true;
        state.accessToken = action.payload.access_token;
        persistTokens(action.payload);
      })
      .addCase(loginUser.rejected, (state, action) => { state.status = 'failed'; state.error = action.payload; })

      .addCase(fetchCurrentUser.fulfilled, (state, action) => { state.user = action.payload; })
      .addCase(fetchCurrentUser.rejected, (state) => { state.user = null; state.isAuthenticated = false; })

      .addCase(updateUserProfile.fulfilled, (state, action) => { state.user = action.payload; });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;
