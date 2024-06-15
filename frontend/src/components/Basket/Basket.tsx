import { useEffect, useRef } from 'react'
import styles from './Basket.module.scss'
import { useBasket } from '../../hooks/useBasket'
import useClickOutside from '../../hooks/useClickOutside'
import { MainButton } from '../MainButton/MainButton'
import { AppIcon } from '../SvgIconComponents/AppIcon'
import { BasketItem } from './components/BasketItem'
import { BasketItemWrapper } from './components/BasketItemWrapper'

export const Basket = (): JSX.Element => {

    const {openStatus, closeBasket} = useBasket()

    const basketBox = useRef<HTMLDivElement | null>(null)
    
    useClickOutside(basketBox, closeBasket)

    useEffect(() => {
        document.body.style.overflow = openStatus ? 'hidden' : 'visible'

        return () => {document.body.style.overflow = 'visible'}
        
    }, [openStatus])

    return (
        <>
            {
                openStatus && 
                <div className={styles.container}>
                    <div 
                        ref={basketBox}
                        className={styles.box}
                    >
                        <header className={styles.header}>
                            <h4 className={styles. titleContainer}>
                                <span className={styles.title}>Кошик</span>
                                <span className={styles.counter}>{`(1)`}</span>
                            </h4>
                            <button onClick={closeBasket}>
                                <AppIcon iconName='cross'/>
                            </button>
                        </header>
                        <div className={styles.content}>
                            <BasketItemWrapper/>
                        </div>
                        <div className={styles.totalPrice}>
                            <span>Загальна сума</span>   
                            <span>10000 грн</span>   
                        </div>
                        <div className={styles.actions}>
                            <MainButton
                                title='Оформити замовлення'
                                colored
                            />
                            <MainButton
                                title='Продовжити покупки'
                                onClick={closeBasket}
                            />

                        </div>
                    </div>
                </div>
            }
        </>
    )
} 