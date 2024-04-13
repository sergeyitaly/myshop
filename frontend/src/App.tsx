import { Route, Routes } from 'react-router-dom';
import { Home } from './pages/home';
import { Layout } from './layout/Layout/Layout';
import CollectionsPage from "./pages/CollectionPage/CollectionsPage";
import CollectionItemsPage from "./pages/CollectionItem/CollectionItems";
// import CollectionItems from "./pages/CollectionItem/CollectionItems";

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
                        path="collections"
                        element={<CollectionsPage />}
                    />
                    <Route
                        path="/collections/:id"
                        element={<CollectionItemsPage />} />

                </Route>
            </Routes>
        </>
    );
}

export default App;
