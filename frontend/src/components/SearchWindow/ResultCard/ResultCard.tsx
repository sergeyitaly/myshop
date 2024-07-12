import styles from './ResultCard.module.scss'
import defaultFoto from '../../../assets/default.png'
import clsx from 'clsx'

interface ResultCardProps {
    src: string
    title: string
    loading?: boolean
    onClick?: () => void
}


export const ResultCard = ({
    src,
    title,
    loading,
    onClick
}: ResultCardProps) => {
    return (
        <div 
            className={clsx(styles.card, {
                [styles.loading]: loading
            })}
            onClick={onClick}
        > 
            <div className={styles.imageWrapper}>
                <img 
                    className={styles.image}
                    src={src || defaultFoto} 
                    alt={title} 
                />
            </div>
            <h2 className={styles.title}>{title}</h2>
        </div>
    )
}