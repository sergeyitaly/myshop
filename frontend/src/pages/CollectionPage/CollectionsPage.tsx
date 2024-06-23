import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import style from './style.module.scss';
import { Collection } from '../../models/entities';
import { PreviewCard } from '../../components/Cards/PreviewCard/PreviewCard';
import { PageContainer } from '../../components/PageContainer';
import { ROUTE } from '../../constants';



interface Props {
  collections: Collection[];
  loadCollectionsByPage: (page: number) => void;
  totalPages: number;
}

const CollectionsPage: React.FC<Props> = ({ collections = [], loadCollectionsByPage, totalPages }) => {
  const [currentPage, setCurrentPage] = useState(1);

  const navigate = useNavigate()

  useEffect(() => {
    loadCollectionsByPage(currentPage);
  }, [currentPage, loadCollectionsByPage]);

  const handlePageClick = (page: number) => {
    setCurrentPage(page);
  };

  const validTotalPages = isNaN(totalPages) || totalPages < 1 ? 1 : totalPages;

  const handleClickCollectionCard = (id: number) => {
    navigate(ROUTE.COLLECTION + id)
  }
 
  return (
    <main>
      <section>
        <PageContainer>
          <h1 className={style.title}>Колекції</h1>
          <div className={style.cardContainer}>
            {collections.map((collection) => (
              <PreviewCard
                  key={collection.id}
                  photoSrc={collection.photo}
                  title={collection.name}
                  subTitle={collection.category}
                  onClick={() => handleClickCollectionCard(collection.id)}
              />
            ))}
          </div>
          {collections.length > 9 && (
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
          )}
        </PageContainer>
      </section>
    </main>
  );
};

export default CollectionsPage;
