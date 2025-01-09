import { useGetProductsByMainFilterQuery } from "../../api/productSlice";
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard";
import { AppSlider } from "../../components/AppSlider/AppSlider";
import { popularSettings } from "./sliderSettings/PopularProductSetting";
import { Link } from "react-router-dom";
import { ROUTE } from "../../constants";
import { useAppTranslator } from "../../hooks/useAppTranslator";

export const PopularProducts = () => {
	const { data, isLoading } = useGetProductsByMainFilterQuery({
		popularity: 1,
	});

	const products = data?.results || [];

	const { getTranslatedProductName } = useAppTranslator();

	return (
		<AppSlider isLoading={isLoading} sliderSettings={popularSettings}>
			{products.map((product) => {
				const { id, id_name, photo, discount, photo_tumbnail } =
					product;

				return (
					<Link
						key={id}
						to={`${ROUTE.PRODUCT}${id_name}`}
						rel="noopener noreferrer"
					>
						<PreviewCard
							key={id}
							photoSrc={photo}
							previewSrc={photo_tumbnail}
							title={getTranslatedProductName(product)}
							discount={discount}
							price={product.price}
							currency={product.currency}
						/>{" "}
					</Link>
				);
			})}
		</AppSlider>
	);
};
