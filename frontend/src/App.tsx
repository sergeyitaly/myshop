import { Route, Routes } from 'react-router-dom';
import { Home } from './pages/home';
import { Layout } from './layout/Layout/Layout';

function App() {
    return (
        <>
            <Routes>
                <Route element={<Layout withFooter withHeader/>}>
                    <Route
                        index
                        element={<Home />}
                    />
                    <Route
                        path="collection"
                        element={<h1>Collection</h1>}
                    />
                </Route>
            </Routes>
        </>
    );
}

export default App;
