import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import style from './style.module.scss';
import { PreviewCard } from '../../components/Cards/PreviewCard/PreviewCard';
import { NamedSection } from '../../components/NamedSection/NamedSection';
import { AppCarousel } from '../../components/AppCarousel/AppCarousel';
import { useGetAllProductsFromCollectionQuery, useGetOneCollectionByIdQuery } from '../../api/collectionSlice';
import { skipToken } from '@reduxjs/toolkit/query';
import { PreviewItemsContainer } from '../../components/containers/PreviewItemsContainer/PreviewItemsContainer';
import { ROUTE } from '../../constants';
import { formatNumber } from '../../functions/formatNumber';
import { formatCurrency } from '../../functions/formatCurrency';

const CollectionItemsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate()

  const {
    data:collection, 
    isSuccess, 
    isLoading: isLoadingCollection
  } = useGetOneCollectionByIdQuery( id ? +id : skipToken)

  const {
     data: productResponce,
     isSuccess: isSuccessProductFetshing,
     isLoading: isLoadingProducts,
     isError: isErrorProducts,
     error
  } = useGetAllProductsFromCollectionQuery( id ? +id : skipToken )

  console.log(error);
  

  const products = isSuccessProductFetshing ? productResponce.results : []
  
  const handleClickProduct = (productId: number) => {
    navigate(`${ROUTE.PRODUCT}${productId}`)
  }

  return (
    <main className={style.main}>
      {
        <NamedSection 
          title={isSuccess ? collection.name : ''}
          isLoading = {isLoadingCollection}
        >
            <PreviewItemsContainer
              isLoading={isLoadingProducts}
              isError = {isErrorProducts}
              textWhenEmpty='Ця колекція поки що не має продуктів'
              textWhenError='Помилка!'
            >
              {
                products.map((product) => (
                  <PreviewCard
                      key={product.id}
                      photoSrc={product.photo || ''}
                      title={product.name}
                      subTitle={`${formatNumber(product.price)} ${formatCurrency(product.currency)}`}
                      onClick={() => handleClickProduct(product.id)}
                  />
                ))
              }
            </PreviewItemsContainer>
          </NamedSection>
      }
        <NamedSection title='Бестселери'>
          <AppCarousel>
            {
              products.map((product) => (
                <PreviewCard
                      className={style.item}
                      key={product.id}
                      photoSrc={product.photo || ''}
                      title={product.name}
                      subTitle={`${formatNumber(product.price)} ${formatCurrency(product.currency)}`}
                      onClick={() => handleClickProduct(product.id)}
                  />
              ))
            }
          </AppCarousel>
        </NamedSection>
    </main>
  );
};

export default CollectionItemsPage;
