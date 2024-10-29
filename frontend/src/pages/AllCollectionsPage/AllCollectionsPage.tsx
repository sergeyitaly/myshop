import React from "react";  
import { NamedSection } from "../../components/NamedSection/NamedSection";
import { AllCollections } from "../../sections/TabSection/AllCollections";
import { useTranslation } from "react-i18next";


export const AllCollectionsPage: React.FC = () => {
    const { t } = useTranslation();

    return (
        <>
            <NamedSection
                title={t('all_collections')}
            >
                <AllCollections />
                </NamedSection>
        </>
    );
};