import { useParams } from "react-router-dom";
import { PageContainer } from "../containers/PageContainer";
import { ProductGallery } from "./components/ProductGallery/ProductGallery";
import { ProductInfo } from "./components/ProductInfo/ProductInfo";
import { useProduct } from "../../hooks/useProduct";
import { countDiscountPrice } from "../../functions/countDiscountPrice";
import style from "./ProducSection.module.scss";
import clsx from "clsx";

interface ProductSectionProps {
	isLoading: boolean
}

export const ProductSection = ({
	isLoading
}: ProductSectionProps) => {
	const { id } = useParams<{ id: string }>();

	const { product, variants, changeColor, changeSize } = useProduct(id!);

	const discountPrice = product
		? countDiscountPrice(product.price, product.discount)
		: null;

	return (
		<section>
			<PageContainer className={clsx(style.product_section_container, {[style.fetching]: isLoading}) }>
				{product && (
					<>
						<ProductGallery
							defaultImage={product.photo_url}
							smallImg={product.photo_thumbnail_url}
							images={product.images}
							discount={!!discountPrice}
						/>
						<ProductInfo
							product={product}
							discountPrice={discountPrice}
							productVariants={variants}
							onChangeColor={changeColor}
							onChangeSize={changeSize}
						/>
					</>
				)}
			</PageContainer>
		</section>
	);
};
