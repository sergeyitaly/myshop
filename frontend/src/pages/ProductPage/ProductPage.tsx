import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Product } from '../../models/entities';
import { ProductSlider } from '../../components/ProductSlider/ProductSlider';
import { ProductSection } from '../../components/ProductSection/ProductSection'; 
import { MainContainer } from './components/MainContainer';
import { useProduct } from '../../hooks/useProduct';
import { ROUTE } from '../../constants';
import { useGetAllProductsFromCollectionQuery, useGetCollectionByNameQuery } from '../../api/collectionSlice';
import { skipToken } from '@reduxjs/toolkit/query';
import { PreviewCard } from '../../components/Cards/PreviewCard/PreviewCard';
import styles from './ProductPage.module.scss';
import { useTranslation } from 'react-i18next';

const ProductPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { t } = useTranslation();  // Hook for translation

  const [allowClick, setAllowClick] = useState<boolean>(true);
  const { product, isLoading, isFetching } = useProduct(+id!);

  const { data: collection } = useGetCollectionByNameQuery(product?.collection ?? skipToken);
  const { data: productsData } = useGetAllProductsFromCollectionQuery(collection?.id ?? skipToken);

  if (isLoading) {
    return <div>{t('loading')}</div>;  // Localized 'Loading...' text
  }

  if (!product) {
    return <div>{t('product_not_found')}</div>;  // Localized 'Product not found' text
  }

  const handleClickSlide = (productItem: Product) => {
    if (allowClick) {
      navigate(`${ROUTE.PRODUCT}${productItem.id}`);
    }
  };

  return (
    <MainContainer isLoading={isFetching}>
      <ProductSection />
      <ProductSlider 
        title={t('also_from_this_collection')}  // Localized title
        onAllowClick={setAllowClick}
      >
        {productsData?.results.map((product) => (
          <PreviewCard
            className={styles.card}
            key={product.id}
            title={product.name}
            discount={product.discount}
            price={product.price}
            currency={product.currency}
            photoSrc={product.photo_url}
            previewSrc={product.photo_thumbnail_url}
            onClick={() => handleClickSlide(product)}
          />
        ))}
      </ProductSlider>
    </MainContainer>
  );
};

export default ProductPage;
