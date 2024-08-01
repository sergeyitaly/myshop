import { useEffect, useState } from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import { Breadcrumbs, Link, Stack } from '@mui/material';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { getProductNameById, getCollectionNameById } from '../../api/api';
import styles from './style.module.scss'
import { isHiddenIfLocationContainPath } from '../../functions/isHiddenIfLocationContainPath';

interface BreadcrumbTitles {
    [key: string]: string;
}



export function CustomSeparator() {
    const location = useLocation();
    const [productName, setProductName] = useState<string>('');
    const [collectionName, setCollectionName] = useState<string>('');
    const [collectionNum, setCollectionNum] = useState<string>(''); // Initialize collectionNum state

    
     
    

    useEffect(() => {
        const fetchData = async () => {
            try {
                const paths = location.pathname.split('/').filter(Boolean);

                if (paths.includes('product')) {
                    const productId = paths[paths.indexOf('product') + 1];
                    const product = await getProductNameById(productId);
                    setProductName(product.name);

                } else if (paths.includes('collection')) {
                    const collectionId = paths[paths.indexOf('collection') + 1];
                    const collection = await getCollectionNameById(+collectionId);
                    setCollectionName(collection.name);
                    setCollectionNum(collectionId); // Set collectionNum from collectionId
                } else {
                    setProductName('');
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();

        return () => {
            setProductName('');
        };
    }, [location.pathname]);

    const breadcrumbTitles: BreadcrumbTitles = {
        '/': 'Головна',
        '/collections': 'Колекції',
        '/about': 'Про нас',
        '/contact': 'Контакти',
    };

    const generateBreadcrumbs = () => {
        const paths = location.pathname.split('/').filter(Boolean);
        const breadcrumbs = [];

        if (location.pathname !== '/') {
            breadcrumbs.push(
                <Link
                    key="/"
                    component={RouterLink}
                    underline="hover"
                    to="/"
                    sx={{ marginLeft: '30px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}
                >
                    Головна
                </Link>
            );
        }

        paths.forEach((path, index) => {
            const currentPath = `/${path}`;

            if (breadcrumbTitles[currentPath]) {
                breadcrumbs.push(
                    <Link
                        key={currentPath}
                        component={RouterLink}
                        underline="hover"
                        to={currentPath}
                        sx={{ marginLeft: '10px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}
                        >
                        {breadcrumbTitles[currentPath]}
                    </Link>
                );
            } else {
                if (index === paths.length - 1 && productName && collectionName) {
                    breadcrumbs.push(
                        <Link
                            key="collections"
                            component={RouterLink}
                            underline="hover"
                            to="/collections"
                            sx={{  marginLeft: '10px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}
                        >
                            Колекції
                        </Link>,
                        <Link
                            key="collection"
                            component={RouterLink}
                            underline="hover"
                            to={`/collection/${collectionNum}`}
                            sx={{ marginLeft: '10px',fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}
                        >
                            {collectionName}
                        </Link>,
                        <span key="productName" style={{ fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}>
                            {productName}
                        </span>
                    );
                } else if (index === paths.length - 1 && productName) {
                    breadcrumbs.push(
                        <Link
                            key="collections"
                            component={RouterLink}
                            underline="hover"
                            to="/collections"
                            sx={{ marginLeft: '10px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}
                        >
                            Колекції
                        </Link>,
                        <span key="productName" style={{ marginLeft: '10px',fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}>
                            {productName}
                        </span>
                    );
                } else if (index === paths.length - 1 && collectionName) {
                    breadcrumbs.push(
                        <Link
                            key="collections"
                            component={RouterLink}
                            underline="hover"
                            to="/collections"
                            sx={{ marginLeft: '10px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}
                        >
                            Колекції
                        </Link>,
                        <span key="collectionName" style={{ marginLeft: '10px',fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}>
                            {collectionName}
                        </span>
                    );
                }
            }
        });

        return breadcrumbs;
    };

    return (
        <div className={styles.container} style={{ backgroundColor: '#E3E3E26E' }}>
            <Stack spacing={2}>
                {
                    !isHiddenIfLocationContainPath(location.pathname, 'thank') &&
                    <Breadcrumbs separator={<NavigateNextIcon />} aria-label="breadcrumb">
                        {generateBreadcrumbs()}
                    </Breadcrumbs>
                }
            </Stack>
        </div>
    );
}