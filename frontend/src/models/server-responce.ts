export interface ServerResponce<T> {
    count: number,
    next: null | number,
    next_page_number: null | number,
    page_size: number,
    previous: null | number,
    previous_page_number: null | number,
    results: T
}

export interface ShortServerResponce<T> {
    count: number
    next: string
    previous: string
    results: T
}

