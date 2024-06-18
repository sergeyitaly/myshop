import { Skeleton } from "@mui/material"
import styles from './BasketItemSkeletom.module.scss'


export const BasketItemSkeleton = () => {
    return (
        <div className={styles.container}>
            <Skeleton variant="rectangular" width={156} height={164} />
            <div className={styles.infoWrapper}>
                <Skeleton variant="rectangular"  height={24} />
                <Skeleton variant="rectangular"  height={24} />
                <Skeleton variant="rectangular"  height={24} />
                <Skeleton variant="rectangular"  height={24} />
                <Skeleton variant="rectangular"  height={24} />
            </div>
        </div>
    )
}