export interface Product {
    id: number
    available: boolean
    brandimage: null | string
    collection: string
    color: string
    currency: string
    description: string
    images?: ProductImage[] // Make images property optional
    name: string;
    photo: string;
    photo_url: string;
    popularity: number
    price: number ;
    sales_count: number;
    size: string
    slug: string
    stock: string
    created: Date
    updated: Date
}


interface ProductImage {
    id: string;
    images: string; 
}

export interface Collection {
    id: number
    category: string
    photo_url: string
    photo: string
    name: string
    created: Date
    updated: Date
    sales_count: number
}

export interface Category {
    id: number
    name: string
}

export interface User {
    id: number
    username: string
    email: string
}

interface Color {
    name?: string
    color: string
}

export interface ProductVariantsModel {
    colors: Color[]
    sizes: string[]
}