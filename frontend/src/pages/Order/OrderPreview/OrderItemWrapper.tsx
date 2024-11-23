import { OrderItemCard } from "../../../components/Cards/OrderItemCard/OrderItemCard";
import { useProduct } from "../../../hooks/useProduct";
import { BasketItemModel, Product } from "../../../models/entities";
import i18n from "i18next";

interface OrderItemWrapperProps {
    basketItem: BasketItemModel;
    onClickDelete?: (product: Product) => void;
    onClickIncrement?: (product: Product) => void;
    onClickDecrement?: (product: Product) => void;
}

export const OrderItemWrapper = ({
    basketItem,
    onClickDelete,
}: OrderItemWrapperProps) => {
    const { productId, qty } = basketItem;
    const { product } = useProduct(productId.toString());
    const handleClickDeleteItem = () => {
        onClickDelete && product && onClickDelete(product);
    };

    return (
        <>
            {product && (
                <OrderItemCard
                    product={product}
                    qty={qty}
                    language={i18n.language}
                    stock={product.stock}
                    onClickDelete={handleClickDeleteItem}
                />
            )}
        </>
    );
};
