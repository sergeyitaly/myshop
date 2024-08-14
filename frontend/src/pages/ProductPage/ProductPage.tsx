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

// Function to get translated product name
const getTranslatedProductName = (product: Product, language: string): string => {
  return language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
};

const ProductPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();  // Hook for translation

  const [allowClick, setAllowClick] = useState<boolean>(true);
  const { product, isLoading, isFetching } = useProduct(+id!);
  // Assuming `product.collection` is of type `Collection`
  const collectionName = product?.collection?.name ?? skipToken;
  const { data: collection } = useGetCollectionByNameQuery(collectionName);

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
            title={getTranslatedProductName(product, i18n.language) || t('no_name')}  // Use translated name or fallback
            discount={product.discount}
            price={product.price}
            currency={product.currency}
            photoSrc={product.photo_url || ''}
            previewSrc={product.photo_thumbnail_url || ''}
            onClick={() => handleClickSlide(product)}
          />
        ))}
      </ProductSlider>
    </MainContainer>
  );
};

export default ProductPage;
