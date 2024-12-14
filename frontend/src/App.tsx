import { useEffect, useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import { Layout } from './layout/Layout/Layout';
import CollectionsPage from './pages/CollectionPage/CollectionsPage';
import CollectionItemsPage from './pages/CollectionItem/CollectionItems';
import ProductPage from './pages/ProductPage/ProductPage';
import { Home } from './pages/home/home';
import { NotFound } from './pages/not-found/not-found';
import { OrderPage } from './pages/Order/OrderPage';
import { ThankPage } from './pages/ThankPage/ThankPage';
import { PaymentAndDeliveryPage } from './pages/PaymentAndDeliveryPage/PaymentAndDeliveryPage';
import { PrivacyPolicyPage } from './pages/PrivacyPolicyPage/PrivacyPolicyPage';
import { ReturnsRefundsPage } from './pages/ReturnsRefundsPage/ReturnsRefundsPage';
import { ROUTE } from './constants';
import { FilterPage } from './pages/FilterPage/FilterPage';
import { TestPage } from './pages/TestPage';
import { Contact } from "./pages/Contact/Contact";
import {ThankYouPage} from "./pages/Contact/ThankYouPage/ThankYouPage";
import { About } from './pages/About/About';
import { FeedbackPage } from './pages/Feedback/Feedback';
import { NewProductsPage } from './pages/NewProductsPage/NewProductsPage';
import { AllCollectionsPage } from './pages/AllCollectionsPage/AllCollectionsPage';
import { ProductsWithDiscountPage } from './pages/ProductsWithDiscountPage/ProductsWithDiscountPage';
import { ThankFeedbackPage } from './pages/Thank_for_feedback/ThankFeedbackPage';
import { NoConnectionPage } from './pages/no-connection/no-connection';

function App() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return (
    <Routes>
      <Route element={<Layout />}>

        {isOnline ? (
          <Route index element={<Home />} />
        ) : (
          <Route path="/no-connection" element={<NoConnectionPage />} />
        )}
        <Route path="/collections" element={<CollectionsPage />} />
        <Route path="/collection/:id" element={<CollectionItemsPage />} />
        <Route path="/product/:id" element={<ProductPage />} />
        <Route path="/order" element={<OrderPage />} />
        <Route path="/products" element={<FilterPage />} />
        <Route path="/test" element={<TestPage />} />
        <Route path={ROUTE.FEEDBACK} element={<FeedbackPage />} />
        <Route path={ROUTE.THANK_FOR_FEEDBACK} element={<ThankFeedbackPage />} />
        <Route path={ROUTE.ABOUT} element={<About />} />
        <Route path={ROUTE.THANK} element={<ThankPage />} />
        <Route path={ROUTE.CONTACTS} element={<Contact />} />
        <Route path={ROUTE.SENDCONTACTS} element={<ThankYouPage />} />
        <Route path={ROUTE.PAYMENT_DELIVERY} element={<PaymentAndDeliveryPage />} />
        <Route path={ROUTE.PRIVACY_POLICY} element={<PrivacyPolicyPage />} />
        <Route path={ROUTE.RETURNS_REFUNDS} element={<ReturnsRefundsPage />} />
        <Route path={ROUTE.NEW_ARRIVALS} element={<NewProductsPage />} />
        <Route path={ROUTE.ALL_COLLECTIONS} element={<AllCollectionsPage />} />
        <Route path={ROUTE.DISCOUNT} element={<ProductsWithDiscountPage />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
