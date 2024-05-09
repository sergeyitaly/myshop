import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; // Import useNavigate
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
    products: Product[];
    loadMoreProducts: (id: string) => void;
}

const CollectionItemsPage: React.FC<CollectionItemsPageProps> = ({ products, loadMoreProducts }) => {
    const { id } = useParams<{ id?: string }>(); // Provide a default value or make id optional
    const [collection, setCollection] = useState<Collection | null>(null);
    const navigate = useNavigate(); // Initialize navigate

    useEffect(() => {
        const fetchCollection = async () => {
            try {
                if (id) { // Check if id is not undefined
                    const response = await axios.get<Collection>(`/collections/${id}`);
                    setCollection(response.data);
                }
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
            {/* Load more button */}
            <button onClick={() => id && loadMoreProducts(id)}>Load More</button>
            {/* Navigate back to the main page when all pages are loaded */}
            {!id && <button onClick={() => navigate('/')}>Go back to main page</button>}
        </div>
    );
};

export default CollectionItemsPage;
