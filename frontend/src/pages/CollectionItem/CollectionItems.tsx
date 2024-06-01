import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import style from './style.module.scss';
import CarouselBestseller from '../CollectionPage/CarouselBestseller/CarouselBestseller';
import { AxiosResponse } from 'axios';
import { getCollectionNameById } from '../../api/api';

interface Collection {
  id: string;
  name: string;
  photo: string;
  category: string;
}

interface Product {
  id: string;
  name: string;
  photo: string;
  price: number | string;
}

interface CollectionItemsPageProps {
  loadProductsByPage: (id: string, page: number) => Promise<AxiosResponse<any>>;
}

const CollectionItemsPage: React.FC<CollectionItemsPageProps> = ({ loadProductsByPage }) => {
  const { id } = useParams<{ id: string }>();
  const [collection, setCollection] = useState<Collection | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    const fetchData = async (page: number) => {
      try {
        setLoading(true);

        if (!collection) {
          const collectionData = await getCollectionNameById(id!);
          setCollection(collectionData);
        }

        const { data: { results, count } } = await loadProductsByPage(id!, page);
        setProducts(results);
        setTotalPages(Math.ceil(count / 6));
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData(currentPage);
  }, [id, loadProductsByPage, currentPage, collection]);

  const handlePageClick = (page: number) => {
    setCurrentPage(page);
  };

  if (loading) {
    return <div className={style.container}>Loading...</div>;
  }

  if (!collection) {
    return <div className={style.container}>Collection does not exist.</div>;
  }

  return (
    <>
      <h1 className={style.title}>{collection.name}</h1>
      {products.length === 0 ? (
        <div className={style.container}>
          <p>This collection has no products.</p>
        </div>
      ) : (
        <div className={style.productContainer}>
          {products.map((product) => (
            <Link
              to={`/product/${product.id}`}
              key={product.id}
              className={style.card}
            >
              <div className={style.cardImage}>
                <img
                  src={product.photo}
                  alt={product.name}
                  style={{ maxWidth: '100%', height: 'auto', display: 'block' }}
                  loading="lazy"
                />
              </div>
              <div className={style.cardContent}>
                <p className={style.name}>{product.name}</p>
                <p className={style.price}>{product.price}</p>
              </div>
            </Link>
          ))}
        </div>
      )}
      <div className={style.pagination}>
        {[...Array(totalPages)].map((_, index) => (
          <button
            key={index + 1}
            onClick={() => handlePageClick(index + 1)}
            className={currentPage === index + 1 ? style.activePage : ''}
          >
            {index + 1}
          </button>
        ))}
      </div>
      <CarouselBestseller products={products.map(product => ({ ...product, price: String(product.price) }))} />
    </>
  );
};

export default CollectionItemsPage;
