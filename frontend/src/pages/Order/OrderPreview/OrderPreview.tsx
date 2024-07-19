import clsx from 'clsx'
import { useBasket } from '../../../hooks/useBasket'
import styles from './OrderPreview.module.scss'
import { formatPrice } from '../../../functions/formatPrice'
import { OrderItemCard } from '../../../components/Cards/OrderItemCard/OrderItemCard'

interface OrderPreviewProps {
    className?: string
}



export const OrderPreview = ({
    className
}: OrderPreviewProps) => {

    const { basketItems, totalPrice, deleteFromBasket, changeCounter} = useBasket()


    return (
        <div className={clsx(className, styles.container )}>
            <div className={styles.spaceBetween}>
                <h2 className={styles.text}>Замовлення</h2>
            </div>
            <div className={styles.content}>
            {
                basketItems.map(({product, qty}) => (
                    product &&
                    <OrderItemCard 
                        product={product}
                        qty={qty}
                        onClickDelete={deleteFromBasket}
                        onChangeCounter={(val) => changeCounter(product, val)}
                    />
                ))
            }

            </div>
            <div className={styles.spaceBetween}>
                <p className={styles.text}>Загальна сума</p>
                <p className={styles.text}>{formatPrice(totalPrice, 'UAH')}</p>
            </div>
        </div>
    )
}