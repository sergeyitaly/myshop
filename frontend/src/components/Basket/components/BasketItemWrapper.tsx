import { useGetOneProductByIdQuery } from "../../../api/productSlice"
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
}: BasketItemWrapperProps) => {

    const {data, isLoading} = useGetOneProductByIdQuery(productId)

    if(isLoading) return <BasketItemSkeleton/>

    if(data) return (
        <BasketItem
            product={data}
            qty={qty}
            color={{color: data.color_value || '', name: data.color_name || ''}}
            size={data.size || ''}
            onClickDelete={onClickDelete}
        />)
}