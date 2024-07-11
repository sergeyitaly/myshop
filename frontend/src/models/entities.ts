export type Currency = 'UAH' | 'USD' | 'EUR'

export interface AdditionalField {
    name: string
    value: string
}

export interface Product {
    id: number,
    photo_url: string,
    collection: string,
    images: ProductImage[],
    photo: string | null,
    brandimage: string | null,
    name: string,
    description: string | null,
    price: string,
    stock: number,
    available: boolean,
    created: Date,
    updated: Date,
    sales_count: number,
    popularity: number,
    slug: string,
    color_name: string | null,
    color_value: string | null,
    size: string | null,
    currency: Currency
    additional_fields: AdditionalField[]
  }


export interface ProductImage {
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

export interface BasketItemModel {
    productId: number
    qty: number
}


export interface Order {
    name: string
    surname: string
    phone: number
    email: string
    address: string
    receiver: boolean
    receiver_comments: string | null
    submitted_at: Date
}