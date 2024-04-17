import { useState, useEffect } from 'react';
import axios from 'axios';
import { Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';

interface Collection {
    id: number;
    slug: string;
    name: string;
    photo: string;
}

function CollectionsPage() {
    const [collections, setCollections] = useState<Collection[]>([]);

    useEffect(() => {
        const fetchCollections = async () => {
            try {
                const response = await axios.get<Collection[]>('http://localhost:8000/collections/');
                setCollections(response.data);
            } catch (error) {
                console.error('Error fetching collections:', error);
            }
        };

        fetchCollections();
    }, []);

    let collection = collections.filter((obj) => obj.slug === "");
    console.log(collection)

    return (
        <Container>
            <h1>Collections</h1>
            {collections.map((collection) => (
                <div key={collection.id}>
                    <Link to={`/collections/${collection.slug}`}>
                        <h3>{collection.name}</h3>
                        <img src={collection.photo} alt={collection.name} style={{ maxWidth: '100%' }} />
                    </Link>
                </div>
            ))}
        </Container>
    );
}

export default CollectionsPage;
