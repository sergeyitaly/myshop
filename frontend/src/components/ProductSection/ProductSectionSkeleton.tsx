import { PageContainer } from "../containers/PageContainer"
import { ProductGellerySkeleton } from "./components/ProductGallery/ProductGallerySkeleton"
import { ProductInfoSkeleton } from "./components/ProductInfo/ProductInfoSkeleton"
import styles from './ProducSection.module.scss'


export const ProductSectionSkeleton = () => {
    return (
        <section>
            <PageContainer className={styles.product_section_container}>
                <ProductGellerySkeleton/>
                <ProductInfoSkeleton/>
            </PageContainer>
        </section>
    )
}