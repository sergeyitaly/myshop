import React from 'react';
import { useParams } from 'react-router-dom';
import { useGetOneCollectionByIdQuery } from '../../api/collectionSlice';
import { skipToken } from '@reduxjs/toolkit/query';
import style from './style.module.scss';
import { FilterSection } from '../../sections/FilterSection/FilterSection';
import { BestSellersSection } from '../../sections/BestSellersSection/BestSellersSection';


const CollectionItemsPage: React.FC = () => {

  const { id } = useParams<{ id: string }>();

  const {data: collection} = useGetOneCollectionByIdQuery(id ? +id : skipToken);

  return (
    <main className={style.main}>
      <FilterSection initialCollection={collection} />
      <BestSellersSection/>
    </main>
  );
};

export default CollectionItemsPage;
