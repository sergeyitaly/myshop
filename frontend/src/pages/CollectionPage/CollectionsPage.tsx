import { Link } from 'react-router-dom';
import style from './style.module.scss';
import { fullData } from "../../components/Carousels/carouselMock";

const CollectionsPage: React.FC = () => {
    return (
        <div className={style.container}>
            <h1 className={style.title}> Колекції </h1>
            <div className={style.cardContainer}>
                {fullData.collections.map((collection) => (
                    <Link to={`/collections/${collection.id}`} key={collection.id} className={style.card}>
                        <div className={style.cardImage}>
                            <img src={collection.imageUrl} alt={collection.name} style={{maxWidth:'100%'}} />
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
