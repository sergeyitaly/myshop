import { Route, Routes } from 'react-router-dom';
import { Layout } from './layout/Layout/Layout';
import CollectionItemsPage from './pages/CollectionItem/CollectionItems';
import CollectionsPage from './pages/CollectionPage/CollectionsPage';
import { Home } from './pages/home/home';
import { NotFound } from './pages/not-found/not-found';
import { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
    const [collections, setCollections] = useState([]);
//    const [collection, setCollection] = useState([]);

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


//        const fetchCollection = async () => {
//            try {
//                const response = await axios.get('/collections/:id/');
//                setCollection(response.data);
//            } catch (error) {
//                console.error('Error fetching collection:', error);
 //           }
//       };
//        fetchCollection();
    }, []);

    return (
        <Routes>
            <Route element={<Layout withFooter withHeader />}>
                <Route index element={<Home />} />
                <Route path="/collections" element={<CollectionsPage collections={collections} />} />
                <Route path="/collections/:id" element={<CollectionItemsPage />} 
                //collection={collection} />}
                />
                <Route path="*" element={<NotFound />} />
            </Route>
        </Routes>
    );
}

export default App;
