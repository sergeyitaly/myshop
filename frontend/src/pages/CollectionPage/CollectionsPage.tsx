import React from 'react';
import { useNavigate } from 'react-router-dom';
import style from './style.module.scss';
import { Collection } from '../../models/entities';
import { PreviewCard } from '../../components/Cards/PreviewCard/PreviewCard';
import { PageContainer } from '../../components/PageContainer';
import { ROUTE } from '../../constants';
import { useGetAllCollectionsQuery } from '../../api/collectionSlice';





const CollectionsPage: React.FC = () => {


  const navigate = useNavigate()

  const {data} = useGetAllCollectionsQuery()

  const collections: Collection[] = data?.results || []

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
        </PageContainer>
      </section>
    </main>
  );
};

export default CollectionsPage;
