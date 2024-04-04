import { AboutUsSection } from "../components/AboutUsSection/AboutUsSection";
import { HeroSection } from "../components/HeroSection/HeroSection";
import styles from "./home.module.scss"
import CarouselCeramic from "../components/Carousels/CarouselCeramic/CarouselCeramic";
import CarouselNewProduct from "../components/Carousels/CarouselNewProduct/CarouselNewProduct";
import CarouselFilters from "../components/Carousels/CarouselFilters/CarouselFilters";

export const Home = () => {
    return (
        <main className={styles.main}>
            <HeroSection />
            <CarouselCeramic />
            <CarouselNewProduct />
            <CarouselFilters />
            <AboutUsSection />
        </main>
    );
};
