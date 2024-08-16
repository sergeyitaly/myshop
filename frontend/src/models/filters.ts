
export interface ProductFilter {
    name?: string
    category?: string
    price?: string
    sales_count?: string
    popularity?: string
    search?: string
    ordering?: string
    page?: number
    page_size?: number
}

export interface CollectionProductFilter {
    search?: string
    ordering?: string
    page?: number
    page_size?: number
}

export interface CollectionFilter {
    category?: string
    search?: string
    ordering?: string
    page?: number
    page_size?: number
}

export interface CategoryFilter {
    name?: string
    search?: string
    page?: number
    page_size?: number
}

export interface MainFilter {
    category?: string
    collection?: string
    name?: string
    price_min?: number
    price_max?: number
    sales_count?: number
    popularity?: number
    search?: string
    ordering?: string
    page?: number
    page_size?: number
}




