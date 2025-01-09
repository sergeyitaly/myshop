import { useGetProductsByMainFilterQuery } from "../../api/productSlice";
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard";
import { AppSlider } from "../../components/AppSlider/AppSlider";
import { discountSettings } from "./sliderSettings/DiscountSetting";
import { Link } from "react-router-dom";
import { ROUTE, screens } from "../../constants";
import { useAppTranslator } from "../../hooks/useAppTranslator";
import { useMediaQuery } from "@mui/material";

export const ProductsWithDiscount = () => {
	const isMobile = useMediaQuery(screens.maxMobile);

	const { data, isLoading } = useGetProductsByMainFilterQuery({
		has_discount: true,
	});

	const products = data?.results || [];

	const { getTranslatedProductName } = useAppTranslator();

	return (
		<AppSlider
			isLoading={isLoading}
			sliderSettings={discountSettings}
			qtyOfPreloaderCards={isMobile ? 2 : 4}
		>
			{products.map((product) => {
				const {
					id,
					id_name,
					photo,
					discount,
					photo_tumbnail,
					currency,
					price,
				} = product;

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
							price={price}
							currency={currency}
						/>{" "}
					</Link>
				);
			})}
		</AppSlider>
	);
};
