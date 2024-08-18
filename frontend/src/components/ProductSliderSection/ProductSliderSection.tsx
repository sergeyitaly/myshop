import { useNavigate } from "react-router-dom";
import { Product } from "../../models/entities";
import { PreviewCard } from "../Cards/PreviewCard/PreviewCard"
import { NamedSection } from "../NamedSection/NamedSection"
import { ProductSlider } from "../ProductSlider/ProductSlider"
import { useTranslation } from "react-i18next";
import { ROUTE } from "../../constants";
import styles from './ProductSliderSection.module.scss'
import { SwiperSlide } from "swiper/react";
import { MapComponent } from "../MapComponent";
import { PreviewLoadingCard } from "../Cards/PreviewCard/PreviewLoagingCard";


// Function to get translated product name
const getTranslatedProductName = (product: Product, language: string): string => {
    return language === 'uk' ? product.name_uk || product.name : product.name_en || product.name;
  };

interface ProductSliderSectionProps {
    translateField: string
    products?: Product[]
    isSuccess: boolean
    isLoading?: boolean
}

export const ProductSliderSection = ({
    products, 
    translateField,
    isSuccess,
    isLoading
}: ProductSliderSectionProps) => {

    const navigate = useNavigate()

    const { t, i18n } = useTranslation();  // Hook for translation

    const handleClickSlide = (productItem: Product) => {
        navigate(`${ROUTE.PRODUCT}${productItem.id}`);
    }

    return (
        <NamedSection
            title={t(translateField)}
        > 
            {
                isSuccess && products &&
                <ProductSlider>
                    {products.map((product) => (
                        <SwiperSlide
                            key={product.id}
                        >
                            <PreviewCard
                                className={styles.card}
                                title={getTranslatedProductName(product, i18n.language) || t('no_name')}  // Use translated name or fallback
                                discount={product.discount}
                                price={product.price}
                                currency={product.currency}
                                photoSrc={product.photo_url || ''}
                                previewSrc={product.photo_thumbnail_url || ''}
                                onClick={() => handleClickSlide(product)}
                            />
                        </SwiperSlide>
                    ))}
                </ProductSlider>
            }
            {
                isLoading && 
                <ProductSlider>
                    <SwiperSlide><PreviewLoadingCard/></SwiperSlide>
                    <SwiperSlide><PreviewLoadingCard/></SwiperSlide>
                    <SwiperSlide><PreviewLoadingCard/></SwiperSlide>
                    <SwiperSlide><PreviewLoadingCard/></SwiperSlide>
                </ProductSlider>
            }
        </NamedSection>
    )
}