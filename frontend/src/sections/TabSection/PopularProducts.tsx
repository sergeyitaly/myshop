import { useNavigate } from "react-router-dom";
import { useGetProductsByMainFilterQuery } from "../../api/productSlice";
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard";
import { AppSlider } from "../../components/AppSlider/AppSlider";
import { popularSettings } from "./sliderSettings/PopularProductSetting";
import { ROUTE } from "../../constants";
import { useTranslation } from "react-i18next";

export const PopularProducts = () => {
	const navigate = useNavigate();

	const { i18n } = useTranslation();
	const language = i18n.language;

	const { data, isLoading } = useGetProductsByMainFilterQuery({
		popularity: 1,
	});

	const products = data?.results || [];

	const getTranslatedProductName = (
		product: any,
		language: string
	): string => {
		return language === "uk"
			? product.name_uk || product.name
			: product.name_en || product.name;
	};

	return (
		<AppSlider isLoading={isLoading} sliderSettings={popularSettings}>
			{products.map((product) => {
				const { id, photo, discount, photo_tumbnail } = product;
				const translatedName = getTranslatedProductName(
					product,
					language
				);

				return (
					<PreviewCard
						key={id}
						photoSrc={photo}
						previewSrc={photo_tumbnail}
						title={translatedName}
						discount={discount}
						price={product.price}
						currency={product.currency}
						onClick={() => navigate(`${ROUTE.PRODUCT}${id}`)}
					/>
				);
			})}
		</AppSlider>
	);
};
