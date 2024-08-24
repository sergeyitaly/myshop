import { useEffect, useState } from 'react';
import { useLocation, Link as RouterLink } from 'react-router-dom';
import { Breadcrumbs, Link, Stack, CircularProgress, Typography } from '@mui/material';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { useTranslation } from 'react-i18next';
import useFetch from '../../hooks/useFetch'; // Adjust the path as needed
import { getProductNameById, getCollectionNameById } from '../../api/api'; // Adjust the path as needed
import styles from './Breadcrumbs.module.css'; // Import CSS module

const isHiddenIfLocationContainPath = (path: string, substring: string): boolean => path.includes(substring);

type BreadcrumbTitles = {
    [key: string]: string;
};

const getTranslatedProductName = (product: any, language: string): string => {
    return language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
};

const getTranslatedCollectionName = (collection: any, language: string): string => {
    return language === 'uk' ? collection.name_uk || collection.name : collection.name_en || collection.name;
};

const BreadcrumbsComponent = () => {
    const location = useLocation();
    const { t, i18n } = useTranslation();
    const [breadcrumbs, setBreadcrumbs] = useState<JSX.Element[]>([]);

    const paths = location.pathname.split('/').filter(Boolean);
    const isProductPage = paths.includes('product');
    const isCollectionPage = paths.includes('collection');

    const productId = isProductPage ? paths[paths.indexOf('product') + 1] : '';
    const collectionId = isCollectionPage ? paths[paths.indexOf('collection') + 1] : '';
    const collectionIdNumber = Number(collectionId);

    const [productData, productLoading, productError] = useFetch(() => getProductNameById(productId), [productId, i18n.language]);
    const [collectionData, collectionLoading, collectionError] = useFetch(() => getCollectionNameById(collectionIdNumber), [collectionId, i18n.language]);


    useEffect(() => {
        const generateBreadcrumbs = () => {
            if (productLoading || collectionLoading) {
                setBreadcrumbs([<CircularProgress key="loading" />]);
                return;
            }

            if (productError || collectionError) {
                setBreadcrumbs([<Typography key="error" color="error">Error loading data</Typography>]);
                return;
            }

            const paths = location.pathname.split('/').filter(Boolean);
            const breadcrumbItems: JSX.Element[] = [];

            if (location.pathname !== '/') {
                breadcrumbItems.push(
                    <Link
                        key="/"
                        component={RouterLink}
                        underline="hover"
                        to="/"
                        sx={{ marginLeft: '30px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}
                    >
                        {t('home')}
                    </Link>
                );
            }

            paths.forEach((path, index) => {
                const currentPath = `/${path}`;

                if (breadcrumbTitles[currentPath]) {
                    breadcrumbItems.push(
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
                    if (index === paths.length - 1 && productData && collectionData) {
                        breadcrumbItems.push(
                            <Link
                                key="collections"
                                component={RouterLink}
                                underline="hover"
                                to="/collections"
                                sx={{ marginLeft: '10px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}
                            >
                                {t('collections')}
                            </Link>,
                            <Link
                                key="collection"
                                component={RouterLink}
                                underline="hover"
                                to={`/collections/${collectionId}`}
                                sx={{ marginLeft: '10px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}
                            >
                                {getTranslatedCollectionName(collectionData, i18n.language)}
                            </Link>,
                            <span key="productName" style={{ fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}>
                                {getTranslatedProductName(productData, i18n.language)}
                            </span>
                        );
                    } else if (index === paths.length - 1 && productData) {
                        breadcrumbItems.push(
                            <Link
                                key="collections"
                                component={RouterLink}
                                underline="hover"
                                to="/collections"
                                sx={{ marginLeft: '10px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}
                            >
                                {t('collections')}
                            </Link>,
                            <span key="productName" style={{ marginLeft: '10px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}>
                                {getTranslatedProductName(productData, i18n.language)}
                            </span>
                        );
                    } else if (index === paths.length - 1 && collectionData) {
                        breadcrumbItems.push(
                            <Link
                                key="collections"
                                component={RouterLink}
                                underline="hover"
                                to="/collections"
                                sx={{ marginLeft: '10px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}
                            >
                                {t('collections')}
                            </Link>,
                            <span key="collectionName" style={{ marginLeft: '10px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}>
                                {getTranslatedCollectionName(collectionData, i18n.language)}
                            </span>
                        );
                    }
                }
            });

            setBreadcrumbs(breadcrumbItems);
        };

        generateBreadcrumbs();
    }, [productData, collectionData, productLoading, collectionLoading, productError, collectionError, i18n.language, location.pathname]);

    const breadcrumbTitles: BreadcrumbTitles = {
        '/': t('home'),
        '/collections': t('collections'),
        '/about': t('about_us'),
        '/contact': t('contact'),
    };

    return (
        <div className={styles.container} style={{ backgroundColor: '#E3E3E26E' }}>
            <Stack spacing={2}>
                {
                    !isHiddenIfLocationContainPath(location.pathname, 'thank') &&
                    <Breadcrumbs separator={<NavigateNextIcon />} aria-label="breadcrumb">
                        {breadcrumbs}
                    </Breadcrumbs>
                }
            </Stack>
        </div>
    );
};

export default BreadcrumbsComponent;
