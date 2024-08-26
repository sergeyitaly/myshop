import { configureStore } from '@reduxjs/toolkit';
import { apiSlice } from '../api/mainApiSlice';
import { filterApiSlice } from '../api/filterApiSlice'; // Import filterApiSlice
import { basketSlice } from './basketSlice';
import { snackbarSlice } from './snackbarSlice';
import { searchSlice } from './searchSlice';

export const store = configureStore({
  reducer: {
    [apiSlice.reducerPath]: apiSlice.reducer,
    [filterApiSlice.reducerPath]: filterApiSlice.reducer, // Add filterApiSlice reducer
    basket: basketSlice.reducer,
    snackbar: snackbarSlice.reducer,
    searchBar: searchSlice.reducer
  },
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware()
      .concat(apiSlice.middleware)
      .concat(filterApiSlice.middleware), // Add filterApiSlice middleware
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch;
