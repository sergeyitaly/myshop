import { useFormikContext } from "formik"
import { useBasket } from "../../../../hooks/useBasket"
import { useEffect } from "react"
import { OrderFormModel } from "../order-form.model"

export const ProductAndPriceFormikUpdate = () => {

    const {basketItems, totalPrice} = useBasket()
    const {setValues} = useFormikContext<OrderFormModel>()

    useEffect(() => {
        setValues((state) => ({...state, products: basketItems, totalPrice}) )
    }, [basketItems, totalPrice])

    return <></>
}