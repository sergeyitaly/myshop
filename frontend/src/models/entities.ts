// interface Product {
//     id: string;
//     name: string;
//     price: string;
//     photo: string;
//   }

export interface Product {
    id: number | string
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


interface Color {
    name?: string
    color: string
}

export interface ProductVariantsModel {
    colors: Color[]
    sizes: string[]
}

interface ProductImage {
    id: string;
    images: string; // Assuming 'images' property contains image URLs
}

export interface ProductColorModel {
    productId: Product['id']
    name: string
    color: string
}

export interface ProductSizeModel {
    productId: Product['id']
    value: string | number
}