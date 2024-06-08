import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { apiBaseUrl, getProductNameById } from '../../api/api';
import { useSwipeable } from 'react-swipeable'; // Import useSwipeable hook
import { Product, ProductColorModel } from '../../models/entities';
import { ProductControl } from '../../components/ProductControl/ProductControl';
import { DropDown } from '../../components/DropDown/DropDown';
import { ProductSlider } from '../../components/ProductSlider/ProductSlider';
import axios from 'axios';
import style from './ProductPage.module.scss';
import { ProductSlide } from '../../components/Cards/ProductSlide/ProductSlide';



const productColors: ProductColorModel[] = [
  {
    productId: 10,
    name: 'Позолота',
    color: '#E0B139'
  },
  {
    productId: 10,
    name: 'Сірий',
    color: '#D9D9D9'
  },
]

const ProductPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);

  const [products, setProducts] = useState<Product[]>([])

  console.log(product);

  
  
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


  useEffect(() => {
    getProducts()
  }, [])

  const getProducts = async () => {
    const products = await axios.get(`${apiBaseUrl}/api/products/`)
    setProducts(products.data.results);
  }

  const handleIncrement = () => {
    setQuantity((prevQuantity) => prevQuantity + 1);
  };

  const handleDecrement = () => {
    if (quantity > 0) {
      setQuantity((prevQuantity) => prevQuantity - 1);
    }
  };

  const handlers = useSwipeable({
    onSwipedLeft: () => {
      // Handle swipe left
    },
    onSwipedRight: () => {
      // Handle swipe right
    }
  });

  if (loading) {
    return <div className={style.container}>Loading...</div>;
  }

  if (!product) {
    return <div className={style.container}>Product not found.</div>;
  }


  return (
    <main className={style.main}>
      <section className={style.section}>
        <div className={style.imageList}>
          {
            product.images?.map((image) => (
              <div className={style.previevBox}>
                <img src={product.photo}/>
              </div>
            ))
          }
        </div>
        <div className={style.imageBox}>
          <img 
            className={style.image}
            src={product.photo}
          />
        </div>
        <div className={style.productInfo}>
          <ProductControl 
            product={product}
            colors={productColors}
            sizes={['30', '40']}
          />
          <div className={style.description}>
            <h3>Опис:</h3>
            <p>{product.description ? product.description : 'опис товару поки що відсутній'}</p>
          </div>
        </div>

          <DropDown
            className={style.applyDropdown}
            title='Застосування:'
            content='Підходить для повсякденного носіння, а також стане чудовим доповненням до вечірнього або урочистого вбрання.'
          />
          <DropDown
            className={style.careDropdown}
            title='Догляд:'
            content="Чистка: Використовуйте м'яку тканину або спеціалізований розчин для чищення срібла. Не використовуйте абразивні засоби, оскільки вони можуть пошкодити покриття.

            Зберігання: Зберігайте кольє окремо від інших ювелірних виробів, щоб уникнути подряпин. Використовуйте м'яку тканинну сумочку або коробку з м'яким покриттям.
            Уникайте контакту з хімікатами: Не допускайте контакту кольє з парфумами, косметикою, миючими засобами та іншими хімікатами, які можуть пошкодити позолоту.

            Носіння: Намагайтеся надягати кольє після того, як ви нанесли косметику та парфуми, та знімати перед купанням, спортом або сном.
            Дотримуючись цих рекомендацій, ви зможете довше зберігати красу та блиск вашого кольє з срібла з позолотою."
          />
      </section>
      <ProductSlider 
        title='Також з цієї колекції'
      >
         {
            products.map((product) => (
                <ProductSlide
                    key={product.id}   
                    product={product}
                />
            ))
        }
      </ProductSlider>
  </main>
  );
};

export default ProductPage;