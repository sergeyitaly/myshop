import React, { useState } from 'react';
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
import { useTranslation } from 'react-i18next'; // Import useTranslation hook

const CollectionsPage: React.FC = () => {
  const { t } = useTranslation(); // Use the useTranslation hook

  const isMobile = useMediaQuery(screens.maxMobile);
  const limit = isMobile ? 8 : 8;
  const navigate = useNavigate();
  const [currentPage, setCurrentPage] = useState<number>(1);
  
  // Fetch collections with current page and limit
  const { data, isLoading, isFetching } = useGetCollectionsByFilterQuery({ page_size: limit, page: currentPage });
  const collections: Collection[] = data?.results || [];
  let totalPages = 0;

  if (data) {
    totalPages = Math.ceil(data.count / limit);
  }

  const handleClickCollectionCard = (id: number) => {
    navigate(ROUTE.COLLECTION + id);
  };

  const handleChangePage = (page: number) => {
    setCurrentPage(page);
  };

  return (
    <main>
      <NamedSection title={t('collections')}>
        <PreviewItemsContainer isLoading={isLoading} itemsQtyWhenLoading={limit}>
          {collections.map((collection, i) => (
            <MotionItem key={collection.id} index={i}>
              <PreviewCard
                photoSrc={collection.photo_url}
                previewSrc={collection.photo_thumbnail_url}
                title={collection.name} // This will be localized if backend returns localized name
                loading={isFetching}
                subTitle={`${t('category')}: ${collection.category}`} // Ensure backend returns localized category if needed
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
