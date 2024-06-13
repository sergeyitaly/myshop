import { Product } from '../../../models/entities'
import style from './ProductSlide.module.scss'

interface ProductSlideProps {
    product: Product
    onClick?: (product: Product) => void
}

export const ProductSlide = ({
    product,
    onClick
}: ProductSlideProps) => {

    const {photo, price, currency, name} = product

    const handleClick = () => {
        onClick && onClick(product)
    }

    return (
        <div 
            className={style.container}
            onClick={handleClick}
        >
            <div className={style.imageBox}>
                <img src={photo} alt="" />
            </div>
            <h3>{name}</h3>
            <span>{price} {currency}</span>
        </div>
    )
}