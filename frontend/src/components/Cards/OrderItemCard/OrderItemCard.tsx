import { Product } from "../../../models/entities"
import defaultPhoto from '../../../assets/default.png'
import styles from './OrderItemCard.module.scss'
import { Counter } from "../../Counter/Counter"
import { AvailableLable } from "../../AvailableLabel/AvailableLabel"
import { formatPrice } from "../../../functions/formatPrice"


interface OrderItemCardProps {
    product: Product
    qty: number
    onClickDelete?: (product: Product) => void
    onClickIncrement?: (product: Product) => void
    onClickDecrement?: (product: Product) => void
}

export const OrderItemCard = ({
    product,
    qty,
    onClickDelete,
    onClickDecrement,
    onClickIncrement
}: OrderItemCardProps) => {

    const { photo, name, available, price, currency } = product

    const handleClickDelete = () => {
        onClickDelete && onClickDelete(product)
    }
    
    const handleClickIncrement = () => {
        onClickIncrement && onClickIncrement(product)
    }
    
    const handleClickReduce = () => {
        onClickDecrement && onClickDecrement(product)
    }

    return (
        <div className={styles.card}>
            <div className={styles.imageBox}>
                <div className={styles.imageWrapper}>
                    <img 
                        className={styles.image}
                        src={photo || defaultPhoto} 
                        alt={name}
                    />
                </div>
            </div>
            <div className={styles.info}>
                <div className={styles.title}>{name}</div>
                <div className={styles.control}>
                    <Counter
                        className={styles.counter}
                        value={qty}
                        onIncrement={handleClickIncrement}
                        onReduce={handleClickReduce}
                    />
                    <button 
                        className={styles.deleteButton}
                        onClick={handleClickDelete}
                    >Видалити</button>
                </div>
                <AvailableLable className={styles.available} isAvailable={available}/>
                <p className={styles.price}>{formatPrice(price, currency)}</p>
            </div>
        </div>
    )
}