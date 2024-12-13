import { MapComponent } from '../../MapComponent'
import { Skeleton } from '../../Skeleton/Skeleton'
import styles from './FeedbackCard.module.scss'


export const SkeletonFeedbackCard = () => {
    return (
        <div className={styles.card}>
            <Skeleton className={styles.skeletonTitle}/>
            <div className={styles.buttons}>
                <MapComponent 
                    qty={4} 
                    component={<Skeleton className={styles.buttonSkeleton}/>}
                />
                
            </div>
            <Skeleton className={styles.commentText}/>
            <Skeleton className={styles.textarea}/>
        </div>
    )
}