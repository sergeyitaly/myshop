// CollectionsPage.tsx
import axios from 'axios';
import React, { useState, useEffect } from 'react';

import { Link } from 'react-router-dom';
import style from './style.module.scss';
//import { fullData } from "../../components/Carousels/carouselMock";

interface Collection {
    id: number;
    name: string;
    category: string;
    imageUrl: string;
}

const CollectionsPage: React.FC = () => {
    const [collections, setCollections] = useState<Collection[]>([]);

    useEffect(() => {
        const fetchCollections = async () => {
            try {
                const response = await axios.get('/api/collections/'); // Adjust endpoint URL
                setCollections(response.data);
            } catch (error) {
                console.error('Error fetching collections:', error);
            }
        };

        fetchCollections();
    }, []);

    return (
        <div className={style.container}>
            <h1 className={style.title}>Колекції</h1>
            <div className={style.cardContainer}>
                {collections.map((collection) => (
                    <Link to={`/collections/${collection.id}`} key={collection.id} className={style.card}>
                        <div className={style.cardImage}>
                            <img src={collection.imageUrl} alt={collection.name} style={{ maxWidth: '100%' }} />
                            <p className={style.name}>{collection.name}</p>
                            <p className={style.category}>{collection.category}</p>
                        </div>
                    </Link>
                ))}
            </div>
        </div>
    );
};

export default CollectionsPage;