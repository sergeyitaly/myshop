import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PreviewCard } from '../../components/Cards/PreviewCard/PreviewCard';
import { NamedSection } from '../../components/NamedSection/NamedSection';
import { AppCarousel } from '../../components/AppCarousel/AppCarousel';
import { useGetOneCollectionByIdQuery, useGetProductsFromCollectionByProductFilterQuery } from '../../api/collectionSlice';
import { skipToken } from '@reduxjs/toolkit/query';
import { ROUTE } from '../../constants';
import { formatNumber } from '../../functions/formatNumber';
import { formatCurrency } from '../../functions/formatCurrency';
import style from './style.module.scss';
import { FilterSection } from '../../sections/FilterSection/FilterSection';



const CollectionItemsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate()

  const limit = 4


  const {
    data:collection, 
  } = useGetOneCollectionByIdQuery( id ? +id : skipToken)

  const {
     data: productResponce,
     isSuccess: isSuccessProductFetshing,
  } = useGetProductsFromCollectionByProductFilterQuery( collection ? 
    {collectionId: collection.id,
      page_size: limit,
    } 
    : skipToken )

  const products = isSuccessProductFetshing ? productResponce.results : []
  
  const handleClickProduct = (productId: number) => {
    navigate(`${ROUTE.PRODUCT}${productId}`)
  }


  

  

  return (
    <main className={style.main}>
        <FilterSection/>
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
