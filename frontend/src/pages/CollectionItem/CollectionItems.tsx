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
import React from 'react';
import { useParams } from 'react-router-dom'; // импорт useParams для получения параметров маршрута
import style from './style.module.scss';
import { fullData } from "../../components/Carousels/carouselMock";

const CollectionItemsPage: React.FC = () => {

    const { id } = useParams<{ id: string }>();// изменение параметра маршрута на id
    console.log('ID коллекции из URL:', id);
    const collection = fullData.collections.find(collection => collection.id === id);
    console.log('Найденная коллекция:', collection);

    if (!collection) {
        return <div> Коллекция не найдена </div>
    }

    console.log('Товары коллекции:', collection.items);

    return (
        <div className={style.container}>
            <h1 className={style.title}>{collection.name}</h1>
            <div className={style.cardContainer}>
                {collection.items.length > 0 ? ( // Проверка наличия товаров в коллекции
                    collection.items.map((product, index) => (
                        <div key={index} className={style.card}>
                            <div className={style.cardImage}>
                                <img src={product.imageUrl} alt={product.name} style={{maxWidth:'100%'}} />
                                <p className={style.name}>{product.name}</p>
                                <p className={style.price}>{product.price}</p>
                            </div>
                        </div>
                    ))
                ) : (
                    <div>Товары отсутствуют</div> // Вывод сообщения, если товаров в коллекции нет
                )}
            </div>
        </div>
    );
};

export default CollectionItemsPage;
