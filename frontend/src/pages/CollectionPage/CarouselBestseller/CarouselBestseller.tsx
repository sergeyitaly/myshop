import React from "react";
import Slider, { Settings } from "react-slick";
import style from "./style.module.scss";
import { Product } from "../../../models/entities";
import { useGetAllProductsQuery } from "../../../api/productSlice";
import { PreviewCard } from "../../../components/Cards/PreviewCard/PreviewCard";

const CarouselBestseller: React.FC = () => {
  // Carousel settings
  const settings: Settings = {
    className: style.list,
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    initialSlide: 0,
    arrows: false,
    responsive: [
      {
        breakpoint: 700,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
          initialSlide: 0,
        },
      },
    ],
  };

  // Provide default values for page and search
  const { data } = useGetAllProductsQuery({ page: 1 }); // or use appropriate values

  const products: Product[] = data?.results || [];

  return (
    <Slider {...settings}>
      {products.map((product) => (
        <PreviewCard
          className={style.item}
          key={product.id}
          photoSrc={product.photo || ''}
          previewSrc={product.photo_thumbnail_url}
          title={product.name}
          subTitle={product.price}
        />
      ))}
    </Slider>
  );
};

export default CarouselBestseller;
