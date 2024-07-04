import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Collection } from '../../models/entities';
import { PreviewCard } from '../../components/Cards/PreviewCard/PreviewCard';
import { ROUTE } from '../../constants';
import { useGetAllCollectionsQuery } from '../../api/collectionSlice';
import { NamedSection } from '../../components/NamedSection/NamedSection';
import { PreviewItemsContainer } from '../../components/containers/PreviewItemsContainer/PreviewItemsContainer';


const CollectionsPage: React.FC = () => {

  const navigate = useNavigate()

  const {data, isLoading} = useGetAllCollectionsQuery()

  const collections: Collection[] = data?.results || []

  const handleClickCollectionCard = (id: number) => {
    navigate(ROUTE.COLLECTION + id)
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
                      subTitle={collection.category}
                      onClick={() => handleClickCollectionCard(collection.id)}
                  />
                ))
              }
          </PreviewItemsContainer>
        </NamedSection>
    </main>
  );
};

export default CollectionsPage;
