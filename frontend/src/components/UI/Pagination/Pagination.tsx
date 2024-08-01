import clsx from 'clsx'
import { AppIcon } from '../../SvgIconComponents/AppIcon'
import styles from './Pagination.module.scss'
import { Fragment } from 'react/jsx-runtime'

interface PaginationProps {
    className?: string
    totalPages: number
    currentPage: number
    onChange?: (pageNumber: number) => void
}


export const Pagination = ({
    className,
    totalPages,
    currentPage,
    onChange
}: PaginationProps) => {


    const pageArray = Array.from({length: totalPages}, (_, i) => i + 1)
    const isFirstPage = currentPage === pageArray[0]
    const isLastPage = currentPage === pageArray[pageArray.length - 1]

    const handleClickPage = (page: number) => {
        onChange && onChange(page)
    }

    const hanleClickNext = () => {
        !isLastPage &&
        onChange && onChange(currentPage + 1)
    }
 
    const hanleClickPrev = () => {
        !isFirstPage &&
        onChange && onChange(currentPage - 1)
    }
    

    return (
        <div className={clsx(styles.container, className) }>
            <button 
                className={styles.arrowButton}
                disabled = {isFirstPage}
                onClick={hanleClickPrev}
            >
                <AppIcon iconName='leftArrow'/> 
            </button>
            <div className={styles.pageContainer}>
                {
                    pageArray.map((number) => (
                        <Fragment key={number}>
                            {
                                <button 
                                    className={clsx(styles.pageButton, {
                                        [styles.active]: currentPage === number
                                    })}
                                    onClick={() => handleClickPage(number)}
                                >
                                        {number}
                                </button>
                            }
                        </Fragment>
                    )) 
                }
            </div>
            <button 
                className={styles.arrowButton}
                disabled = {isLastPage}
                onClick={hanleClickNext}
            >
               <AppIcon iconName='rigrtArrow'/> 
            </button>
        </div>
    )
}