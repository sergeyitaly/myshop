import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import style from './style.module.scss';

interface Collection {
  id: string;
  name: string;
  photo: string;
  category: string;
}

interface Props {
  collections: Collection[];
  loadCollectionsByPage: (page: number) => void;
  totalPages: number;
}

const CollectionsPage: React.FC<Props> = ({ collections = [], loadCollectionsByPage, totalPages }) => {
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    loadCollectionsByPage(currentPage);
  }, [currentPage, loadCollectionsByPage]);

  const handlePageClick = (page: number) => {
    setCurrentPage(page);
  };

  const validTotalPages = isNaN(totalPages) || totalPages < 1 ? 1 : totalPages;

  return (
    <div>
      <div className={style.container}>
        <h1 className={style.title}>Колекції</h1>
        <div className={style.cardContainer}>
          {collections.map((collection) => (
            <Link
              to={`/collection/${collection.id}`}
              key={collection.id}
              className={style.card}
            >
              <div className={style.cardImage}>
                <img
                  src={collection.photo}
                  alt={collection.name}
                  style={{ maxWidth: '100%' }}
                  loading="lazy"
                />
                <p className={style.name}>{collection.name}</p>
                <p className={style.category}>{collection.category}</p>
              </div>
            </Link>
          ))}
        </div>
        <div className={style.pagination}>
          {[...Array(validTotalPages)].map((_, index) => (
            <button
              key={index + 1}
              onClick={() => handlePageClick(index + 1)}
              className={currentPage === index + 1 ? style.activePage : ''}
            >
              {index + 1}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CollectionsPage;
