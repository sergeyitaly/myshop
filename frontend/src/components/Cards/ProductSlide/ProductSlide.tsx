import { Product } from '../../../models/entities'
import style from './ProductSlide.module.scss'

interface ProductSlideProps {
    product: Product
}

export const ProductSlide = ({
    product
}: ProductSlideProps) => {

    const {photo, price, currency, name} = product

    return (
        <div 
            className={style.container}
        >
            <div className={style.imageBox}>
                <img src={photo} alt="" />
            </div>
            <h3>{name}</h3>
            <span>{price} {currency}</span>
        </div>
    )
}