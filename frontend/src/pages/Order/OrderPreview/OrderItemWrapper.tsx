import { OrderItemCard } from "../../../components/Cards/OrderItemCard/OrderItemCard"
import { useProduct } from "../../../hooks/useProduct"
import { BasketItemModel, Product } from "../../../models/entities"

interface OrderItemWrapperProps {
    basketItem: BasketItemModel
    onClickDelete?: (product: Product) => void
    onClickIncrement?: (product: Product) => void
    onClickDecrement?: (product: Product) => void
}


export const OrderItemWrapper = ({
    basketItem,
    onClickDelete,
    onClickDecrement,
    onClickIncrement
}: OrderItemWrapperProps) => {

    const { productId, qty } = basketItem

    const {product} = useProduct(productId)

    const handleClickDeleteItem = () => {
        onClickDelete && product && onClickDelete(product)
    }

    const handleClickIncrement = () => {
        onClickIncrement && product && onClickIncrement(product)
    }
    
    const handleClickDecrement = () => {
        onClickDecrement && product && onClickDecrement(product)
    }

    return (
        <>
            {
                product &&
                <OrderItemCard 
                    product={product}
                    qty={qty}
                    onClickDelete={handleClickDeleteItem}
                    onClickDecrement={handleClickDecrement}
                    onClickIncrement={handleClickIncrement}
                />
            }
        </>
    )
}