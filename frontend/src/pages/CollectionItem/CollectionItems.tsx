import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import style from "./style.module.scss";
import { fullData } from "../../components/Carousels/carouselMock";
import Pagination from "@mui/material/Pagination";
import CarouselBestseller from "../CollectionPage/CarouselBestseller/CarouselBestseller";
import { Link } from "react-router-dom";

const CollectionItemsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const collection = fullData.collections.find(
    (collection) => collection.id === id
  );

  interface CollectionItemsPageProps {
    products: Product[];
    loadMoreProducts: (id: string) => void;
  }

  const CollectionItemsPage: React.FC<CollectionItemsPageProps> = ({
    products,
    loadMoreProducts,
  }) => {
    const { id } = useParams<{ id?: string }>();
    const [collection, setCollection] = useState<Collection | null>(null);
    const navigate = useNavigate();

    useEffect(() => {
      const fetchCollection = async () => {
        try {
          if (id) {
            const response = await axios.get<Collection>(
              `${getApiBaseUrl()}/collections/${id}`
            );
            setCollection(response.data);
          }
        } catch (error) {
          console.error("Error fetching collection:", error);
        }
      };
      fetchCollection();
    }, [id]);

    const getApiBaseUrl = () => {
      return process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";
    };

    if (!collection) {
      return <div className={style.container}>Collection not found.</div>;
    }

    return (
      <div className={style.container}>
        <h1 className={style.title}>{collection.name}</h1>
        {products.map((product) => (
          <Link to={`/product/${id}`} key={product.id} className={style.card}>
            <div className={style.cardImage}>
              <img
                src={product.photo}
                alt={product.name}
                style={{ maxWidth: "100%" }}
              />
              <p className={style.name}>{product.name}</p>
              <p className={style.price}>{product.price}</p>
            </div>
          </Link>
        ))}
        <CarouselBestseller products={products} />
        <button onClick={() => id && loadMoreProducts(id)}>Load More</button>
        {!id && (
          <button onClick={() => navigate("/")}>Go back to main page</button>
        )}
      </div>
    );
  };
};

export default CollectionItemsPage;
