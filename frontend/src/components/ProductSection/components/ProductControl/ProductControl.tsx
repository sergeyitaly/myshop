import { useEffect } from 'react';
import { Product, ProductVariantsModel } from '../../../../models/entities';
import { AvailableLable } from '../../../AvailableLabel/AvailableLabel';
import { Counter } from '../../../Counter/Counter';
import { MainButton } from '../../../UI/MainButton/MainButton';
import { ValueBox } from '../../../ProductVariants/ValueBox/ValueBox';
import style from './ProductControl.module.scss';
import { ProductVariants } from '../../../ProductVariants/ProductVariants';
import { useBasket } from '../../../../hooks/useBasket';
import { useCounter } from '../../../../hooks/useCounter';
import { formatPrice } from '../../../../functions/formatPrice';
import { useNavigate } from 'react-router-dom';
import { ROUTE } from '../../../../constants';
import { useTranslation } from 'react-i18next';

// Function to get translated product name
const getTranslatedProductName = (product: any, language: string): string => {
    return language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
};

// Function to get translated color name
const getTranslatedColorName = (color: any, language: string): string => {
    return language === 'uk' ? color.name_uk || color.name : color.name_en || color.name;
};

interface ProductControlProps {
    discountPrice?: number | null;
    product: Product;
    variants: ProductVariantsModel;
    onChangeColor?: (color: string) => void;
    onChangeSize?: (size: string) => void;
    colors?: string[]; // Add this line to accept colors

}

export const ProductControl = ({
    discountPrice,
    product,
    variants,
    onChangeColor,
    onChangeSize,
}: ProductControlProps) => {
    const { t, i18n } = useTranslation(); // Hook for translation
    const language = i18n.language;

    const { available, price, currency, color_name, color_value } = product;
    const { colors, sizes } = variants;

    const { qty, setCounter } = useCounter(1);

    useEffect(() => {
        setCounter(1);
    }, [product.id]);

    const { addToBasket, openBasket } = useBasket();
    const navigate = useNavigate();

    const handleAddToBasket = () => {
        addToBasket(product, qty);
        openBasket();
    };

    const handleClickBuyNow = () => {
        addToBasket(product, qty);
        navigate(ROUTE.ORDER);
    };

    return (
        <div className={style.container}>
            <h2 className={style.title}>{getTranslatedProductName(product, language)}</h2> {/* Translated product name */}
            <div className={style.price}>
                {formatPrice(discountPrice ? discountPrice : price, currency)}
                {discountPrice && (
                    <span className={style.discount}>{formatPrice(price, currency)}</span>
                )}
            </div>
            <AvailableLable 
                className={style.available}
                isAvailable={available}
            />
            <ProductVariants
                className={style.color}
                title={t('color')} // Translated color title
                value={getTranslatedColorName({ name: color_name }, language) || ''}
            >
                {colors.map(({ color }) => (
                    <ValueBox 
                        key={color}
                        value={color}
                        isActive={color === color_value}
                        color={getTranslatedColorName({ name: color }, language)}
                        onClick={onChangeColor}
                    />
                ))}
            </ProductVariants>
            <div className={style.sizeArea}>
                <ProductVariants
                    title={t('size')} // Translated size title
                >
                    {sizes.map((size) => (
                        <ValueBox 
                            key={size}
                            isActive={size === size}
                            value={size}
                            title={size}
                            onClick={onChangeSize}
                        />
                    ))}
                </ProductVariants>
                <Counter
                    className={style.counter}
                    value={qty}
                    onChangeCounter={setCounter}
                />    
            </div>
            <MainButton
                className={style.add}
                title={t('add_to_basket')} // Translated 'Add to basket'
                onClick={handleAddToBasket}
            />
            <MainButton
                className={style.buy}
                color='blue'
                title={t('buy_now')} // Translated 'Buy now'
                onClick={handleClickBuyNow}
            />
        </div>
    );
};
