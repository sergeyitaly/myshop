
export const screen = {
    maxBig: '1440px',
    maxLaptop: '1366px',
    maxTablet: '1280px',
    maxMobile: '740px'
}

export const screens = {
    maxBig: '(max-width: 1440px)',
    maxLaptop: '(max-width: 1366px)',
    maxTablet: '(max-width: 1280px)',
    maxMobile: '(max-width: 740px)'
}

export enum ROUTE {
    HOME = '/',
    PRODUCT = '/product/',
    COLLECTION = '/collection/',
    ORDER = '/order/'
}

export enum ENDPOINTS {
    CATEGORIES = 'categories',
    CATEGORY = 'category',
    COLLECTION = 'collection',
    COLLECTIONS = 'collections',
    ORDER = 'order',
    PRODUCT = 'product',
    PRODUCTS = 'products'
}

export enum STORAGE {
    BASKET='basket'
}

export type AppIconNames = 'cart' | 'cross' | 'vase' | 'delete'
