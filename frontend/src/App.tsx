import { useEffect, useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import { Layout } from './layout/Layout/Layout';
import CollectionsPage from './pages/CollectionPage/CollectionsPage';
import CollectionItemsPage from './pages/CollectionItem/CollectionItems';
import ProductPage from './pages/ProductPage/ProductPage';
import { Home } from './pages/home/home';
import { NotFound } from './pages/not-found/not-found';
import axios from 'axios';
import CarouselBestseller from './pages/CollectionPage/CarouselBestseller/CarouselBestseller';
import OrderPage from './pages/OrderPage/OrderPage';
import { Product } from './models/entities';

const apiBaseUrl = import.meta.env.VITE_LOCAL_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;

interface Collection {
  id: string;
  name: string;
  photo: string;
  category: string;
}


function App() {
  const [collections, setCollections] = useState<Collection[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);

  const loadCollectionsByPage = async (page: number) => {
    setCurrentPage(page);
    try {
      const response = await axios.get<{ results: Collection[]; count: number }>(
        `${apiBaseUrl}/api/collections/?page=${page}`
      );
      setCollections(response.data.results);
      const pages = Math.ceil(response.data.count / 9); // 9 collections per page
      setTotalPages(pages);
    } catch (error) {
      console.error('Error fetching collections:', error);
    }
  };

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get<{ results: Product[] }>(`${apiBaseUrl}/api/products/`);
        setProducts(response.data.results);
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    };

    loadCollectionsByPage(currentPage);
    fetchProducts();
  }, [apiBaseUrl, currentPage]);

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
              totalPages={totalPages}
            />
          }
        />
        <Route path="/collection/:id" element={<CollectionItemsPage/>}/>
        <Route path="/product/:id" element={<ProductPage />} />
        <Route path="/products" element={<CarouselBestseller products={products} />} />
        <Route path="/order" element={<OrderPage />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
