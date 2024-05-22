import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import style from "./style.module.scss";
import { fullData } from "../../components/Carousels/carouselMock";
// import Pagination from "@mui/material/Pagination";
import CarouselBestseller from "../CollectionPage/CarouselBestseller/CarouselBestseller";
import { Link } from "react-router-dom";
import axios from "axios";

const CollectionItemsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const collection = fullData.collections.find(
    (collection) => collection.id === id
  );
  interface Collection {
    id: string;
    name: string;
    photo: string;
    category: string;
  }

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
    price: number;
}

const CollectionItemsPage: React.FC = () => {
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
                    axios.get<{ results: Product[] }>(`${apiBaseUrl}/api/collection/${id}/products/`)
                ]);
                setCollection(collectionResponse.data);
                setProducts(productsResponse.data.results); // Adjusting to handle response with results key
                setLoading(false);
            } catch (error) {
                console.error('Error fetching data:', error);
                setLoading(false);
            }
        };

        fetchData();
    }, [id, apiBaseUrl]);

    if (loading) {
        return <div className={style.container}>Завантаження...</div>;
    }

    if (!collection) {
        return <div className={style.container}>Колекції не існує</div>;
    }

    if (products.length === 0) {
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
                     <Link to={`/product/${product.id}`} key={product.id} className={style.card}>
                        <div className={style.cardImage}>
                            <img
                                src={product.photo}
                                alt={product.name}
                                style={{ maxWidth: '100%', height: 'auto', display: 'block' }}
                                loading="lazy" // Add lazy loading attribute
                            />
                            <p className={style.name}>{product.name}</p>
                            <p className={style.price}>{product.price}</p>
                        </div>
                    </Link>
                ))}
            </div>
            <CarouselBestseller products={products.map(product => ({ ...product, price: String(product.price) }))} />
        </div>
    );
};

export default CollectionItemsPage;
