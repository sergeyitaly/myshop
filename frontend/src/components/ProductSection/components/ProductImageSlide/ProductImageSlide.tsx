import ZoomInIcon from '@mui/icons-material/ZoomIn';
import clsx from 'clsx';
import styles from './ProductImageSlide.module.scss'
import { Plug } from '../../../Plug/Plug';

interface ProductImageProps {
    src: string
    alt: string
    discount?: boolean
    className?: string
    onClickZoom: (src: string) => void
}

export const ProductImageSlide = ({
    alt,
    src,
    discount,
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
            {
                discount && <Plug className={styles.plug}/>
            }
        </div>
    )
}