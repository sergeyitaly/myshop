import { Route, Routes } from 'react-router-dom';
import { Layout } from './layout/Layout/Layout';
import CollectionsPage from './pages/CollectionPage/CollectionsPage';
import CollectionItemsPage from './pages/CollectionItem/CollectionItems';
import ProductPage from './pages/ProductPage/ProductPage';
import { Home } from './pages/home/home';
import { NotFound } from './pages/not-found/not-found';
import { OrderPage } from './pages/Order/OrderPage';
import { ThankPage } from './pages/ThankPage/ThankPage';
import { ROUTE } from './constants';
import { FilterPage } from './pages/FilterPage/FilterPage';

function App() {


  return (
    <Routes>
      <Route element={<Layout withFooter withHeader />}>
        <Route index element={<Home />} />
        <Route path="/collections" element={<CollectionsPage/>}/>
        <Route path="/collection/:id" element={<CollectionItemsPage/>}/>
        <Route path="/product/:id" element={<ProductPage/>} />
        <Route path="/order" element={<OrderPage />} />
        <Route path="/products" element={<FilterPage />} />
        <Route path={ROUTE.THANK} element={<ThankPage />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
