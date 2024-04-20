import { Route, Routes } from "react-router-dom";
import { Layout } from "./layout/Layout/Layout";
import CollectionItemsPage from "./pages/CollectionItem/CollectionItems";
import CollectionsPage from "./pages/CollectionPage/CollectionsPage";
import { Home } from "./pages/home/home";
import { NotFound } from "./pages/not-found/not-found";
import ProductPage from "./pages/ProductPage/ProductPage";

function App() {
  return (
    <>
      <Routes>
        <Route element={<Layout withFooter withHeader />}>
          <Route index element={<Home />} />
          <Route path="collections" element={<CollectionsPage />} />
          <Route path="/collections/:id" element={<CollectionItemsPage />} />
          <Route path="*" element={<NotFound />} />
        </Route>
        <Route path="product" element={<ProductPage />}></Route>
      </Routes>
    </>
  );
}

export default App;
