import { useProduct } from "../../../hooks/useProduct"
import { BasketItem } from "./BasketItem"

export const BasketItemWrapper = () => {

    const {product, variants} = useProduct(13)

    return (
        <>
            {
                product &&  
                <BasketItem
                    product={product}
                    variants={variants}
                />
            }
           
        </>
    )   
}