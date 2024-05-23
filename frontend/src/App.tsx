import { useState, useEffect } from 'react';
import { Route, Routes } from 'react-router-dom';
import { Layout } from './layout/Layout/Layout';
import CollectionsPage from './pages/CollectionPage/CollectionsPage';
import { Home } from './pages/home/home';
import { NotFound } from './pages/not-found/not-found';
import axios from 'axios';
import CarouselBestseller from './pages/CollectionPage/CarouselBestseller/CarouselBestseller';
import CollectionItemsPage from './pages/CollectionItem/CollectionItems';
import OrderPage from './pages/OrderPage/OrderPage';

const apiBaseUrl = import.meta.env.VITE_LOCAL_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;

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
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);

    useEffect(() => {
        const fetchCollections = async (page: number) => {
            try {
                const response = await axios.get<{ results: Collection[]; next: string | null; count: number }>(`${apiBaseUrl}/api/collections/?page=${page}`);
                setCollections(response.data.results);
                setTotalPages(Math.ceil(response.data.count / 6)); // Assuming 6 collections per page
            } catch (error) {
                console.error('Error fetching collections:', error);
            }
        };

        const fetchProducts = async () => {
            try {
                const response = await axios.get<{ results: Product[] }>(`${apiBaseUrl}/api/products/`);
                setProducts(response.data.results);
            } catch (error) {
                console.error('Error fetching products:', error);
            }
        };

        fetchCollections(currentPage);
        fetchProducts();
    }, [apiBaseUrl, currentPage]);

    const loadCollectionsByPage = (page: number) => {
        setCurrentPage(page);
    };

    return (
        <Routes>
            <Route element={<Layout withFooter withHeader />}>
                <Route index element={<Home />} />
                <Route
                    path="/collections"
                    element={
                        <CollectionsPage
                            collections={collections}
                            loadCollectionsByPage={loadCollectionsByPage}
                            hasNextPage={currentPage < totalPages}
                            totalPages={totalPages}
                        />
                    }
                />
                <Route
                    path="/collection/:id"
                    element={
                        <CollectionItemsPage
                            loadProductsByPage={(id, page) => axios.get(`${apiBaseUrl}/api/collection/${id}/products/?page=${page}`)}
                        />
                    }
                />
                <Route path="/products" element={<CarouselBestseller products={products} />} />
                <Route path="/order" element={<OrderPage />} />
                <Route path="*" element={<NotFound />} />
            </Route>
        </Routes>
    );
}

export default App;
