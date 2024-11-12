import React from "react";  
import { NamedSection } from "../../components/NamedSection/NamedSection";
import { NewProducts } from "../../sections/TabSection/NewProducts";
import { PageContainer } from "../../components/containers/PageContainer";
import { useTranslation } from "react-i18next";


export const NewProductsPage: React.FC = () => {
    const { t } = useTranslation();

    return (
        <PageContainer>
            <div style={{ marginTop: '60px' }}>
            <NamedSection
                title={t('new_arrivals')}
            >
                <NewProducts />
                </NamedSection>
            </div>
        </PageContainer>
    );
};