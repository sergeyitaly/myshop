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
}

const CollectionsPage: React.FC<Props> = ({ collections }) => {

    return (
        <div className={style.container}>
            <h1 className={style.title}> Колекції </h1>
            <div className={style.cardContainer}>
                {collections.map((collection) => (
                    <Link to={`/collections/${collection.id}`} key={collection.id} className={style.card}>
                        <div className={style.cardImage}>
                            <img src={collection.photo} alt={collection.name} style={{ maxWidth: '100%' }} />
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
