import React from 'react';
import { useParams } from 'react-router-dom';
import { ProductSection } from '../../components/ProductSection/ProductSection'; 
import { MainContainer } from './components/MainContainer';
import { useProduct } from '../../hooks/useProduct';
import { useGetCollectionByNameQuery } from '../../api/collectionSlice';
import { skipToken } from '@reduxjs/toolkit/query';
import { useTranslation } from 'react-i18next';
import { FromThisCollectionSection } from '../../sections/FromThisCollectionSection/FromthisCollectionSection';



const ProductPage: React.FC = () => {

  const { id } = useParams<{ id: string }>();
  
  const { t } = useTranslation();  // Hook for translation

  const { product, isLoading, isFetching } = useProduct(+id!);
  // Assuming `product.collection` is of type `Collection`
  const collectionName = product?.collection?.name ?? skipToken;

  const { data: collection } = useGetCollectionByNameQuery(collectionName);


  if (isLoading) {
    return <div>{t('loading')}</div>;  // Localized 'Loading...' text
  }

  if (!product) {
    return <div>{t('product_not_found')}</div>;  // Localized 'Product not found' text
  }

  return (
    <MainContainer isLoading={isFetching}>
      <ProductSection />
      <FromThisCollectionSection
        collectionId={collection?.id}
      />
    </MainContainer>
  );
};

export default ProductPage;
