// App.tsx
import { useState, useEffect } from 'react';
import { Route, Routes } from 'react-router-dom';
import { Layout } from './layout/Layout/Layout';
import CollectionsPage from './pages/CollectionPage/CollectionsPage';
import { Home } from './pages/home/home';
import { NotFound } from './pages/not-found/not-found';
import axios from 'axios';
import CarouselBestseller from './pages/CollectionPage/CarouselBestseller/CarouselBestseller';
import CollectionItemsPage from './pages/CollectionItem/CollectionItems';


const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;

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
    const [nextPage, setNextPage] = useState<string | null>(null);

    useEffect(() => {
        localStorage.setItem('pageCounter', '1');

        const fetchCollections = async () => {
            try {
                const response = await axios.get<{ results: Collection[]; next: string | null }>(`${apiBaseUrl}/collections/`);
                setCollections(response.data.results);
                setNextPage(response.data.next);
            } catch (error) {
                console.error('Error fetching collections:', error);
            }
        };

        const fetchProducts = async () => {
            try {
                const response = await axios.get<{ results: Product[]; next: string | null }>(`${apiBaseUrl}/products/`);
                setProducts(response.data.results);
                setNextPage(response.data.next);
            } catch (error) {
                console.error('Error fetching products:', error);
            }
        };

        fetchCollections();
        fetchProducts();
    }, []);

    const loadMoreCollections = async () => {
        if (nextPage) {
            try {
                const response = await axios.get<{ results: Collection[]; next: string | null }>(nextPage);
                setCollections([...collections, ...response.data.results]);
                setNextPage(response.data.next);
                const pageCounter = localStorage.getItem('pageCounter');
                if (pageCounter) {
                    localStorage.setItem('pageCounter', String(parseInt(pageCounter) + 1));
                }
            } catch (error) {
                console.error('Error fetching more collections:', error);
            }
        }
    };

    const loadMoreProducts = async () => {
        if (nextPage) {
            try {
                const response = await axios.get<{ results: Product[]; next: string | null }>(nextPage);
                setProducts([...products, ...response.data.results]);
                setNextPage(response.data.next);
            } catch (error) {
                console.error('Error fetching more products:', error);
            }
        }
    };

    return (
        <Routes>
            <Route element={<Layout withFooter withHeader />}>
                <Route index element={<Home />} />
                <Route
                    path="/collections"
                    element={<CollectionsPage collections={collections} loadMoreCollections={loadMoreCollections} hasNextPage={nextPage !== null} />}
                />
                <Route
                    path="/collection/:id"
                    element={<CollectionItemsPage products={products} loadMoreProducts={loadMoreProducts} />}
                />
                <Route path="/products" element={<CarouselBestseller products={products} />} />
                <Route path="*" element={<NotFound />} />
            </Route>
        </Routes>
    );
}

export default App;
