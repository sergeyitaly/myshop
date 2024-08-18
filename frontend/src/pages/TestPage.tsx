import { Swiper, SwiperSlide } from 'swiper/react';
import { useGetAllProductsQuery, useGetManyProductsByFilterQuery } from '../api/productSlice';
import { PreviewCard } from '../components/Cards/PreviewCard/PreviewCard';
import styles from './Test.module.scss'

import 'swiper/css/bundle';
import './styles.css'

import { Grid, Pagination } from 'swiper/modules';

export const TestPage = () => {

    const {data} = useGetManyProductsByFilterQuery({
        page_size: 1
    })

    console.log(data);

    
    return (
        <div>
            <Swiper
             slidesPerView={3}
             grid={{
               rows: 2,
               fill: 'row'
             }}
             spaceBetween={20}
             pagination={{
               clickable: true,
             }}
             modules={[Grid, Pagination]}
            >
                {
                    data?.results.map(({id, photo_url, photo_thumbnail_url, price, discount, name, collection}) => {
                        return (
                            <SwiperSlide
                                key={id}
                            >
                                <PreviewCard
                                    className={styles.card}
                                    photoSrc={photo_url}
                                    previewSrc={photo_thumbnail_url}
                                    title={name}
                                    subTitle={collection?.name}
                                    discount={discount}
                                    price={price}
                                    currency={'UAH'}
                                />
                            </SwiperSlide>
                        )
                    })
                }
            </Swiper>
        </div>
    )
}