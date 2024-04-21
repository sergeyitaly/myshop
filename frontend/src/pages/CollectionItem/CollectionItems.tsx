import React from 'react';
import { useParams } from 'react-router-dom';
import style from './style.module.scss';
import Pagination from '@mui/material/Pagination';
import CarouselBestseller from '../CollectionPage/CarouselBestseller/CarouselBestseller';

interface Item {
    id: string;
    photo: string;
    name: string;
    price: string;
}

interface Collection {
    id: string;
    name: string;
    items: Item[];
}

const CollectionItemsPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();

    // Fetch the specific collection based on the id
    // You might need to pass collections array as props or fetch it from context
    const collections: Collection[] = []; // Fetch or get collections from props or context

    // Find the specific collection by id
    const collection = collections.find((collection) => collection.id === id);

    if (!collection) {
        return <div className={style.container}>Collection not found.</div>;
    }

    return (
        <div className={style.container}>
            <h1 className={style.title}>{collection.name}</h1>
            <div className={style.cardContainer}>
                {collection.items.map((product, index) => (
                    <div key={index} className={style.card}>
                        <div className={style.cardImage}>
                            <img src={product.photo} alt={product.name} style={{ maxWidth: '100%' }} />
                            <p className={style.name}>{product.name}</p>
                            <p className={style.price}>{product.price}</p>
                        </div>
                    </div>
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
