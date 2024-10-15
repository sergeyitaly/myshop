import { useNavigate } from "react-router-dom";
import { useGetProductsByMainFilterQuery } from "../../api/productSlice";
import { AppSlider } from "../../components/AppSlider/AppSlider";
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard";
import { NamedSection } from "../../components/NamedSection/NamedSection";
import { useAppTranslator } from "../../hooks/useAppTranslator";
import { Product } from "../../models/entities";
import { ROUTE } from "../../constants";


export const BestSellersSection = () => {

    const navigate = useNavigate()

    const {data, isLoading} = useGetProductsByMainFilterQuery({
        page_size: 10
      })


      const {t, getTranslatedProductName} = useAppTranslator()

    const products = data?.results || []

    const handleClickSlide = (productItem: Product) => {
        navigate(`${ROUTE.PRODUCT}${productItem.id_name}`);
    }

    return (
        <NamedSection
            title={t('bestsellers')}
        > 
                <AppSlider
                    isLoading = {isLoading}
                >
                    {products.map((product) => (
                            <PreviewCard
                                key={product.id}
                                title={getTranslatedProductName(product)}  // Use translated name or fallback
                                discount={product.discount}
                                price={product.price}
                                currency={product.currency}
                                photoSrc={product.photo_url || ''}
                                previewSrc={product.photo_thumbnail_url || ''}
                                onClick={() => handleClickSlide(product)}
                            />
                    ))}
                </AppSlider>
        </NamedSection>
    )
}