import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { apiBaseUrl } from '../../api/api';
import { Product } from '../../models/entities';
import { ProductSlider } from '../../components/ProductSlider/ProductSlider';
import axios from 'axios';
import { ProductSlide } from '../../components/Cards/ProductSlide/ProductSlide';
import { ProductInfoSection } from '../../components/ProductInfoSection/ProductInfoSection';
import { MainContainer } from './components/MainContainer';
import { useProduct } from '../../hooks/useProduct';
import { ROUTE } from '../../constants';


const ProductPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  

  const [products, setProducts] = useState<Product[]>([])

  

  const {product, isLoading, isFetching, variants, changeColor, changeSize} = useProduct(id)


  const [allowClick, setAllowClick] = useState<boolean>(true)
  

  useEffect(() => {
    getProducts()
  }, [])

  const getProducts = async () => {
    const products = await axios.get(`${apiBaseUrl}/api/products/`)
    setProducts(products.data.results);
  }




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
            products.map((product) => (
                <ProductSlide
                    key={product.id}   
                    product={product}
                    onClick={handleClickSlide}
                />
            ))
        }
      </ProductSlider>
    </MainContainer>
  );
};

export default ProductPage;
