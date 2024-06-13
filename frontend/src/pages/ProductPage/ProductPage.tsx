import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Product } from '../../models/entities';
import { ProductSlider } from '../../components/ProductSlider/ProductSlider';
import { ProductSlide } from '../../components/Cards/ProductSlide/ProductSlide';
import { ProductInfoSection } from '../../components/ProductInfoSection/ProductInfoSection';
import { MainContainer } from './components/MainContainer';
import { useProduct } from '../../hooks/useProduct';
import { ROUTE } from '../../constants';
import { useGetAllProductsFromCollectionQuery, useGetCollectionByNameQuery } from '../../api/collectionSlice';
import { skipToken } from '@reduxjs/toolkit/query';


const ProductPage: React.FC = () => {

  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();


  const [allowClick, setAllowClick] = useState<boolean>(true)

  const {product, isLoading, isFetching, variants, changeColor, changeSize} = useProduct(+id!)

  const {data: collection} = useGetCollectionByNameQuery(product?.collection ?? skipToken)

  const {data: productsData} = useGetAllProductsFromCollectionQuery(collection?.id ?? skipToken)
  

  if (isLoading) {
    return <div >Loading...</div>;
  }

  if (!product) {
    return <div >Product not found.</div>;
  }

  const handleClickSlide = (productItem: Product) => {
    allowClick &&
    navigate(`${ROUTE.PRODUCT}${productItem.id}`)
  }


  return (
    <MainContainer
      isLoading = {isFetching}
    >
      <ProductInfoSection
        product={product}
        productVariants={variants}
        onChangeColor={changeColor}
        onChangeSize={changeSize}
      />
      <ProductSlider 
         title='Також з цієї колекції'
         onAllowClick={setAllowClick}
       >
         {
           productsData?.results.map((product) => (
               <ProductSlide
                   key={product.id}   
                   product={product}
                   onClick={handleClickSlide}
               />
           ))
         }
       </ProductSlider>
    </MainContainer>
    
  )
}

export default ProductPage;
