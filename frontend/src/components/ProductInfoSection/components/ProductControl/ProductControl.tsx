
import { Product, ProductVariantsModel} from '../../../../models/entities'
import { AvailableLable } from '../../../AvailableLabel/AvailableLabel'
import { Counter } from '../../../Counter/Counter'
import { MainButton } from '../../../UI/MainButton/MainButton'
import { ValueBox } from '../../../ProductVariants/ValueBox/ValueBox'
import style from './ProductControl.module.scss'
import { ProductVariants } from '../../../ProductVariants/ProductVariants'
import { useBasket } from '../../../../hooks/useBasket'
import { useCounter } from '../../../../hooks/useCounter'
import { formatPrice } from '../../../../functions/formatPrice'
import { useNavigate } from 'react-router-dom'
import { ROUTE } from '../../../../constants'
import { useEffect } from 'react'

interface ProductControlProps {
    product: Product
    variants: ProductVariantsModel
    onChangeColor?: (color: string) => void
    onChangeSize?: (size: string) => void
}

export const ProductControl = ({
    product,
    variants,
    onChangeColor,
    onChangeSize,
}: ProductControlProps) => {

    const {name, available, price, currency} = product

    const {colors, sizes} = variants

    const {
      qty,
      setCounter
    } = useCounter(1)

    useEffect(() => {
      setCounter(1)
    }, [product.id])


    const {addToBasket, openBasket} = useBasket()

    const navigate = useNavigate()


    const handleAddToBasket = () => {
      addToBasket(product, qty)
      openBasket()
    }

    const handleClickBuyNow = () => {
      addToBasket(product, qty)
      navigate(ROUTE.ORDER)
    }

    return (
        <div className={style.container}>
          <h2 className={style.title}>{name}</h2>
          <div className={style.price}>{formatPrice(price, currency)}</div>
          <AvailableLable 
            className={style.available}
            isAvailable={available}
          />
          <ProductVariants
            className={style.color}
            title='Колір'
            value={product.color_name || ''}
          >
            {
              colors.map(({color}) => (
                <ValueBox 
                  key={color}
                  value={color}
                  isActive={color === product.color_value}
                  color={color}
                  onClick={onChangeColor}
                />
              ))
            }
          </ProductVariants>
          
          <div className={style.sizeArea}>
            <ProductVariants
                title='Розмір'
            >
                {
                    sizes.map((size) => (
                        <ValueBox 
                            key={size}
                            isActive={size === product.size}
                            value={size}
                            title={size}
                            onClick={onChangeSize}
                    />
                    ))
                }
            </ProductVariants>
            <Counter
                className={style.counter}
                value={qty}
                onChangeCounter={setCounter}
            />    
          </div>
          <MainButton
            className={style.add}
            title='Додати до кошика'
            onClick={handleAddToBasket}
          />
          <MainButton
            className={style.buy}
            color='blue'
            title='Купити зараз'
            onClick={handleClickBuyNow}
          />
        </div>
    )
}