import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PreviewCard } from '../../components/Cards/PreviewCard/PreviewCard';
import { NamedSection } from '../../components/NamedSection/NamedSection';
import { AppCarousel } from '../../components/AppCarousel/AppCarousel';
import { useGetOneCollectionByIdQuery, useGetProductsFromCollectionByProductFilterQuery } from '../../api/collectionSlice';
import { skipToken } from '@reduxjs/toolkit/query';
import { PreviewItemsContainer } from '../../components/containers/PreviewItemsContainer/PreviewItemsContainer';
import { ROUTE } from '../../constants';
import { formatNumber } from '../../functions/formatNumber';
import { formatCurrency } from '../../functions/formatCurrency';
import style from './style.module.scss';
import { Pagination } from '../../components/UI/Pagination/Pagination';

const CollectionItemsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate()

  const limit = 4

  const [currentPage, setCurrentPage] = useState<number>(1)

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
  } = useGetProductsFromCollectionByProductFilterQuery( collection ? 
    {collectionId: collection.id,
      page_size: limit,
      page: currentPage
    } 
    : skipToken )

  const products = isSuccessProductFetshing ? productResponce.results : []
  
  const handleClickProduct = (productId: number) => {
    navigate(`${ROUTE.PRODUCT}${productId}`)
  }



  let totalPages = 0

  if(productResponce){
    totalPages = Math.ceil(productResponce.count / limit)
  }

  const handleChangePage = (page: number ) => {
    setCurrentPage(page)
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
                      previewSrc={product.photo_thumbnail_url}
                      title={product.name}
                      price={product.price}
                      currency={product.currency}
                      discount={product.discount}
                      onClick={() => handleClickProduct(product.id)}
                  />
                ))
              }
            </PreviewItemsContainer>
            {
              productResponce && totalPages > 1 &&
              <Pagination
                className={style.pagination}
                totalPages={totalPages}
                currentPage={currentPage}
                onChange = {handleChangePage}
              />
            }
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
                      previewSrc={product.photo_thumbnail_url}
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
