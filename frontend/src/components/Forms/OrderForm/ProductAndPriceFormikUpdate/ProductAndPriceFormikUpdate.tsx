import { useFormikContext } from "formik"
import { useBasket } from "../../../../hooks/useBasket"
import { useEffect } from "react"
import { OrderDTO } from "../../../../models/dto"

export const ProductAndPriceFormikUpdate = () => {

    const {basketItems} = useBasket()
    const {setValues} = useFormikContext<OrderDTO>()

    useEffect(() => {
        const orderItems: OrderDTO['order_items'] = basketItems.map(({productId, qty}) => ({
            product_id: productId,
            quantity: qty
        }))
        setValues((state) => ({...state, order_items: orderItems}) )
    }, [basketItems])

    return <></>
}