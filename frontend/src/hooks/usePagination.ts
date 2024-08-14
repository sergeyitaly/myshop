import { useState } from "react"


interface PaginationParams {
    initialPage?: number
    numberOfItems?: number
    limit?: number
}

export const usePagination = ({
    initialPage = 1,
    numberOfItems = 0,
    limit = 0
}: PaginationParams) => {

    const [currentPage, setCurrentPage] = useState<number>(initialPage)

    let totalPages = 0

    if(numberOfItems){
      totalPages = Math.ceil(numberOfItems / limit)
    }

    const handleChangePage = (page: number ) => {
        setCurrentPage(page)
    }

    return {
        currentPage,
        totalPages,
        setCurrentPage,
        handleChangePage
    }
}