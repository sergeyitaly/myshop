import React from "react";
import Slider, {Settings} from "react-slick";
import style from "./style.module.scss";
import { Product } from "../../../models/entities";
import { useGetAllProductsQuery } from "../../../api/productSlice";
import { PreviewCard } from "../../../components/Cards/PreviewCard/PreviewCard";

const CarouselBestseller: React.FC = () => {


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

  const {data} = useGetAllProductsQuery()

  const products: Product[] = data?.results || []


  return (
      <Slider {...settings}>
        {products.map((product) => (
          // <Link
          //   to={`/product/${product.id}`}
          //   key={product.id}
          //   className={style.card}
          // >
          //   <div className={style.card}>
          //     <div className={style.cardImage}>
          //       <img
          //         src={product.photo || defaultPhoto}
          //         alt={product.name}
          //         className={style.image}
          //         loading="lazy"
          //       />
          //       <p className={style.name}>{product.name}</p>
          //       <p className={style.price}>{product.price}</p>
          //     </div>
          //   </div>
          // </Link>
            <PreviewCard
                className={style.item}
                key={product.id}
                photoSrc={product.photo || ''}
                title={product.name}
                subTitle={product.price}
                // onClick={() => handleClickCollectionCard(collection.id)}
            />
        ))}
      </Slider>
  );
};

export default CarouselBestseller;
