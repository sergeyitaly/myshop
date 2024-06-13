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