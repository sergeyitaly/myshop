import React from 'react';
import { Link } from 'react-router-dom';
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
                    // Display "No collections available" only if collections are loaded and empty
                    collections ? (
                        <p>No collections available</p>
                    ) : null // Do not display anything if collections are still being loaded
                )}
            </div>
            {/* Render "Load More" button only if there are more pages to load */}
            {hasNextPage && (
                <div className={style.loadMore}>
                    <button onClick={loadMoreCollections}>Load More</button>
                </div>
            )}
        </div>
    );
};

export default CollectionsPage;
