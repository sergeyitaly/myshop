import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import style from './style.module.scss';
import CarouselBestseller from '../CollectionPage/CarouselBestseller/CarouselBestseller';
import axios from 'axios';

interface Product {
    id: string;
    name: string;
    price: string;
    photo: string;
}

interface Collection {
    id: string;
    name: string;
    photo: string;
    category: string;
}

interface CollectionItemsPageProps {
    collections: Collection[];
    products: Product[];
}

const CollectionItemsPage: React.FC<CollectionItemsPageProps> = ({ products }) => {
    const { id } = useParams<{ id: string }>();
    const [collection, setCollection] = useState<any>(null); // Change type as needed

    useEffect(() => {
        const fetchCollection = async () => {
            try {
                const response = await axios.get(`/collections/${id}`);
                setCollection(response.data);
            } catch (error) {
                console.error('Error fetching collection:', error);
            }
        };
        fetchCollection();
    }, [id]);

    if (!collection) {
        return <div className={style.container}>Collection not found.</div>;
    }

    return (
        <div className={style.container}>
            <h1 className={style.title}>{collection.name}</h1>
            {/* Render collection items here */}
            {products.map((product) => (
                <div key={product.id} className={style.card}>
                    <div className={style.cardImage}>
                        <img src={product.photo} alt={product.name} style={{ maxWidth: '100%' }} />
                        <p className={style.name}>{product.name}</p>
                        <p className={style.price}>{product.price}</p>
                    </div>
                </div>
            ))}
            {/* Render CarouselBestseller component */}
            <CarouselBestseller products={products} />
        </div>
    );
};

export default CollectionItemsPage;
