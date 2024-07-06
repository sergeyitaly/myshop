import clsx from 'clsx'
import { useBasket } from '../../../hooks/useBasket'
import { OrderItemWrapper } from './OrderItemWrapper'
import styles from './OrderPreview.module.scss'
import { formatPrice } from '../../../functions/formatPrice'

interface OrderPreviewProps {
    className?: string
}



export const OrderPreview = ({
    className
}: OrderPreviewProps) => {

    const { basketItems, totalPrice, deleteFromBasket, reduceCounter, increaceCounter } = useBasket()

    return (
        <div className={clsx(className, styles.container )}>
            <div className={styles.spaceBetween}>
                <h2 className={styles.text}>Замовлення</h2>
            </div>
            <div className={styles.content}>
            {
                basketItems.map((item) => (
                    <OrderItemWrapper 
                        key={item.productId}
                        basketItem={item}
                        onClickDelete={deleteFromBasket}
                        onClickDecrement={reduceCounter}
                        onClickIncrement={increaceCounter}
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