import React from 'react';
import style from './style.module.scss';

interface Collection {
    id: string;
    name: string;
    photo: string;
    category: string;
}

interface Props {
    collections: Collection[]; // Define the type of collections
    loadMoreCollections: () => void; // Function to load more collections
    hasNextPage: boolean; // Indicates if there is a next page
}

const CollectionsPage: React.FC<Props> = ({ collections, loadMoreCollections, hasNextPage }) => {
    return (
        <div className={style.container}>
            <h1 className={style.title}> Колекції </h1>
            <div className={style.cardContainer}>
                {collections.map(collection => (
                    <div key={collection.id} className={style.card}>
                        <div className={style.cardImage}>
                            <img src={collection.photo} alt={collection.name} style={{ maxWidth: '100%' }} />
                            <p className={style.name}>{collection.name}</p>
                            <p className={style.category}>{collection.category}</p>
                        </div>
                    </div>
                ))}
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