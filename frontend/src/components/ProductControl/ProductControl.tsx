
import { Product, ProductColorModel } from '../../models/entities'
import { AvailableLable } from '../AvailableLabel/AvailableLabel'
import { Counter } from '../Counter/Counter'
import { MainButton } from '../MainButton/MainButton'
import { ProductVariants } from '../ProductVariants/ProductVariants'
import { ValueBox } from '../ProductVariants/ValueBox/ValueBox'
import style from './ProductControl.module.scss'

interface ProductControlProps {
    product: Product
    colors: ProductColorModel[]
    sizes: Product['size'][]
}

export const ProductControl = ({
    product,
    colors,
    sizes
}: ProductControlProps) => {

    const {name, available, price, currency} = product

    return (
        <div className={style.container}>
          <h2 className={style.title}>{name}</h2>
          <div className={style.price}>{price} {currency}</div>
          <AvailableLable 
            className={style.available}
            isAvailable={available}
          />
          <ProductVariants
            className={style.color}
            title='Колір'
            value='позолота'
          >
            {
                    colors.map(({color}) => (
                      <ValueBox 
                        isActive={color === product.color}
                        color={color}
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
                            isActive={size === product.size}
                            value={size}
                    />
                    ))
                }
            </ProductVariants>
            <Counter
                value={1}
            />    
          </div>
          <MainButton
            className={style.add}
            title='Додати до кошика'
          />
          <MainButton
            className={style.buy}
            title='Купити зараз'
          />
        </div>
    )
}