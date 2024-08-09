import { ReactNode } from "react"
import { MapComponent } from "../../MapComponent"
import { PreviewLoadingCard } from "../../Cards/PreviewCard/PreviewLoagingCard"
import styles from './PreviewItemsContainer.module.scss'

interface PreviewItemsContainerProps {
    isLoading ?: boolean
    itemsQtyWhenLoading?: number 
    children: ReactNode
    textWhenEmpty?: string
    isError ?: boolean
    textWhenError?: string
}

export const PreviewItemsContainer = ({
    children,
    itemsQtyWhenLoading = 3,
    isLoading,
    textWhenEmpty = 'Empty',
    isError,
    textWhenError = 'Error'
}: PreviewItemsContainerProps) => {

    let isNotEmpty = false

    const isArray = Array.isArray(children)


    if(isArray){
        isNotEmpty = !!children.length
    }

    if(isLoading) {
        return (
            <div className={styles.container}>
                <MapComponent
                    qty={itemsQtyWhenLoading}
                    component={<PreviewLoadingCard/>}
                />
            </div>
        )
    }

    if(isError) {
        return (<p className={styles.errorContainer}>{textWhenError}</p>)
    }
    
    return (
        <>
            {
                isNotEmpty ?
                <div className={styles.container}>
                    {children}
                </div>
                :
                <p className={styles.emptyContainer}>{textWhenEmpty}</p>
            }
        </>
    )
}