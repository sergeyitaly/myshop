import { Link } from "react-router-dom";
import { useGetProductsByMainFilterQuery } from "../../api/productSlice";
import { AppSlider } from "../../components/AppSlider/AppSlider";
import { PreviewCard } from "../../components/Cards/PreviewCard/PreviewCard";
import { NamedSection } from "../../components/NamedSection/NamedSection";
import { useAppTranslator } from "../../hooks/useAppTranslator";

import { ROUTE } from "../../constants";

export const BestSellersSection = () => {
	const { data, isLoading } = useGetProductsByMainFilterQuery({
		page_size: 10,
	});

	const { t, getTranslatedProductName } = useAppTranslator();

	const products = data?.results || [];

	return (
		<NamedSection title={t("bestsellers")}>
			<AppSlider isLoading={isLoading}>
				{products.map((product) => (
					<Link
						key={product.id}
						to={`${ROUTE.PRODUCT}${product.id_name}`}
						rel="noopener noreferrer"
					>
						<PreviewCard
							key={product.id}
							title={getTranslatedProductName(product)}
							discount={product.discount}
							price={product.price}
							currency={product.currency}
							photoSrc={product.photo_url || ""}
							previewSrc={product.photo_thumbnail_url || ""}
						/>{" "}
					</Link>
				))}
			</AppSlider>
		</NamedSection>
	);
};
