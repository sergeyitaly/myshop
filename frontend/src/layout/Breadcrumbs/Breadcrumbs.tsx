import { Fragment, useEffect, useState } from 'react'
import { PageContainer } from '../../components/containers/PageContainer'
import styles from './Breadcrumbs.module.scss'
import { ROUTE } from '../../constants'
import { Link, useParams, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useGetOneCollectionByIdQuery } from '../../api/collectionSlice'
import { skipToken } from '@reduxjs/toolkit/query'
import { useGetOneProductByIdQuery } from '../../api/productSlice'
import clsx from 'clsx'

interface Breadcrumb {
    title?: string
    link?: string
    isLoading?: boolean
}

type Pages = 'collections' | 'products' | 'order' | 'home'

type ConstantRoutes = {[K in Pages]: Breadcrumb}

// Function to get translated product name
const getTranslatedProductName = (product: any, language: string): string => {
    return language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
};

// Function to get translated collection name
const getTranslatedCollectionName = (collection: any, language: string): string => {
    return language === 'uk' ? collection.name_uk || collection.name : collection.name_en || collection.name;
};

const pageDefiner = (path: string) => {

    const route = path.split('/')[1];

    let pages = {
        isCollections: false,
        isCollection: false,
        isProducts: false,
        isProduct: false,
        isOrder: false
    }

    if(route === 'collections') pages = {...pages, isCollections: true }
    if(route === 'collection')  pages = {...pages, isCollection: true }
    if(route === 'products')    pages = {...pages, isProducts: true }
    if(route === 'product')     pages = {...pages, isProduct: true}
    if(route === 'order')       pages = {...pages, isOrder: true}

    return pages
}

export const Breadcrumbs = () => {

    const {id} = useParams<{id: string}>()
    const {pathname} = useLocation()

    const { t, i18n } = useTranslation()

    const constantRoutes: ConstantRoutes = {
        collections: {
            title: t('collections'),
            link: ROUTE.COLLECTIONS
        },
        home: {
            title: t('home'),
            link: ROUTE.HOME
        },
        products: {
            title: t('All products'),
            link: ROUTE.PRODUCTS
        },
        order: {
            title: t('order'),
            link: ROUTE.ORDER
        }
    }

 

    const {
        data: collectionResponce,
        isLoading: isLoadingCollection,
        isFetching: isFetchingCollection
    } = 
    useGetOneCollectionByIdQuery((pageDefiner(pathname).isCollection && id) ? +id : skipToken )

    const {
        data: productResponce,
        isLoading: isProductLoading,
        isFetching: isProductFetching
    } = useGetOneProductByIdQuery((pageDefiner(pathname).isProduct && id) ? +id : skipToken) 

    const [list, setList] = useState<Breadcrumb[]>([])


    const getBreadcrumbs = (): Breadcrumb[] => {

        const {collections, home, order, products} = constantRoutes

        const list: Breadcrumb[] = [home]

        const pages = pageDefiner(pathname)
        const {isCollection, isCollections, isProducts, isProduct, isOrder} = pages

        

        if(isCollections){
            list.push(products)
            list.push(collections)
        }

        if(isProducts){
            list.push(products)
        }

        if(isProduct){
            list.push(products)
            list.push(collections)

            if(isProductLoading || isProductFetching)
                list.push({isLoading: true})
            else{
                list.push({
                    title: getTranslatedCollectionName(productResponce?.collection, i18n.language),
                    link: `${ROUTE.COLLECTION}${productResponce?.collection?.id}` 
                })
                list.push({
                    title: getTranslatedProductName(productResponce, i18n.language)
                })
            }
        }

        if (isCollection && id){
            list.push(products)
            list.push(collections)
            list.push({
                title: getTranslatedCollectionName(collectionResponce, i18n.language),
                link: `${ROUTE.COLLECTION}${collectionResponce?.id}`,
                isLoading: isLoadingCollection || isFetchingCollection,
            })
        }

        if(isOrder) list.push(order)

        

        return Object.values(pages).some(item => item) ? list: []
    }

    useEffect(() => {
        setList(getBreadcrumbs())
    }, [
        pathname,
        id, 
        isLoadingCollection, 
        isFetchingCollection, 
        collectionResponce, 
        productResponce, 
        isProductFetching, 
        isProductLoading
    ])

    return (
        <>
            {
                !!list.length &&
                <section className={styles.section}>
                    <PageContainer className={styles.container}>
                        {
                            list.map((item, index) => {

                                const isLast = index === list.length - 1

                                console.log(item.title, isLast);
                                const {link, title, isLoading} = item
                                
                                return (
                                    <Fragment key={title}>
                                    {
                                        isLoading ?
                                        <span>Loading...</span>
                                        :
                                        !isLast ?
                                        <>
                                            <Link
                                                className={clsx(styles.noWrap, styles.link)}
                                                to={link || ''}
                                            >
                                                {title}
                                            </Link>
                                            <span>{'>'}</span>
                                        </>
                                        : 
                                        <span className={clsx(styles.noWrap, styles.last)}>{title}</span>
                                    }
                                    </Fragment>
                                )
                            })
                        }
                    </PageContainer>
                </section>
            }
        </>
    )
}