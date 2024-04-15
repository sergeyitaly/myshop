import { AboutUsSection } from "../../components/AboutUsSection/AboutUsSection";
import styles from "./home.module.scss"
import CarouselCeramic from "../../components/Carousels/CarouselCeramic/CarouselCeramic";
import CarouselNewProduct from "../../components/Carousels/CarouselNewProduct/CarouselNewProduct";
import CarouselFilters from "../../components/Carousels/CarouselFilters/CarouselFilters";
import { HeroSection } from '../../components/HeroSection/HeroSection';
import {AllCollection, Discount, Popular} from "../../components/Carousels/Mobil/Mobile";
import {useEffect, useState} from "react";

export const Home = () => {
    const [isMobile, setIsMobile] = useState(false);

    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < 600);
        };

        handleResize();
        window.addEventListener("resize", handleResize);
        return () => {
            window.removeEventListener("resize", handleResize);
        };
    }, []);
    
    return (
        <main className={styles.main}>
            <HeroSection />
            <CarouselCeramic />
            <CarouselNewProduct />
            {isMobile ? (
                <>
                    <AllCollection />
                    <Popular />
                    <Discount />
                </>
            ) : (
                <CarouselFilters />
            )}
            <AboutUsSection />
        </main>
    );
};
