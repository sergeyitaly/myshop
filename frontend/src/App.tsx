import { useState, useEffect } from 'react';
import { Route, Routes } from 'react-router-dom';
import { Layout } from './layout/Layout/Layout';
import CollectionsPage from './pages/CollectionPage/CollectionsPage';
import { Home } from './pages/home/home';
import { NotFound } from './pages/not-found/not-found';
import axios from 'axios';
import CarouselBestseller from './pages/CollectionPage/CarouselBestseller/CarouselBestseller';

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
        const fetchCollections = async () => {
            try {
                const response = await axios.get<{ results: Collection[]; next: string | null }>('http://localhost:8000/collections/');
                setCollections(response.data.results);
                setNextPage(response.data.next); // Store the URL of the next page
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

    const loadMoreCollections = async () => {
        if (nextPage) {
            try {
                const response = await axios.get<{ results: Collection[]; next: string | null }>(nextPage);
                setCollections([...collections, ...response.data.results]);
                setNextPage(response.data.next); // Update the URL of the next page
            } catch (error) {
                console.error('Error fetching more collections:', error);
            }
        }
    };

    const loadMoreProducts = async (id: string) => {
        if (nextPage) {
            try {
                const response = await axios.get<{ results: Product[]; next: string | null }>(`/products/?collection=${id}&page=${nextPage}`);
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

                <Route path="/products" element={<CarouselBestseller products={products} />} />
                <Route path="*" element={<NotFound />} />
            </Route>
        </Routes>
    );
}

export default App;
