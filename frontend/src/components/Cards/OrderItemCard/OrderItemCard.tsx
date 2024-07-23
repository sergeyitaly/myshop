import { Product } from "../../../models/entities"
import defaultPhoto from '../../../assets/default.png'
import styles from './OrderItemCard.module.scss'
import { Counter } from "../../Counter/Counter"
import { formatPrice } from "../../../functions/formatPrice"


interface OrderItemCardProps {
    product: Product
    qty: number
    onClickDelete?: (product: Product) => void
    onChangeCounter?: (value: number) => void
}

export const OrderItemCard = ({
    product,
    qty,
    onClickDelete,
    onChangeCounter
}: OrderItemCardProps) => {

    const { photo, name, price, currency } = product

    const handleClickDelete = () => {
        onClickDelete && onClickDelete(product)
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
                <p className={styles.price}>{formatPrice(price, currency)}</p>

                <div className={styles.control}>
                    <Counter
                        className={styles.counter}
                        value={qty}
                        onChangeCounter={onChangeCounter}
                    />
                    <button 
                        className={styles.deleteButton}
                        onClick={handleClickDelete}
                    >Видалити</button>
                </div>
            </div>
        </div>
    )
}