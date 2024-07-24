import { Product } from "../../../models/entities"
import styles from './OrderItemCard.module.scss'
import { Counter } from "../../Counter/Counter"
import { formatPrice } from "../../../functions/formatPrice"
import { AppImage } from "../../AppImage/AppImage"


interface OrderItemCardProps {
    product: Product
    qty: number
    onClickDelete?: (product: Product) => void
    onChangeCounter?: (value: number) => void
    onClickName?: (product: Product) => void
    onClickPhoto?: (product: Product) => void
}

export const OrderItemCard = ({
    product,
    qty,
    onClickDelete,
    onChangeCounter,
    onClickName,
    onClickPhoto
}: OrderItemCardProps) => {

    const { photo, name, price, currency } = product

    const handleClickDelete = () => {
        onClickDelete && onClickDelete(product)
    }
    
    const handleClickName = () => {
        onClickName && onClickName(product)
    }

    const handleClickPhoto = () => {
        onClickPhoto && onClickPhoto(product)
    } 
   

    return (
        <div className={styles.card}>
            <button 
                className={styles.imageBox}
                onClick={handleClickPhoto}
            >
                <AppImage 
                    src={photo} 
                    alt={name}
                />
            </button>
            <div className={styles.info}>
                <div 
                    className={styles.title}
                    onClick={handleClickName}
                >{name}</div>
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