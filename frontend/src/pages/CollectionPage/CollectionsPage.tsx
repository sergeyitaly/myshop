import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import style from './style.module.scss';

interface Collection {
    id: string;
    name: string;
    photo: string;
    category: string;
}

interface Props {
    collections: Collection[];
    loadMoreCollections: () => void;
    hasNextPage: boolean;
}

const CollectionsPage: React.FC<Props> = ({ collections, loadMoreCollections, hasNextPage }) => {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(false); // Simulate loading time, replace with actual fetching logic
    }, []);

    useEffect(() => {
        const handleScroll = () => {
            if (
                window.innerHeight + document.documentElement.scrollTop === document.documentElement.offsetHeight
            ) {
                loadMoreCollections();
            }
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, [loadMoreCollections]);

    return (
        <div className={style.container}>
            <h1 className={style.title}> Колекції </h1>
            <div className={style.cardContainer}>
                {collections.map((collection) => (
                    <Link to={`/collection/${collection.id}`} key={collection.id} className={style.card}>
                        <div className={style.cardImage}>
                            <img src={collection.photo} alt={collection.name} style={{ maxWidth: '100%' }} />
                            <p className={style.name}>{collection.name}</p>
                            <p className={style.category}>{collection.category}</p>
                        </div>
                    </Link>
                ))}
            </div>
            {loading && <div className={style.loading}>Loading...</div>}
            {hasNextPage && (
                <div className={style.loadMore}>
                    <button onClick={loadMoreCollections}>Load More</button>
                </div>
            )}
        </div>
    );
};

export default CollectionsPage;
