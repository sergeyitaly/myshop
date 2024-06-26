import { useEffect, useRef } from 'react'
import styles from './Basket.module.scss'
import { useBasket } from '../../hooks/useBasket'
import useClickOutside from '../../hooks/useClickOutside'
import { MainButton } from '../MainButton/MainButton'
import { AppIcon } from '../SvgIconComponents/AppIcon'
import { BasketItemWrapper } from './components/BasketItemWrapper'
import { EmptyBasket } from './components/EmptyBasket/EmptyBasket'
import clsx from 'clsx'
import { useNavigate } from 'react-router-dom'
import { ROUTE } from '../../constants'

export const Basket = (): JSX.Element => {

    const navigate = useNavigate()

    const {
        openStatus, 
        basketItems, 
        totalPrice, 
        isEmptyBasket,
        productQty,
        closeBasket, 
        deleteFromBasket, 
        increaceCounter, 
        reduceCounter

    } = useBasket()

    const basketBox = useRef<HTMLDivElement | null>(null)
    
    useClickOutside(basketBox, closeBasket)

    useEffect(() => {
        document.body.style.overflow = openStatus ? 'hidden' : 'visible'

        return () => {document.body.style.overflow = 'visible'}
        
    }, [openStatus])


    const handleClickBlueButton = () => {
        if(isEmptyBasket){
            navigate(ROUTE.HOME)
            closeBasket()
        }
    }

    return (
        <>
            {
                openStatus && 
                <div className={styles.container}>
                    <div 
                        ref={basketBox}
                        className={styles.box}
                    >
                        <header className={clsx(styles.header, {
                            [styles.endline]: isEmptyBasket
                        })}>
                            <h4 className={styles. titleContainer}>
                                <span className={styles.title}>Кошик</span>
                                <span className={styles.counter}>{`(${productQty})`}</span>
                            </h4>
                            <button onClick={closeBasket}>
                                <AppIcon iconName='cross'/>
                            </button>
                        </header>
                        <div className={clsx(styles.content, {
                            [styles.center]: isEmptyBasket
                        })}>
                            {
                                !isEmptyBasket ?
                                basketItems.map(({productId, qty}) => (
                                    <BasketItemWrapper
                                        key={productId}
                                        productId={productId}
                                        qty={qty}
                                        onClickDelete={deleteFromBasket}
                                        onClickIncrement={increaceCounter}
                                        onClickDecrement={reduceCounter}
                                    />
                                ))
                                :
                                <EmptyBasket/>
                            }
                        </div>
                        {
                            !isEmptyBasket &&
                            <div className={styles.totalPrice}>
                                <span>Загальна сума</span>   
                                <span>{totalPrice} грн</span>   
                            </div>
                        }
                        <div className={styles.actions}>
                            <MainButton
                                title= {isEmptyBasket ? 'Повернутися на головну' : 'Оформити замовлення'}
                                colored
                                onClick={handleClickBlueButton}
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