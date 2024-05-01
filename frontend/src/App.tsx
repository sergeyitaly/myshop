import { Route, Routes } from 'react-router-dom';
import { Layout } from './layout/Layout/Layout';
import CollectionsPage from './pages/CollectionPage/CollectionsPage';
import CollectionItemsPage from './pages/CollectionItem/CollectionItems';
import { Home } from './pages/home/home';
import { NotFound } from './pages/not-found/not-found';
import axios from 'axios';
import CarouselBestseller from './pages/CollectionPage/CarouselBestseller/CarouselBestseller';
import  {useState, useEffect } from 'react';

interface Collection {
    id: string;
    name: string;
    photo: string;
    category: string;
}

interface Product {
    id: string;
    name: string;
    price: string;
    photo: string;
}

function App() {
    const [collections, setCollections] = useState<Collection[]>([]);
    const [products, setProducts] = useState<Product[]>([]);

    useEffect(() => {
        const fetchCollections = async () => {
            try {
                const response = await axios.get<{ results: Collection[]; next: string | null }>('http://localhost:8000/collections/');
                setCollections(response.data.results);
            } catch (error) {
                console.error('Error fetching collections:', error);
            }
        };

        const fetchProducts = async () => {
            try {
                const response = await axios.get<Product[]>('http://localhost:8000/products/');
                setProducts(response.data);
            } catch (error) {
                console.error('Error fetching products:', error);
            }
        };

        fetchCollections();
        fetchProducts();
    }, []);


    return (
        <Routes>
            <Route element={<Layout withFooter withHeader />}>
                <Route index element={<Home />} />
                <Route path="/collections" element={<CollectionsPage collections={collections} />} />
                <Route path="/collection/:id" element={<CollectionItemsPage collections={collections} products={products} />} />
                <Route path="/products" element={<CarouselBestseller products={products} />} />
                <Route path="*" element={<NotFound />} />
            </Route>
        </Routes>
    );
}

export default App;
