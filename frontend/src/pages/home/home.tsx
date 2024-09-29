import { AboutUsSection } from "../../components/AboutUsSection/AboutUsSection";
import styles from "./home.module.scss";
import { HeroSection } from '../../components/HeroSection/HeroSection';
import { TabSection } from "../../sections/TabSection/TabSection";
import { PopularProducts } from "../../sections/TabSection/PopularProducts";
import { NamedSection } from "../../components/NamedSection/NamedSection";
import { ProductsWithDiscount } from "../../sections/TabSection/ProductsWithDiscount";
import { screens } from "../../constants";
import { useMediaQuery } from "@mui/material";
import { AllCollections } from "../../sections/TabSection/AllCollections";
import { LightSection } from "../../sections/TabSection/LightSection";
import { NewProducts } from "../../sections/TabSection/NewProducts";
import { useTranslation } from "react-i18next";

export const Home = () => {

      const isMobile = useMediaQuery(screens.maxMobile)

      const {t} = useTranslation()

    return (
        <main className={styles.main}>
            <HeroSection />
            <NamedSection
                title={t('light')}
            >
                <LightSection />
            </NamedSection>
            <NamedSection
                title={t('new_arrivals')}
            >
                <NewProducts/>
            </NamedSection>
            {
                isMobile ? 
                <>
                    <NamedSection
                        title={t('popularProducts')}
                    >
                        <PopularProducts/>
                    </NamedSection>
                    <NamedSection
                        title={t('discounts')}
                    >
                        <ProductsWithDiscount/>
                    </NamedSection>
                    <NamedSection
                        title={t('all_collections')}
                    >
                        <AllCollections/>
                    </NamedSection>
                </>
                :
                <TabSection/>
            }
            <AboutUsSection />
        </main>
    );
};
