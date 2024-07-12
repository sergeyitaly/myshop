import clsx from 'clsx'
import { Skeleton } from '../../Skeleton/Skeleton'
import styles from './ResultCard.module.scss'


export const ResultCardSkeleton = () => {
    return (
        <div className={styles.card}> 
            <div className={styles.imageWrapper}>
                <Skeleton 
                    className={styles.image} 
                />
            </div>
            <Skeleton className={clsx(styles.title, styles.titleSkeleton)}/>
        </div>
    )
}