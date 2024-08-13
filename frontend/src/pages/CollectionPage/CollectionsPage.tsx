import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Collection } from '../../models/entities';
import { PreviewCard } from '../../components/Cards/PreviewCard/PreviewCard';
import { ROUTE, screens } from '../../constants';
import { useGetCollectionsByFilterQuery } from '../../api/collectionSlice';
import { NamedSection } from '../../components/NamedSection/NamedSection';
import { PreviewItemsContainer } from '../../components/containers/PreviewItemsContainer/PreviewItemsContainer';
import { Pagination } from '../../components/UI/Pagination/Pagination';
import styles from './style.module.scss';
import { MotionItem } from '../../components/MotionComponents/MotionItem';
import { useMediaQuery } from '@mui/material';
import { useTranslation } from 'react-i18next'; // Import useTranslation for translations

const CollectionsPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const isMobile = useMediaQuery(screens.maxMobile);
  const limit = isMobile ? 8 : 8;
  const navigate = useNavigate();
  const [currentPage, setCurrentPage] = useState<number>(1);
  const { data, isLoading, isFetching, refetch } = useGetCollectionsByFilterQuery({ page_size: limit, page: currentPage }, { refetchOnMountOrArgChange: true });

  // Re-fetch data when language changes
  useEffect(() => {
    refetch(); // Refetch data to get translated fields
  }, [i18n.language, refetch]);

  const collections: Collection[] = data?.results || [];

  const handleClickCollectionCard = (id: number) => {
    navigate(ROUTE.COLLECTION + id);
  };

  const totalPages = data ? Math.ceil(data.count / limit) : 0;

  const handleChangePage = (page: number) => {
    setCurrentPage(page);
  };

  return (
    <main>
      <NamedSection title={t('collections')}>
        <PreviewItemsContainer
          isLoading={isLoading}
          itemsQtyWhenLoading={limit}
        >
          {collections.map((collection, i) => (
            <MotionItem key={collection.id} index={i}>
              <PreviewCard
                photoSrc={collection.photo_url}
                previewSrc={collection.photo_thumbnail_url}
                title={collection.name} // Use translated collection name from the database
                loading={isFetching}
                subTitle={t(collection.category)} // Use translated category name from the database
                onClick={() => handleClickCollectionCard(collection.id)}
              />
            </MotionItem>
          ))}
        </PreviewItemsContainer>
        {data && totalPages > 1 && (
          <Pagination
            className={styles.pagination}
            totalPages={totalPages}
            currentPage={currentPage}
            onChange={handleChangePage}
          />
        )}
      </NamedSection>
    </main>
  );
};

export default CollectionsPage;
