import React from "react";  
import { NamedSection } from "../../components/NamedSection/NamedSection";
import { NewProducts } from "../../sections/TabSection/NewProducts";
import { useTranslation } from "react-i18next";


export const NewProductsPage: React.FC = () => {
    const { t } = useTranslation();

    return (
        <>
            <NamedSection
                title={t('new_arrivals')}
            >
                <NewProducts />
                </NamedSection>
        </>
    );
};