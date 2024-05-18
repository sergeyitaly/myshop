import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
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

const CollectionItemsPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [collection, setCollection] = useState<Collection | null>(null);
    const [products, setProducts] = useState<Product[]>([]);
    const [nextPage, setNextPage] = useState<string | null>(null);
    const navigate = useNavigate();
    const apiBaseUrl = import.meta.env.VITE_LOCAL_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;

    useEffect(() => {
        const fetchCollection = async () => {
            try {
                if (id) {
                    const response = await axios.get<Collection>(`${apiBaseUrl}/collections/${id}/`);
                    setCollection(response.data);
                    fetchProducts(id);
                }
            } catch (error) {
                console.error('Error fetching collection:', error);
            }
        };

        const fetchProducts = async (collectionId: string) => {
            try {
                const response = await axios.get<{ results: Product[]; next: string | null }>(
                    `${apiBaseUrl}/collections/${collectionId}/products/`
                );
                setProducts(response.data.results);
                setNextPage(response.data.next);
            } catch (error) {
                console.error('Error fetching products:', error);
            }
        };

        fetchCollection();
    }, [id, apiBaseUrl]);

    const loadMoreProducts = async () => {
        if (nextPage) {
            try {
                const response = await axios.get<{ results: Product[]; next: string | null }>(nextPage);
                setProducts((prevProducts) => [...prevProducts, ...response.data.results]);
                setNextPage(response.data.next);
            } catch (error) {
                console.error('Error fetching more products:', error);
            }
        }
    };

    if (!collection) {
        return <div className={style.container}>Collection not found.</div>;
    }

    return (
        <div className={style.container}>
            <h1 className={style.title}>{collection.name}</h1>
            {products.map((product) => (
                <div key={product.id} className={style.card}>
                    <div className={style.cardImage}>
                        <img src={product.photo} alt={product.name} style={{ maxWidth: '100%' }} />
                        <p className={style.name}>{product.name}</p>
                        <p className={style.price}>{product.price}</p>
                    </div>
                </div>
            ))}
            <CarouselBestseller products={products} />
            <button onClick={loadMoreProducts}>Load More</button>
            <button onClick={() => navigate('/')}>Go back to main page</button>
        </div>
    );
};

export default CollectionItemsPage;
