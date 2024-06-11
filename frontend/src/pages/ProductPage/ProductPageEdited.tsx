import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import style from './ProductPage.module.scss';
import { getProductNameById } from '../../api/api';
import { useSwipeable } from 'react-swipeable'; // Import useSwipeable hook
import { Product } from '../../models/entities';

// interface ProductImage {
//   id: string;
//   images: string; // Assuming 'images' property contains image URLs
// }

// interface Product {
//   id: string;
//   name: string;
//   photo: string;
//   price: number | string;
//   description: string;
//   images?: ProductImage[]; // Make images property optional
// }

const ProductPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [currentImageIndex, setCurrentImageIndex] = useState(0); // Track current image index

  useEffect(() => {
    const fetchData = async () => {
      try {
        const productData = await getProductNameById(id!);
        setProduct(productData);
      } catch (error) {
        console.error('Error fetching product:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const handleIncrement = () => {
    setQuantity((prevQuantity) => prevQuantity + 1);
  };

  const handleDecrement = () => {
    if (quantity > 1) {
      setQuantity((prevQuantity) => prevQuantity - 1);
    }
  };

  const handlers = useSwipeable({
    onSwipedLeft: () => {
      // Handle swipe left (move to next image)
      if (product && product.images && product.images.length > 0) {
        setCurrentImageIndex((prevIndex) =>
          prevIndex === product.images!.length - 1 ? 0 : prevIndex + 1
        );
      }
    },
    onSwipedRight: () => {
      // Handle swipe right (move to previous image)
      if (product && product.images && product.images.length > 0) {
        setCurrentImageIndex((prevIndex) =>
          prevIndex === 0 ? product.images!.length - 1 : prevIndex - 1
        );
      }
    }
  });

  if (loading) {
    return <div className={style.container}>Loading...</div>;
  }

  if (!product) {
    return <div className={style.container}>Product not found.</div>;
  }

  return (
    <div className={style.container}>
      <div className={style.leftSection}>
        <div className={style.imageContainer} {...handlers}>
          <img src={product.photo} alt={product.name} className={style.image} />
        </div>
        {product.images && product.images.length > 0 && (
          <div className={style.imageGallery}>
            {product.images.map((image, index) => (
              <div
                key={image.id}
                className={`${style.imageContainer} ${
                  index === currentImageIndex ? style.active : ''
                }`}
              >
                <img
                  src={image.images}
                  alt={product.name}
                  className={style.image}
                />
              </div>
            ))}
          </div>
        )}
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
