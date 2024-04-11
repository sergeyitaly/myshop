import { Route, Routes } from 'react-router-dom';
import { Home } from './pages/home/home';
import { Layout } from './layout/Layout/Layout';
import { NotFound } from './pages/not-found/not-found';

function App() {
    return (
        <>
            <Routes>
                <Route
                    element={
                        <Layout
                            withFooter
                            withHeader
                        />
                    }
                >
                    <Route
                        index
                        element={<Home />}
                    />
                    <Route
                        path="collection"
                        element={<h1>Collection</h1>}
                    />
                    <Route
                        path="*"
                        element={<NotFound />}
                    />
                </Route>
            </Routes>
        </>
    );
}

export default App;
