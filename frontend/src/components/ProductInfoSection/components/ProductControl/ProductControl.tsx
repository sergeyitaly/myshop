
import { Product, ProductVariantsModel} from '../../../../models/entities'
import { AvailableLable } from '../../../AvailableLabel/AvailableLabel'
import { Counter } from '../../../Counter/Counter'
import { MainButton } from '../../../MainButton/MainButton'
import { ValueBox } from '../../../ProductVariants/ValueBox/ValueBox'
import style from './ProductControl.module.scss'
import { ProductVariants } from '../../../ProductVariants/ProductVariants'
import { useState } from 'react'

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
    onChangeSize
}: ProductControlProps) => {

    const {name, available, price, currency} = product

    const {colors, sizes} = variants

    const [quantity, setQuantity] = useState(1);

    const handleIncrement = () => {
        setQuantity((prevQuantity) => prevQuantity + 1);
      };
    
      const handleDecrement = () => {
        if (quantity > 0) {
          setQuantity((prevQuantity) => prevQuantity - 1);
        }
      };

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
                  key={color}
                  value={color}
                  isActive={color === product.color}
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
                value={quantity}
                onIncrement={handleIncrement}
                onReduce={handleDecrement}
            />    
          </div>
          <MainButton
            className={style.add}
            title='Додати до кошика'
          />
          <MainButton
            className={style.buy}
            colored
            title='Купити зараз'
          />
        </div>
    )
}