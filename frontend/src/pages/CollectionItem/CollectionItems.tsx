import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
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

interface PaginatedProducts {
    results: Product[];
    next: string | null;
}

const CollectionItemsPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [collection, setCollection] = useState<Collection | null>(null);
    const [products, setProducts] = useState<Product[]>([]);
    const [nextPage, setNextPage] = useState<string | null>(null);
    const apiBaseUrl = import.meta.env.VITE_LOCAL_API_BASE_URL || import.meta.env.VITE_API_BASE_URL;

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [collectionResponse, productsResponse] = await Promise.all([
                    axios.get<Collection>(`${apiBaseUrl}/collection/${id}/`),
                    axios.get<PaginatedProducts>(`${apiBaseUrl}/collection/${id}/products/`)
                ]);
                setCollection(collectionResponse.data);
                setProducts(productsResponse.data.results);
                setNextPage(productsResponse.data.next);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, [id, apiBaseUrl]);

    const loadMoreProducts = async () => {
        if (nextPage) {
            try {
                const response = await axios.get<PaginatedProducts>(nextPage);
                setProducts((prevProducts) => [...prevProducts, ...response.data.results]);
                setNextPage(response.data.next);
            } catch (error) {
                console.error('Error fetching more products:', error);
            }
        }
    };

    useEffect(() => {
        const handleScroll = () => {
            if (
                window.innerHeight + document.documentElement.scrollTop === document.documentElement.offsetHeight
            ) {
                loadMoreProducts();
            }
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, [nextPage]); // Add nextPage as a dependency to useEffect

    if (!collection) {
        return <div className={style.container}>Завантаження...</div>;
    } else if (products.length === 0) {
        return (
            <div className={style.container}>
                <h1 className={style.title}>{collection.name}</h1>
                <p>В цій колекції немає продуктів.</p>
            </div>
        );
    }

    return (
        <div className={style.container}>
            <h1 className={style.title}>{collection.name}</h1>
            <div className={style.productContainer}>
                {products.map((product) => (
                    <div key={product.id} className={style.productCard}>
                        <div className={style.cardImage}>
                            <img src={product.photo} alt={product.name} style={{ maxWidth: '100%' }} />
                            <p className={style.name}>{product.name}</p>
                            <p className={style.price}>{product.price}</p>
                        </div>
                    </div>
                ))}
            </div>
            <CarouselBestseller products={products} />
        </div>
    );
};

export default CollectionItemsPage;
