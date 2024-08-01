import clsx from "clsx"
import { Skeleton } from "../../Skeleton/Skeleton"
import styles from './PreviewCard.module.scss'



export const PreviewLoadingCard = () => {
    return (
        <div className={styles.card}>
            <div className={styles.imageSize}>
                <Skeleton className={styles.skeleton}/>
            </div>
            <Skeleton className={clsx(styles.title, styles.skeleton)}/>
            <Skeleton className={clsx(styles.subTitle, styles.skeleton)}/>
        </div>
    )
}