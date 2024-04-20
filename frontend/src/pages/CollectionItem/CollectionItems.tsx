// import React from 'react';
// import style from './style.module.scss';
// import Pagination from '@mui/material/Pagination';
//
// const CollectionItems: React.FC = ({ collection }) => {
//     return (
//         <div className={style.container}>
//             <h1 className={style.title}>{collection.name}</h1>
//             <div className={style.cardContainer}>
//                 {collection.items.map((product, index) => (
//                     <div key={index} className={style.card}>
//                         <div className={style.cardImage}>
//                             <img src={product.imageUrl} alt={product.name} style={{maxWidth:'100%'}} />
//                             <p className={style.name}>{product.name}</p>
//                             <p className={style.category}>{product.price}</p>
//                         </div>
//                     </div>
//                 ))}
//                 <Pagination count={3} />
//             </div>
//         </div>
//     );
// };
//
// export default CollectionItems;
// CollectionItemsPage.tsx
import { useParams } from "react-router-dom"; // импорт useParams для получения параметров маршрута
import style from "./style.module.scss";
import { fullData } from "../../components/Carousels/carouselMock";
import Pagination from "@mui/material/Pagination";
import CarouselBestseller from "../CollectionPage/CarouselBestseller/CarouselBestseller";
import { Link } from "react-router-dom";

const CollectionItemsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const collection = fullData.collections.find(
    (collection) => collection.id === id
  );

  if (!collection) {
    return <div> Коллекция не найдена </div>;
  }

  return (
    <div className={style.container}>
      <h1 className={style.title}>{collection.name}</h1>
      <div className={style.cardContainer}>
        {collection.items.map((product, index) => (
          <Link to={`/product/${id}`} key={index} className={style.card}>
            <div className={style.cardImage}>
              <img
                src={product.imageUrl}
                alt={product.name}
                style={{ maxWidth: "100%" }}
              />
              <p className={style.name}>{product.name}</p>
              <p className={style.price}>{product.price}</p>
            </div>
          </Link>
        ))}
      </div>
      <div className={style.pagination}>
        <Pagination count={5} />
      </div>
      <CarouselBestseller />
    </div>
  );
};

export default CollectionItemsPage;
