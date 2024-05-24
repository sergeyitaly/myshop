import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import style from './style.module.scss';
import CarouselBestseller from '../CollectionPage/CarouselBestseller/CarouselBestseller';
import axios, { AxiosResponse } from 'axios';

interface Collection {
    id: string;
    name: string;
    photo: string;
    category: string;
}

interface Product {
    id: string;
    name: string;
    photo: string;
    price: number | string;
}

interface CollectionItemsPageProps {
    loadProductsByPage: (id: string, page: number) => Promise<AxiosResponse<any>>;
}

const CollectionItemsPage: React.FC<CollectionItemsPageProps> = ({ loadProductsByPage }) => {
    const { id } = useParams<{ id: string }>();
    const [collection, setCollection] = useState<Collection | null>(null);
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const apiBaseUrl = import.meta.env.VITE_LOCAL_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const [collectionResponse, productsResponse] = await Promise.all([
                    axios.get<Collection>(`${apiBaseUrl}/api/collection/${id}/`),
                    loadProductsByPage(id!, 1)
                ]);
                setCollection(collectionResponse.data);
                setProducts(productsResponse.data.results);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [id, apiBaseUrl, loadProductsByPage]);

    if (loading) {
        return <div className={style.container}>Loading...</div>;
    }

    if (!collection) {
        return <div className={style.container}>Collection does not exist.</div>;
    }

    if (products.length === 0) {
        return (
            <div className={style.container}>
                <h1 className={style.title}>{collection.name}</h1>
                <p>This collection has no products.</p>
            </div>
        );
    }

    return (
        <>
            <h1 className={style.title}>{collection.name}</h1>
            <div className={style.productContainer}>
                {products.map((product) => (
                    <Link to={`/product/${product.id}`} key={product.id} className={style.card}>
                        <div className={style.cardImage}>
                            <img
                                src={product.photo}
                                alt={product.name}
                                style={{ maxWidth: '100%', height: 'auto', display: 'block' }}
                                loading="lazy"
                            />
                            <p className={style.name}>{product.name}</p>
                            <p className={style.price}>{product.price}</p>
                        </div>
                    </Link>
                ))}
            </div>
            <CarouselBestseller products={products.map(product => ({ ...product, price: String(product.price) }))} />
        </>
    );
};

export default CollectionItemsPage;
