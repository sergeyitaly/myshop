import { useNavigate } from "react-router-dom";
import { useGetProductsByMainFilterQuery } from "../../api/productSlice";
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard";
import { AppSlider } from "../../components/AppSlider/AppSlider";
import { discountSettings } from "./sliderSettings/DiscountSetting";
import { ROUTE } from "../../constants";
import { useTranslation } from "react-i18next";

export const ProductsWithDiscount = () => {
	const navigate = useNavigate();

	const { i18n } = useTranslation();
	const language = i18n.language;

	const { data, isLoading } = useGetProductsByMainFilterQuery({
		has_discount: true,
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
		<AppSlider isLoading={isLoading} sliderSettings={discountSettings}>
			{products.map((product) => {
				const { id, photo, discount, photo_tumbnail, currency, price } =
					product;
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
						price={price}
						currency={currency}
						onClick={() => navigate(`${ROUTE.PRODUCT}${id}`)}
					/>
				);
			})}
		</AppSlider>
	);
};
