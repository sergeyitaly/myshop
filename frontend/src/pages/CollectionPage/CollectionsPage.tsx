import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { Collection, Category } from '../../models/entities';
import { PreviewCard } from '../../components/Cards/PreviewCard/PreviewCard';
import { ROUTE, screens } from '../../constants';
import { useGetCollectionsByFilterQuery } from '../../api/collectionSlice';
import { NamedSection } from '../../components/NamedSection/NamedSection';
import { PreviewItemsContainer } from '../../components/containers/PreviewItemsContainer/PreviewItemsContainer';
import { Pagination } from '../../components/UI/Pagination/Pagination';
import styles from './style.module.scss';
import { MotionItem } from '../../components/MotionComponents/MotionItem';
import { useMediaQuery } from '@mui/material';

const CollectionsPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const isMobile = useMediaQuery(screens.maxMobile);
  const limit = isMobile ? 8 : 8; // Adjust limit based on screen size
  const navigate = useNavigate();
  const [currentPage, setCurrentPage] = useState<number>(1);

  // Fetch collections
  const {
    data: collectionsData,
    isLoading,
    isFetching,
    refetch: refetchCollections
  } = useGetCollectionsByFilterQuery(
    { page_size: limit, page: currentPage },
    { refetchOnMountOrArgChange: true }
  );

  useEffect(() => {
    refetchCollections();
  }, [i18n.language, currentPage, refetchCollections]);

  // Memoize functions to avoid recalculations
  const getTranslatedCollectionName = useCallback((collection: Collection): string => {
    return i18n.language === 'uk' ? collection.name_uk || collection.name : collection.name_en || collection.name;
  }, [i18n.language]);

  const getTranslatedCategoryName = useCallback((category: Category | undefined): string => {
    return i18n.language === 'uk'
      ? category?.name_uk || category?.name || ''
      : category?.name_en || category?.name || '';
  }, [i18n.language]);

  const handleClickCollectionCard = useCallback((id: number) => {
    navigate(`${ROUTE.COLLECTION}${id}`);
  }, [navigate]);

  const totalPages = collectionsData ? Math.ceil(collectionsData.count / limit) : 0;

  const handleChangePage = (page: number) => {
    setCurrentPage(page);
  };

  return (
    <main>
      <NamedSection title={t('collections')}>
        <PreviewItemsContainer isLoading={isLoading} itemsQtyWhenLoading={limit}>
          {collectionsData?.results.map((collection, i) => (
            <MotionItem key={collection.id} index={i}>
              <PreviewCard
                photoSrc={collection.photo_url}
                previewSrc={collection.photo_thumbnail_url}
                title={getTranslatedCollectionName(collection)}
                loading={isFetching}
                subTitle={getTranslatedCategoryName(collection.category)}
                onClick={() => handleClickCollectionCard(collection.id)}
              />
            </MotionItem>
          ))}
        </PreviewItemsContainer>
        {collectionsData && totalPages > 1 && (
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
