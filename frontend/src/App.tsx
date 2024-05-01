import React, { useState, useEffect } from 'react';
import { Route, Routes } from 'react-router-dom';
import { Layout } from './layout/Layout/Layout';
import CollectionsPage from './pages/CollectionPage/CollectionsPage';
import { Home } from './pages/home/home';
import { NotFound } from './pages/not-found/not-found';
import axios from 'axios';
import CarouselBestseller from './pages/CollectionPage/CarouselBestseller/CarouselBestseller';
import CollectionItemsPage from './pages/CollectionItem/CollectionItems';

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
        const fetchData = async () => {
            try {
                const collectionsResponse = await axios.get<{ results: Collection[]; next: string | null }>('http://localhost:8000/collections/');
                setCollections(collectionsResponse.data.results);
                setNextPage(collectionsResponse.data.next); // Store the URL of the next page

                const productsResponse = await axios.get<Product[]>('http://localhost:8000/products/');
                setProducts(productsResponse.data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    const loadMoreData = async (url: string, setter: React.Dispatch<React.SetStateAction<any[]>>) => {
        if (nextPage) {
            try {
                const response = await axios.get<{ results: any[]; next: string | null }>(url);
                setter(prevData => [...prevData, ...response.data.results]);
                setNextPage(response.data.next); // Update the URL of the next page
            } catch (error) {
                console.error('Error fetching more data:', error);
            }
        }
    };

    const loadMoreCollections = () => loadMoreData(nextPage!, setCollections);

    const loadMoreProducts = (id: string) => loadMoreData(`/products/?collection=${id}&page=${nextPage}`, setProducts);

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
