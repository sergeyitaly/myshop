import { useState, useEffect } from 'react';
import { Route, Routes} from 'react-router-dom';
import { Layout } from './layout/Layout/Layout';
import CollectionsPage from './pages/CollectionPage/CollectionsPage';
import CollectionItemsPage from './pages/CollectionItem/CollectionItems';
import { Home } from './pages/home/home';
import { NotFound } from './pages/not-found/not-found';
import axios from 'axios';

interface Collection {
    id: string;
    name: string;
    photo: string;
    price: string;
    category: string;
}

function App() {
    const [collections, setCollections] = useState<Collection[]>([]);
    useEffect(() => {
        const fetchCollections = async () => {
            try {
                const response = await axios.get('/collections/');
                setCollections(response.data);
            } catch (error) {
                console.error('Error fetching collections:', error);
            }
        };
        fetchCollections();
    }, []);

    return (
        <Routes>
            <Route element={<Layout withFooter withHeader />}>
                <Route index element={<Home />} />
                <Route path="/collections" element={<CollectionsPage collections={collections} />} />
                <Route path="/collection/:id" element={<CollectionItemsPage />} />
                <Route path="*" element={<NotFound />} />
            </Route>
        </Routes>
    );
}

export default App;
