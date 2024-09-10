import { AboutUsSection } from "../../components/AboutUsSection/AboutUsSection";
import styles from "./home.module.scss";
import CarouselCeramic from "../../components/Carousels/CarouselCeramic/CarouselCeramic";
import CarouselNewProduct from "../../components/Carousels/CarouselNewProduct/CarouselNewProduct";
import { HeroSection } from '../../components/HeroSection/HeroSection';
import { TabSection } from "../../sections/TabSection/TabSection";
import { PopularProducts } from "../../sections/TabSection/PopularProducts";
import { NamedSection } from "../../components/NamedSection/NamedSection";
import { ProductsWithDiscount } from "../../sections/TabSection/ProductsWithDiscount";
import { screens } from "../../constants";
import { useMediaQuery } from "@mui/material";
import { AllCollections } from "../../sections/TabSection/AllCollections";

export const Home = () => {

      const isMobile = useMediaQuery(screens.maxMobile)

    return (
        <main className={styles.main}>
            <HeroSection />
            <CarouselCeramic />
            <CarouselNewProduct />
            {
                isMobile ? 
                <>
                    <NamedSection
                        title={"Найпопулярніші товари"}
                    >
                        <PopularProducts/>
                    </NamedSection>
                    <NamedSection
                        title={"Знижки"}
                    >
                        <ProductsWithDiscount/>
                    </NamedSection>
                    <NamedSection
                        title={"Всі колекції"}
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
