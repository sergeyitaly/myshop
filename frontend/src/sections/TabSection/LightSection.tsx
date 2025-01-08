import { useGetProductsByMainFilterQuery } from "../../api/productSlice";
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard";
import { AppSlider } from "../../components/AppSlider/AppSlider";
import { lightSettings } from "./sliderSettings/LightSettings";
import { Link } from "react-router-dom";
import { ROUTE, screens } from "../../constants";
import { useAppTranslator } from "../../hooks/useAppTranslator";
import { useMediaQuery } from "@mui/material";
import styles from "./TabSection.module.scss";

export const LightSection = () => {
	const isMobile = useMediaQuery(screens.maxMobile);

	const { data, isLoading } = useGetProductsByMainFilterQuery({
		category: "5",
	});

	const products = data?.results || [];

	const { getTranslatedProductName } = useAppTranslator();

	return (
		<AppSlider
			isLoading={isLoading}
			sliderSettings={lightSettings}
			qtyOfPreloaderCards={isMobile ? 2 : 3}
		>
			{products.map((product) => {
				const { id, photo, id_name, discount, photo_tumbnail } =
					product;

				return (
					<Link
						key={id}
						to={`${ROUTE.PRODUCT}${id_name}`}
						rel="noopener noreferrer"
					>
						<PreviewCard
							key={id}
							className={styles.lightCard}
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
