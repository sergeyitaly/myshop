import { useProduct } from "../../../hooks/useProduct"
import { Product } from "../../../models/entities"
import { BasketItem } from "../../Cards/BasketItem/BasketItem"
import { BasketItemSkeleton } from "../../Cards/BasketItem/BasketItemSkeleton/BasketItemSkeleton"

interface BasketItemWrapperProps {
    productId: number
    qty: number
    onClickDelete: (product: Product) => void
    onClickIncrement: (product: Product) => void
    onClickDecrement: (product: Product) => void
}

export const BasketItemWrapper = ({
    productId,
    qty,
    onClickDelete,
    onClickIncrement,
    onClickDecrement
}: BasketItemWrapperProps) => {

    const {product, variants, isLoading} = useProduct(productId)

    if(isLoading) return <BasketItemSkeleton/>

    if(product) return (
        <BasketItem
        product={product}
        qty={qty}
        variants={variants}
        onClickDelete={onClickDelete}
        onClickIncrement={onClickIncrement}
        onClickDecrement={onClickDecrement}
    />)
}