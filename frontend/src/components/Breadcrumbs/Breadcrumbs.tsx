import { useEffect, useState, useMemo } from 'react';
import { useLocation, Link as RouterLink } from 'react-router-dom';
import { Breadcrumbs, Link, Stack, CircularProgress, Typography } from '@mui/material';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { useTranslation } from 'react-i18next';
import { getProductNameById, getCollectionNameById } from '../../api/api'; // Adjust the path as needed
import styles from './Breadcrumbs.module.css'; // Import CSS module

const BreadcrumbsComponent = () => {
    const location = useLocation();
    const { t, i18n } = useTranslation();
    const [breadcrumbs, setBreadcrumbs] = useState<JSX.Element[]>([]);
    const [productData, setProductData] = useState<{ name_uk?: string; name_en?: string } | null>(null);
    const [collectionData, setCollectionData] = useState<{ name_uk?: string; name_en?: string } | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const paths = useMemo(() => location.pathname.split('/').filter(Boolean), [location.pathname]);
    const isProductPage = paths.includes('product');
    const isCollectionPage = paths.includes('collection');

    const productId = isProductPage ? paths[paths.indexOf('product') + 1] : '';
    const collectionId = isCollectionPage ? paths[paths.indexOf('collection') + 1] : '';

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setError(null);

            try {
                if (isProductPage && productId) {
                    const product = await getProductNameById(productId);
                    setProductData(product);
                } else {
                    setProductData(null); // Clear product data if not on a product page
                }

                if (isCollectionPage && collectionId) {
                    const collection = await getCollectionNameById(Number(collectionId));
                    setCollectionData(collection);
                } else {
                    setCollectionData(null); // Clear collection data if not on a collection page
                }
            } catch (err) {
                setError('Error loading data');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [productId, collectionId, isProductPage, isCollectionPage]);

    const getTranslatedName = (nameUk?: string, nameEn?: string): string => {
        return i18n.language === 'uk' ? nameUk || '' : nameEn || '';
    };

    useEffect(() => {
        const generateBreadcrumbs = () => {
            if (loading) {
                setBreadcrumbs([<CircularProgress key="loading" />]);
                return;
            }

            if (error) {
                setBreadcrumbs([<Typography key="error" color="error">{error}</Typography>]);
                return;
            }

            const breadcrumbItems: JSX.Element[] = [
                <Link
                    key="/"
                    component={RouterLink}
                    underline="hover"
                    to="/"
                    sx={{ marginLeft: '30px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}
                >
                    {t('home')}
                </Link>
            ];

            // Add static breadcrumb titles
            paths.forEach((_, index) => {
                const currentPath = `/${paths.slice(0, index + 1).join('/')}`;

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
                }
            });

            // Handle collection and product names conditionally
            if (isCollectionPage && collectionData) {
                breadcrumbItems.push(
                    <span key="collectionName" style={{ marginLeft: '10px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}>
                        {getTranslatedName(collectionData.name_uk, collectionData.name_en)}
                    </span>
                );
            }

            if (isProductPage && productData) {
                breadcrumbItems.push(
                    <span key="productName" style={{ marginLeft: '10px', fontSize: '20px', fontFamily: 'Inter', color: '#000000' }}>
                        {getTranslatedName(productData.name_uk, productData.name_en)}
                    </span>
                );
            }

            setBreadcrumbs(breadcrumbItems);
        };

        generateBreadcrumbs();
    }, [productData, collectionData, loading, error, i18n.language, paths]);

    const breadcrumbTitles: Record<string, string> = useMemo(() => ({
        '/': t('home'),
        '/collections': t('collections'),
        '/about': t('about_us'),
        '/contact': t('contact'),
    }), [t]);

    return (
        <div className={styles.container} style={{ backgroundColor: '#E3E3E26E' }}>
            <Stack spacing={2}>
                {!location.pathname.includes('thank') && (
                    <Breadcrumbs separator={<NavigateNextIcon />} aria-label="breadcrumb">
                        {breadcrumbs}
                    </Breadcrumbs>
                )}
            </Stack>
        </div>
    );
};

export default BreadcrumbsComponent;
