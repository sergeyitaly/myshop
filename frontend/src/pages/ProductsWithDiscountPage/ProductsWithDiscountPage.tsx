import React from "react";  
import { NamedSection } from "../../components/NamedSection/NamedSection";
import { ProductsWithDiscount } from "../../sections/TabSection/ProductsWithDiscount";
import { PageContainer } from "../../components/containers/PageContainer";
import { useTranslation } from "react-i18next";


export const ProductsWithDiscountPage: React.FC = () => {
    const { t } = useTranslation();

    return (
        <PageContainer>
            <NamedSection
                title={t('discounts')}
            >
                <ProductsWithDiscount />
                </NamedSection>
        </PageContainer>
    );
};
