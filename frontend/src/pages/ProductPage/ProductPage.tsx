// ProductPage.tsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import style from './ProductPage.module.scss';

interface Product {
  id: string;
  name: string;
  photo: string;
  price: number | string;
  description: string;
}

const ProductPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1); // Initialize quantity to 1
  const apiBaseUrl = import.meta.env.VITE_LOCAL_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await axios.get<Product>(`${apiBaseUrl}/api/product/${id}/`);
        setProduct(response.data);
      } catch (error) {
        console.error('Error fetching product:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id, apiBaseUrl]);

  const handleIncrement = () => {
    setQuantity((prevQuantity) => prevQuantity + 1); // Increase quantity by 1
  };

  const handleDecrement = () => {
    if (quantity > 0) {
      setQuantity((prevQuantity) => prevQuantity - 1); // Decrease quantity by 1 if it's greater than 0
    }
  };

  if (loading) {
    return <div className={style.container}>Loading...</div>;
  }

  if (!product) {
    return <div className={style.container}>Product not found.</div>;
  }

  return (
    <div className={style.container}>
      <div className={style.leftSection}>
        <div className={style.imageContainer}>
          <img src={product.photo} alt={product.name} className={style.image} />
        </div>
        <h1 className={style.title}>{product.name}</h1>
      </div>
      <div className={style.rightSection}>
        <p className={style.description}>{product.description}</p>
        <div className={style.priceContainer}>
          <p className={style.price}>${product.price}</p>
          <div className={style.addToCart}>
            <button className={style.decrement} onClick={handleDecrement}>-</button>
            <input type="text" value={quantity} className={style.quantity} readOnly />
            <button className={style.increment} onClick={handleIncrement}>+</button>
            <button className={style.addToCartBtn}>Add to Cart</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductPage;
