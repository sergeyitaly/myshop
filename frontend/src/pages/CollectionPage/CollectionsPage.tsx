import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import style from './style.module.scss';
import { Link } from 'react-router-dom';

interface Collection {
    id: string;
    name: string;
    photo: string;
    category: string;
}

interface Props {
    collections: Collection[];
}

const CollectionsPage: React.FC<Props> = ({ collections }) => {
    return (
        <div className={style.container}>
            <h1 className={style.title}> Колекції </h1>
            <div className={style.cardContainer}>
                {collections && collections.length > 0 ? (
                    collections.map((collection) => (
                        <Link to={`/collections/${collection.id}`} key={collection.id} className={style.card}>
                            <div className={style.cardImage}>
                                <img src={collection.photo} alt={collection.name} style={{ maxWidth: '100%' }} />
                                <p className={style.name}>{collection.name}</p>
                                <p className={style.category}>{collection.category}</p>
                            </div>
                        </Link>
                    ))
                ) : (
                    collections ? (
                        <p>No collections available</p>
                    ) : null
                )}
            </div>
            {hasNextPage && (
                <div className={style.loadMore}>
                    <button onClick={loadMoreCollections}>Load More</button>
                </div>
            )}
        </div>
    );
};

export default CollectionsPage;
