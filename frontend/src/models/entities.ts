// interface Product {
//     id: string;
//     name: string;
//     price: string;
//     photo: string;
//   }

export interface Product {
    id: string | number
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
    price: number | string;
    sales_count: number;
    size: string
    slug: string
    stock: string
    created: Date
    updated: Date

    
    
    
    
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