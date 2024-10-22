
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
    PRODUCTS = '/products/',
    COLLECTION = '/collection/',
    COLLECTIONS = '/collections/',
    ORDER = '/order',
    ABOUT = '/about',
    THANK = '/thank',
    CONTACTS='/contacts',
    FEEDBACK='/feedback',
    SENDCONTACTS = '/sendcontacts',
    PAYMENT_DELIVERY = '/payment_delivery',
    PRIVACY_POLICY = '/privacy_policy',
    RETURNS_REFUNDS = '/returns_refunds'
}

export enum ENDPOINTS {
    CATEGORIES = 'categories',
    CATEGORY = 'category',
    COLLECTION = 'collection',
    COLLECTIONS = 'collections',
    ORDER = 'order',
    FEEDBACK = 'feedback',
    PRODUCT = 'product',
    PRODUCTS = 'products',
    FILTER = 'products/filter',
    TEAM_MEMBERS = 'team',
    TECHNOLOGIES = 'technology',
    BRANDS = 'brand' 
   
}

export enum STORAGE {
    BASKET='basket',
    LANGUAGE='lang'
}

export const color = {
    error: '#E03131',
    gray100: '#CDCDCD',
    gray200: '#A3A3A3',
    gray300: '#787878',
    gray400: '#4F4F4F',
    gray500: '#191919',
    blue: '#0F0FFF',
    button: '#0B0599',
    background: '#ffffff',
    black: '#000000',
    brown: '#5F2111',
    gold: '#8E8B5F',
    warm: '#F3DFA2',
    dirtyWhite: '#F4F5F5',
    darkOrange: '#BB4430'
}

export type AppIconNames = 'face1' | 'face2' | 'face3' | 'face4' | 'cart' | 'cross' | 'vase' | 'delete' | 'search' | 'leftArrow' | 'rigrtArrow' | 'forwardArrow' | 'flagUkraine' | 'flagUK'
