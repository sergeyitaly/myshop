import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Collection } from '../../models/entities';
import { PreviewCard } from '../../components/Cards/PreviewCard/PreviewCard';
import { ROUTE } from '../../constants';
import { useGetCollectionsByFilterQuery } from '../../api/collectionSlice';
import { NamedSection } from '../../components/NamedSection/NamedSection';
import { PreviewItemsContainer } from '../../components/containers/PreviewItemsContainer/PreviewItemsContainer';
import { Pagination } from '../../components/UI/Pagination/Pagination';
import styles from './style.module.scss'


const CollectionsPage: React.FC = () => {

  const limit = 9


  const navigate = useNavigate()

  const [currentPage, setCurrentPage] = useState<number>(1)

  const {data, isLoading, isFetching} = useGetCollectionsByFilterQuery({page_size: limit, page: currentPage})

  const collections: Collection[] = data?.results || []

  const handleClickCollectionCard = (id: number) => {
    navigate(ROUTE.COLLECTION + id)
  }

  let totalPages = 0

  if(data){
    totalPages = Math.ceil(data.count / limit)
  }

  const handleChangePage = (page: number ) => {
    setCurrentPage(page)
  }
  
 
  return (
    <main>
        <NamedSection 
          title='Колекції'
        >
          <PreviewItemsContainer
            isLoading = {isLoading}
          >
              {
                collections.map((collection) => (
                  <PreviewCard
                      key={collection.id}
                      photoSrc={collection.photo}
                      title={collection.name}
                      loading={isFetching}
                      subTitle={collection.category}
                      onClick={() => handleClickCollectionCard(collection.id)}
                  />
                ))
              }
          </PreviewItemsContainer>
          {
            data && totalPages > 1 &&
            <Pagination
              className={styles.pagination}
              totalPages={totalPages}
              currentPage={currentPage}
              onChange = {handleChangePage}
            />
          }
        </NamedSection>
    </main>
  );
};

export default CollectionsPage;
