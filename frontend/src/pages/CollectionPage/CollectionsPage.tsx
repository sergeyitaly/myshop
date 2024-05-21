
import React, { useEffect } from 'react';
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
    useEffect(() => {
        const handleScroll = (event: Event) => {
            const target = event.target as Window;
            if (target.innerHeight + target.document.documentElement.scrollTop === target.document.documentElement.offsetHeight) {
                loadMoreCollections();
            }
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, [loadMoreCollections]);

    return (
        <div className={style.container}>
            <h1 className={style.title}>Колекції</h1>
            <div className={style.cardContainer}>
                {collections.map((collection) => (
                    <Link to={`/collection/${collection.id}`} key={collection.id} className={style.card}>
                        <div className={style.cardImage}>
                            <img src={collection.photo} alt={collection.name} style={{ maxWidth: '100%' }} loading="lazy" />
                            <p className={style.name}>{collection.name}</p>
                            <p className={style.category}>{collection.category}</p>
                        </div>
                    </Link>
                ))}
            </div>
            {hasNextPage && (
                <div className={style.loadMore}>
                    <button onClick={loadMoreCollections}>Завантажити ще</button>
                </div>
            )}
        </div>
      )}
    </div>
  );
};

export default CollectionsPage;
