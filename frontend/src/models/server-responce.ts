export interface ServerResponce<T> {
    count: number,
    next: null | number,
    next_page_number: null | number,
    page_size: number,
    previous: null | number,
    price_max: number,
    price_min: number,
    overall_price_max: number,
    overall_price_min: number,
    previous_page_number: null | number,
    results: T
}

export interface ShortServerResponce<T> {
    count: number;               // Total number of items
    next: string | null;         // URL for the next page of results (if available)
    previous: string | null;     // URL for the previous page of results (if available)
    results: T;                  // Array of items returned in the current page
    price_max: number;           // Maximum price of items in the current response
    price_min: number;           // Minimum price of items in the current response
    overall_price_max: number;   // Maximum price of items across the entire collection
    overall_price_min: number;   // Minimum price of items across the entire collection
}




