import ZoomInIcon from '@mui/icons-material/ZoomIn';
import clsx from 'clsx';
import styles from './ProductImageSlide.module.scss'

interface ProductImageProps {
    src: string
    alt: string
    className?: string
    onClickZoom: (src: string) => void
}

export const ProductImageSlide = ({
    alt,
    src,
    className,
    onClickZoom
}: ProductImageProps) => {
    return (
        <div 
            className={clsx(styles.slide, className) }
        >
            <img src={src} alt={alt}/>
            <button 
                className={styles.zoomButton}
                onClick={() => onClickZoom(src)}
            >
                <ZoomInIcon/>
            </button>
        </div>
    )
}